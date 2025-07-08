#!/usr/bin/env python3
"""
Simple script to run the TechCorp Customer Support Agent Streamlit application.
"""

import os
import sys
import subprocess

def check_environment():
    """Check if required environment variables are set."""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is not set.")
        print("\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your_api_key_here'")
        print("\nOr create a .env file with:")
        print("  OPENAI_API_KEY=your_api_key_here")
        return False
    
    print("✅ Environment variables check passed")
    return True

def run_streamlit_app():
    """Run the Streamlit application."""
    try:
        print("🚀 Starting TechCorp Customer Support Agent...")
        print("📱 The application will open in your browser at http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the application\n")
        
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/ui/streamlit_app.py",
            "--server.headless", "false",
            "--server.runOnSave", "true"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running application: {str(e)}")
        print("\nTry running manually with:")
        print("  streamlit run src/ui/streamlit_app.py")

def main():
    """Main function."""
    print("🤖 TechCorp Customer Support Agent")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run the app
    run_streamlit_app()

if __name__ == "__main__":
    main() 