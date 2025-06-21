#!/usr/bin/env python3
"""
Production deployment validation script for Thesis Brainstorming Tool
"""

import os
import sys
import asyncio
import httpx
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        "main.py",
        "prompt_templates.py", 
        "requirements.txt",
        "vercel.json",
        "templates/index.html",
        "static/styles.css"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def check_environment():
    """Check environment variables"""
    print("\n🔍 Environment Check:")
    
    # Optional but recommended
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("✅ GROQ_API_KEY configured")
    else:
        print("⚠️  GROQ_API_KEY not set (will use fallback system)")
    
    # Check other environment variables
    env_vars = {
        "MAX_REQUESTS_PER_MINUTE": os.getenv("MAX_REQUESTS_PER_MINUTE", "10"),
        "REQUEST_TIMEOUT": os.getenv("REQUEST_TIMEOUT", "30"),
        "PORT": os.getenv("PORT", "8001")
    }
    
    for var, value in env_vars.items():
        print(f"📋 {var}: {value}")
    
    return True

async def test_api_connection():
    """Test API connection if configured"""
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("⚠️  Skipping API test (no key configured)")
        return True
    
    try:
        print("\n🔗 Testing API connection...")
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "User-Agent": "ThesisBrainstorming/1.0"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models = response.json()
                model_count = len(models.get("data", []))
                print(f"✅ API connection successful ({model_count} models available)")
                return True
            else:
                print(f"❌ API connection failed: HTTP {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API connection error: {str(e)}")
        return False

def check_security():
    """Check security configuration"""
    print("\n🛡️  Security Check:")
    
    # Check if running in production mode
    if os.getenv('VERCEL'):
        print("✅ Production mode detected")
        
        # Check CORS origins
        origins = os.getenv("ALLOWED_ORIGINS")
        if origins and origins != "*":
            print(f"✅ CORS origins configured: {origins}")
        else:
            print("⚠️  CORS origins not restricted (allows all origins)")
    else:
        print("📝 Development mode (security checks relaxed)")
    
    return True

def performance_check():
    """Check performance settings"""
    print("\n⚡ Performance Check:")
    
    rate_limit = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "10"))
    timeout = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    print(f"📊 Rate limit: {rate_limit} requests/minute")
    print(f"⏱️  Request timeout: {timeout} seconds")
    
    if rate_limit > 100:
        print("⚠️  High rate limit may impact performance")
    
    if timeout > 60:
        print("⚠️  Long timeout may affect user experience")
    
    return True

async def main():
    """Main deployment check"""
    print("🚀 Thesis Brainstorming Tool - Production Deployment Check")
    print("=" * 60)
    
    checks = [
        ("File Structure", check_files),
        ("Environment", check_environment), 
        ("Security", check_security),
        ("Performance", performance_check)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name} Check:")
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed: {str(e)}")
            all_passed = False
    
    # Test API connection
    try:
        if not await test_api_connection():
            print("⚠️  API test failed (application will use fallback)")
    except Exception as e:
        print(f"⚠️  API test error: {str(e)}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All deployment checks passed!")
        print("🚀 Ready for production deployment")
        
        print("\n📝 Deployment Instructions:")
        print("1. Commit your changes: git add . && git commit -m 'Production ready'")
        print("2. Push to repository: git push origin main")
        print("3. Deploy to Vercel: vercel --prod")
        print("4. Set environment variables in Vercel dashboard")
        print("5. Test the deployed application")
        
        return 0
    else:
        print("❌ Some checks failed - please fix issues before deployment")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)