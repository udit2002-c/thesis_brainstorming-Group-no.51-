#!/usr/bin/env python3
"""
Deployment Setup Script for Thesis Brainstorming Tool
This script helps configure environment variables for production deployment.
"""

import os
import sys
from pathlib import Path

def read_env_file():
    """Read the local .env file"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ No .env file found!")
        return {}
    
    env_vars = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    return env_vars

def main():
    """Main setup function"""
    print("🚀 Thesis Brainstorming Tool - Deployment Setup")
    print("=" * 50)
    
    # Read local environment variables
    env_vars = read_env_file()
    
    if not env_vars:
        print("❌ No environment variables found in .env file")
        print("Please run setup_env.py first to create your .env file")
        return 1
    
    print("\n📋 Environment Variables for Deployment:")
    print("=" * 50)
    
    for key, value in env_vars.items():
        # Mask sensitive values
        if 'KEY' in key.upper() or 'SECRET' in key.upper() or 'TOKEN' in key.upper():
            masked_value = value[:8] + '*' * (len(value) - 8) if len(value) > 8 else '***'
            print(f"🔑 {key}: {masked_value}")
        else:
            print(f"📝 {key}: {value}")
    
    print("\n" + "=" * 50)
    print("📋 Deployment Instructions:")
    print("=" * 50)
    
    print("\n1. 🌐 Vercel Dashboard Setup:")
    print("   - Go to https://vercel.com/dashboard")
    print("   - Select your thesis-brainstorming project")
    print("   - Go to Settings > Environment Variables")
    print("   - Add the following variables:")
    
    for key, value in env_vars.items():
        print(f"     • {key} = {value}")
    
    print("\n2. 🔧 Alternative: Vercel CLI")
    print("   - Install Vercel CLI: npm install -g vercel")
    print("   - Login: vercel login")
    print("   - Set variables: vercel env add GROQ_API_KEY")
    
    print("\n3. 🚀 Deploy:")
    print("   - Push your code: git push origin main")
    print("   - Vercel will automatically deploy")
    print("   - Or deploy manually: vercel --prod")
    
    print("\n4. ✅ Verify:")
    print("   - Check your deployed URL")
    print("   - Test the API status endpoint")
    print("   - Verify thesis generation works")
    
    print("\n" + "=" * 50)
    print("⚠️  Important Notes:")
    print("• Never commit API keys to Git (use .gitignore)")
    print("• Environment variables are encrypted in Vercel")
    print("• The deployed app will use these variables")
    print("• Local development uses .env file")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 