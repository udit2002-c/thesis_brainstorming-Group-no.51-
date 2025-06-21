#!/usr/bin/env python3
"""
Setup script for Groq API integration
This script helps users get started with a real API key
"""

import os
import webbrowser

def main():
    print("🚀 Thesis Brainstorming Application - API Setup")
    print("=" * 50)
    
    # Check if API key already exists
    current_key = os.getenv("GROQ_API_KEY")
    if current_key:
        print(f"✅ GROQ_API_KEY is already set: {current_key[:10]}...")
        choice = input("Do you want to update it? (y/n): ").lower()
        if choice != 'y':
            print("✅ Setup complete! You can now run the application.")
            return
    
    print("\n📋 Steps to get your FREE Groq API key:")
    print("1. Visit https://console.groq.com/keys")
    print("2. Sign up or log in (it's free!)")
    print("3. Click 'Create API Key'")
    print("4. Copy your API key")
    print("5. Come back here and paste it")
    
    # Open browser automatically
    open_browser = input("\n🌐 Open browser to get API key now? (y/n): ").lower()
    if open_browser == 'y':
        webbrowser.open("https://console.groq.com/keys")
    
    print("\n🔑 Once you have your API key:")
    api_key = input("Paste your Groq API key here: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    if not api_key.startswith("gsk_"):
        print("⚠️ Warning: Groq API keys usually start with 'gsk_'")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return
    
    # Save to environment (for current session)
    os.environ["GROQ_API_KEY"] = api_key
    
    # Create a .env file for persistence
    with open(".env", "w") as f:
        f.write(f"GROQ_API_KEY={api_key}\n")
    
    print("✅ API key saved successfully!")
    print("📝 Created .env file for future sessions")
    print("\n🚀 You can now run the application:")
    print("   python3 main.py")
    print("\n💡 Or with environment variable:")
    print(f"   export GROQ_API_KEY={api_key}")
    print("   python3 main.py")

if __name__ == "__main__":
    main() 