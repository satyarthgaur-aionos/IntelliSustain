from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Read from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Debug: Print DATABASE_URL status (without exposing the full URL)
if DATABASE_URL:
    print(f"✅ DATABASE_URL found: {DATABASE_URL[:20]}..." if len(DATABASE_URL) > 20 else "✅ DATABASE_URL found")
else:
    print("❌ DATABASE_URL is empty or not set")
    print("Available environment variables:", [k for k in os.environ.keys() if 'DATABASE' in k.upper() or 'DB' in k.upper()])

# Create the SQLAlchemy engine
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    print("✅ Database engine created successfully")
else:
    print("❌ Cannot create database engine - DATABASE_URL is empty")
    # Create a dummy engine for development (will fail on actual DB operations)
    engine = None

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

# Base class for models
Base = declarative_base()