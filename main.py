import os
import logging
import httpx
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prompt_templates import get_prompt_template, generate_mock_ideas
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# API Configuration for Groq
# Get your free API key from: https://console.groq.com/keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# If no API key is provided, we'll show instructions
if not GROQ_API_KEY:
    logger.warning("No GROQ_API_KEY found in environment variables!")
    logger.warning("Get your free API key from: https://console.groq.com/keys")
    logger.warning("Then set it with: export GROQ_API_KEY=your_key_here")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

async def call_groq_api(prompt: str, num_ideas: int = 2, tone: str = "academic") -> dict:
    """Call Groq API for thesis generation"""
    if not GROQ_API_KEY:
        return {"status": "error", "message": "No GROQ_API_KEY provided. Please set your API key."}
    
    try:
        logger.debug(f"Calling Groq API with prompt: {prompt}")
        
        # Enhanced system prompt for better thesis generation
        system_prompt = f"""You are an expert academic researcher and thesis advisor. Generate {num_ideas} detailed, innovative thesis ideas based on the given prompt. 

For each thesis idea, provide:
1. A clear, compelling title
2. A brief research overview (2-3 sentences)
3. Suggested methodology
4. Expected contributions to the field

Use a {tone} tone and ensure each idea is:
- Specific and innovative
- Academically rigorous
- Feasible as a research project
- Relevant to current academic discourse

Format each idea clearly with numbers and clear sections."""

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",  # Updated model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 0.9
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GROQ_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            logger.debug(f"Groq API response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                logger.info(f"✅ Groq API SUCCESS - Generated {len(content)} characters")
                
                return {
                    "status": "success",
                    "ideas": content,
                    "api_used": "Groq (Live API)"
                }
            elif response.status_code == 401:
                logger.error("❌ Groq API: Invalid API key")
                return {"status": "error", "message": "Invalid Groq API key. Please check your API key at https://console.groq.com/keys"}
            elif response.status_code == 429:
                logger.error("❌ Groq API: Rate limit exceeded")
                return {"status": "error", "message": "Groq API rate limit exceeded. Please try again later."}
            else:
                logger.error(f"❌ Groq API error: {response.status_code} - {response.text}")
                return {"status": "error", "message": f"Groq API error: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"❌ Groq API exception: {str(e)}")
        return {"status": "error", "message": f"Groq API failed: {str(e)}"}

async def fallback_to_mock(research_field: str, num_ideas: int, tone: str, thesis_type: str) -> dict:
    """Enhanced fallback with intelligent mock data"""
    logger.warning("⚠️ Using enhanced mock data as fallback")
    
    try:
        mock_ideas = generate_mock_ideas(research_field, num_ideas, tone, thesis_type)
        return {
            "status": "success",
            "ideas": mock_ideas,
            "api_used": "Enhanced Mock System (Fallback)"
        }
    except Exception as e:
        logger.error(f"❌ Mock generation failed: {str(e)}")
        return {
            "status": "error", 
            "message": "Both API and fallback system failed"
        }

@app.post("/generate")
async def generate_thesis(
    field_of_study: str = Form(...),
    num_ideas: int = Form(...),
    thesis_type: str = Form(...),
    tone: str = Form(...),
    model: str = Form("llama-3.3-70b-versatile")  # Optional model field
):
    try:
        logger.info(f"🎯 Generating thesis ideas: {field_of_study}, {num_ideas} ideas, {thesis_type} type, {tone} tone")
        
        # Create prompt
        prompt = get_prompt_template(field_of_study, num_ideas, tone, thesis_type)
        logger.debug(f"Using prompt: {prompt}")
        
        # Try Groq API first
        result = await call_groq_api(prompt, num_ideas, tone)
        
        if result["status"] == "success":
            logger.info(f"✅ Successfully generated thesis ideas using {result['api_used']}")
            return JSONResponse(content=result)
        
        # If API fails, use enhanced mock system
        logger.warning("⚠️ Groq API failed, using enhanced fallback")
        fallback_result = await fallback_to_mock(field_of_study, num_ideas, tone, thesis_type)
        return JSONResponse(content=fallback_result)
        
    except Exception as e:
        logger.error(f"❌ Generate endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/check-api-status")
async def check_api_status():
    """Check the status of available APIs"""
    statuses = {}
    
    # Check if API key is provided
    if not GROQ_API_KEY:
        statuses["Groq"] = "❌ No API Key (Set GROQ_API_KEY environment variable)"
        statuses["Setup Instructions"] = "Get free API key from https://console.groq.com/keys"
    else:
        # Check Groq API
        try:
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{GROQ_BASE_URL}/models", headers=headers)
                if response.status_code == 200:
                    models = response.json()
                    model_count = len(models.get("data", []))
                    statuses["Groq"] = f"✅ Connected ({model_count} models available)"
                elif response.status_code == 401:
                    statuses["Groq"] = "❌ Invalid API Key"
                else:
                    statuses["Groq"] = f"❌ Error ({response.status_code})"
        except Exception as e:
            statuses["Groq"] = f"❌ Failed ({str(e)[:50]})"
    
    # Enhanced Mock System is always available
    statuses["Enhanced Mock System"] = "✅ Ready (Intelligent Fallback)"
    
    return JSONResponse(content={"statuses": statuses})

@app.get("/models")
async def get_available_models():
    """Get available models from Groq"""
    if not GROQ_API_KEY:
        return {"error": "No GROQ_API_KEY provided", "setup_url": "https://console.groq.com/keys"}
    
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{GROQ_BASE_URL}/models", headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"API returned status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Thesis Brainstorming Application...")
    if GROQ_API_KEY:
        print("✅ Groq API key found - will use live API")
    else:
        print("⚠️ No Groq API key found - will use mock data")
        print("💡 Get your free API key from: https://console.groq.com/keys")
    uvicorn.run(app, host="0.0.0.0", port=8001)