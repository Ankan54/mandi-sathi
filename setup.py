"""
Quick setup script for Mandi Saathi
"""
import os
import sys

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Data.gov.in API Configuration (optional)\n")
            f.write("DATA_GOV_API_KEY=\n\n")
            f.write("# Database Configuration\n")
            f.write("DATABASE_PATH=mandi_saathi.db\n\n")
            f.write("# Cache Configuration (in hours)\n")
            f.write("CACHE_VALIDITY_HOURS=24\n")
        print("✅ .env file created. Please add your OPENAI_API_KEY")
    else:
        print("✅ .env file already exists")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import crewai
        import openai
        import streamlit
        import requests
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def initialize_database():
    """Initialize the database"""
    try:
        from database.db_manager import DatabaseManager
        db = DatabaseManager()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def main():
    print("🌾 Mandi Saathi Setup\n")
    
    # Create .env file
    create_env_file()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OPENAI_API_KEY")
    print("2. Run: streamlit run app.py")
    print("\n🚀 Happy farming!")

if __name__ == "__main__":
    main()
