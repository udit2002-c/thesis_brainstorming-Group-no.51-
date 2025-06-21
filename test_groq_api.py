#!/usr/bin/env python3
"""
Test script for Groq API integration
This script tests the API without needing a real API key
"""

import os
import httpx
import asyncio

# Test with a mock API key (will show proper error handling)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "test_key")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

async def test_groq_api():
    """Test Groq API integration"""
    print("🧪 Testing Groq API Integration")
    print("=" * 40)
    
    # Test 1: Check if API key is set
    if GROQ_API_KEY == "test_key":
        print("⚠️ Using test API key (will show error handling)")
    else:
        print(f"✅ Using real API key: {GROQ_API_KEY[:10]}...")
    
    # Test 2: Try to make a request
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": "Generate 1 thesis idea for Machine Learning"}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{GROQ_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            print(f"📡 API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                print("✅ API Success!")
                print(f"Generated content length: {len(content)} characters")
                print(f"First 200 chars: {content[:200]}...")
                return True
            elif response.status_code == 401:
                print("❌ Invalid API Key")
                print("💡 Get your free API key from: https://console.groq.com/keys")
                return False
            elif response.status_code == 429:
                print("❌ Rate limit exceeded")
                return False
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

async def test_models_endpoint():
    """Test the models endpoint"""
    print("\n🔍 Testing Models Endpoint")
    print("=" * 30)
    
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{GROQ_BASE_URL}/models", headers=headers)
            
            print(f"📡 Models API Status: {response.status_code}")
            
            if response.status_code == 200:
                models = response.json()
                model_count = len(models.get("data", []))
                print(f"✅ Found {model_count} available models")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🚀 Groq API Integration Test")
    print("=" * 50)
    
    # Test API key
    if not GROQ_API_KEY or GROQ_API_KEY == "test_key":
        print("⚠️ No real API key found")
        print("💡 To test with real API:")
        print("   1. Get free key from https://console.groq.com/keys")
        print("   2. Run: export GROQ_API_KEY=your_key_here")
        print("   3. Run this test again")
        print()
    
    # Run tests
    api_test = await test_groq_api()
    models_test = await test_models_endpoint()
    
    print("\n📊 Test Results")
    print("=" * 20)
    print(f"API Test: {'✅ PASS' if api_test else '❌ FAIL (Expected without real API key)'}")
    print(f"Models Test: {'✅ PASS' if models_test else '❌ FAIL (Expected without real API key)'}")
    
    if not api_test and GROQ_API_KEY == "test_key":
        print("\n💡 This is expected behavior without a real API key!")
        print("   The app will use intelligent fallback instead.")
    
    print("\n✅ Integration test complete!")

if __name__ == "__main__":
    asyncio.run(main()) 