"""
Enterprise-grade security middleware for SaaS AI applications
"""
import os
import time
import hashlib
import secrets
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from collections import defaultdict
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecurityConfig:
    """Security configuration for the application"""
    # Rate limiting
    rate_limit_requests: int = 30
    rate_limit_window: int = 60  # seconds
    
    # JWT settings
    jwt_secret: str = os.getenv("JWT_SECRET_KEY", "default-secret-change-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    
    # API security
    max_request_size: int = 10 * 1024 * 1024  # 10MB
    allowed_origins: Optional[list] = None
    enable_csrf: bool = True
    enable_xss_protection: bool = True
    
    # Input validation
    max_query_length: int = 1000
    allowed_special_chars: str = r'[^a-zA-Z0-9\s\-_.,?!@#$%&*()+=:;<>"\'/\\]'
    
    def __post_init__(self):
        if self.allowed_origins is None:
            self.allowed_origins = [
                "http://localhost:3000",
                "http://localhost:5173",
                "https://yourdomain.com"  # Add your production domain
            ]

class SecurityMiddleware:
    """Enterprise security middleware"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.rate_limit_store = defaultdict(list)
        self.blocked_ips = set()
        self.suspicious_activity = defaultdict(int)
        
    async def __call__(self, request: Request, call_next):
        """Main security middleware function"""
        start_time = time.time()
        
        try:
            # 1. IP-based security checks
            client_ip = self._get_client_ip(request)
            if client_ip in self.blocked_ips:
                return JSONResponse(
                    status_code=403,
                    content={"error": "Access denied", "code": "IP_BLOCKED"}
                )
            
            # 2. Request size validation
            if not await self._validate_request_size(request):
                return JSONResponse(
                    status_code=413,
                    content={"error": "Request too large", "code": "REQUEST_TOO_LARGE"}
                )
            
            # 3. Rate limiting
            if not self._check_rate_limit(client_ip):
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded", "code": "RATE_LIMIT_EXCEEDED"}
                )
            
            # 4. Input validation
            if not await self._validate_input(request):
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid input detected", "code": "INVALID_INPUT"}
                )
            
            # 5. CORS validation
            if not self._validate_cors(request):
                return JSONResponse(
                    status_code=403,
                    content={"error": "CORS policy violation", "code": "CORS_VIOLATION"}
                )
            
            # 6. Process request
            response = await call_next(request)
            
            # 7. Add security headers
            response = self._add_security_headers(response)
            
            # 8. Log security events
            self._log_security_event(request, response, start_time)
            
            return response
            
        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal security error", "code": "SECURITY_ERROR"}
            )
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract real client IP considering proxies"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    async def _validate_request_size(self, request: Request) -> bool:
        """Validate request size"""
        content_length = request.headers.get("content-length")
        if content_length:
            return int(content_length) <= self.config.max_request_size
        return True
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """Enhanced rate limiting with burst protection"""
        now = time.time()
        
        # Clean old entries
        self.rate_limit_store[client_ip] = [
            req_time for req_time in self.rate_limit_store[client_ip]
            if now - req_time < self.config.rate_limit_window
        ]
        
        # Check rate limit
        if len(self.rate_limit_store[client_ip]) >= self.config.rate_limit_requests:
            self.suspicious_activity[client_ip] += 1
            
            # Block IP if too many violations
            if self.suspicious_activity[client_ip] >= 5:
                self.blocked_ips.add(client_ip)
                logger.warning(f"IP {client_ip} blocked due to repeated rate limit violations")
            
            return False
        
        self.rate_limit_store[client_ip].append(now)
        return True
    
    async def _validate_input(self, request: Request) -> bool:
        """Validate input for security threats"""
        if request.method == "POST":
            try:
                body = await request.body()
                if body:
                    # Check for SQL injection patterns
                    sql_patterns = [
                        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)",
                        r"(\b(UNION|EXEC|EXECUTE)\b)",
                        r"(--|\b(OR|AND)\b\s+\d+\s*=\s*\d+)",
                        r"(\b(script|javascript|vbscript|onload|onerror)\b)",
                    ]
                    
                    body_str = body.decode('utf-8', errors='ignore').lower()
                    
                    for pattern in sql_patterns:
                        if re.search(pattern, body_str, re.IGNORECASE):
                            logger.warning(f"Potential injection attack detected from {self._get_client_ip(request)}")
                            return False
                    
                    # Check query length
                    if len(body_str) > self.config.max_query_length:
                        return False
                        
            except Exception as e:
                logger.error(f"Input validation error: {e}")
                return False
        
        return True
    
    def _validate_cors(self, request: Request) -> bool:
        """Validate CORS policy"""
        origin = request.headers.get("origin")
        if origin and self.config.allowed_origins and origin not in self.config.allowed_origins:
            logger.warning(f"CORS violation from {origin}")
            return False
        return True
    
    def _add_security_headers(self, response: Response) -> Response:
        """Add security headers to response"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response
    
    def _log_security_event(self, request: Request, response: Response, start_time: float):
        """Log security events for monitoring"""
        duration = time.time() - start_time
        client_ip = self._get_client_ip(request)
        
        # Log suspicious activities
        if response.status_code in [403, 429, 400]:
            logger.warning(
                f"Security event: {client_ip} - {request.method} {request.url.path} - "
                f"Status: {response.status_code} - Duration: {duration:.3f}s"
            )

class InputSanitizer:
    """Input sanitization utilities"""
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        """Sanitize user query input"""
        if not query:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', query)
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    @staticmethod
    def validate_device_id(device_id: str) -> bool:
        """Validate device ID format"""
        if not device_id:
            return False
        
        # Device ID should be alphanumeric with optional hyphens/underscores
        return bool(re.match(r'^[a-zA-Z0-9_-]+$', device_id))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

# Global security instance
security_config = SecurityConfig()
security_middleware = SecurityMiddleware(security_config)
input_sanitizer = InputSanitizer() 