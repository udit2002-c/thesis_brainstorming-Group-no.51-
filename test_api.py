#!/usr/bin/env python3
"""
Simple script to test Groq API key
"""
import os
import asyncio
import httpx

async def test_groq_api():
    """Test if Groq API key is working"""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("💡 Set it with: export GROQ_API_KEY=your_key_here")
        return False
    
    print(f"🔑 Testing API key: {api_key[:8]}...")
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test models endpoint first
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models = response.json()
                model_count = len(models.get("data", []))
                print(f"✅ API key valid! {model_count} models available")
                
                # Test a simple completion
                print("🧪 Testing thesis generation...")
                
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "user", "content": "Generate 1 thesis idea about renewable energy. Keep it brief."}
                    ],
                    "max_tokens": 200
                }
                
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"✅ API working! Generated: {content[:100]}...")
                    print("\n🚀 Your API key is ready! Start the application with:")
                    print("   python3 main.py")
                    return True
                else:
                    print(f"❌ API test failed: {response.status_code}")
                    return False
                    
            elif response.status_code == 401:
                print("❌ Invalid API key")
                print("💡 Get a new key from: https://console.groq.com/keys")
                return False
            else:
                print(f"❌ API error: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Groq API Test Script")
    print("=" * 30)
    
    result = asyncio.run(test_groq_api())
    
    if not result:
        print("\n📝 Setup Instructions:")
        print("1. Visit: https://console.groq.com/keys")
        print("2. Sign up for free")
        print("3. Create an API key")
        print("4. Run: export GROQ_API_KEY=your_key_here")
        print("5. Run this test again: python3 test_api.py") 