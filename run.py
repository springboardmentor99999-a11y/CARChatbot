#!/usr/bin/env python3
"""
Startup script for CARChatbot API
This script initializes the database and starts the FastAPI server
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment configuration...")
    
    # Check for .env file
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found")
        print("   Copy .env.example to .env and configure your API keys")
        print("   The app will still run but OpenAI features may not work")
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("   LLM-based SLA extraction will not work")
    else:
        print("✅ OpenAI API key configured")
    
    print()

def initialize_database():
    """Initialize the database tables"""
    print("🗄️  Initializing database...")
    try:
        from backend.db import create_contracts_table, create_sla_table
        create_contracts_table()
        create_sla_table()
        print("✅ Database initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting CARChatbot API server...")
    print("   Server will be available at: http://127.0.0.1:8000")
    print("   API documentation at: http://127.0.0.1:8000/docs")
    print()
    
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 CARChatbot - Car Loan/Lease Contract Analysis API")
    print("=" * 60)
    print()
    
    check_environment()
    initialize_database()
    start_server()
