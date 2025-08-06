#!/usr/bin/env python3
"""
Enhanced Agentic Agent with AI Magic Features
Integrates conversational memory, multi-device operations, proactive insights, and more
"""

import os
import json
import datetime
import requests
import time
import re
import difflib
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any, Optional, Tuple
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import AI Magic Core
from ai_magic_core import (
    conversation_memory, multi_device_processor, proactive_insights,
    nlp_processor, rich_response, multi_lang, smart_notifications, self_healing
)

INFERRIX_BASE_URL = "https://cloud.inferrix.com/api"

# AI Provider Configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize AI clients
client = None
llm = None

if AI_PROVIDER == "gemini" and GEMINI_API_KEY and GEMINI_API_KEY != "test-key-for-testing":
    client = None
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        convert_system_message_to_human=True
    )
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
    print("🤖 Using Google Gemini Pro as AI provider")
elif OPENAI_API_KEY and OPENAI_API_KEY != "test-key-for-testing":
    client = OpenAI(api_key=OPENAI_API_KEY)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    print("🤖 Using OpenAI GPT-4o as AI provider")
else:
    print("⚠️ No valid AI provider configured - LLM features will be limited")
    client = None
    llm = None

# Initialize the enhanced agentic agent
enhanced_agentic_agent = None

def get_enhanced_agentic_agent():
    global enhanced_agentic_agent
    if enhanced_agentic_agent is None:
        from backend.enhanced_agentic_agent import EnhancedAgenticInferrixAgent
        enhanced_agentic_agent = EnhancedAgenticInferrixAgent()
    return enhanced_agentic_agent 