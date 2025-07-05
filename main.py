import os
import logging
import httpx
import time
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prompt_templates import get_prompt_template, generate_mock_ideas
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

# Production logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting storage
rate_limit_store: Dict[str, list] = defaultdict(list)

# Initialize FastAPI with production settings
app = FastAPI(
    title="Thesis Brainstorming Tool",
    description="AI-powered thesis idea generator for academic research",
    version="1.0.0",
    docs_url="/docs" if not os.getenv('VERCEL') else None,
    redoc_url="/redoc" if not os.getenv('VERCEL') else None
)

# Security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Trusted host middleware for production
if os.getenv('VERCEL'):
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.vercel.app", "localhost", "127.0.0.1"]
    )

# Static files directory
static_directory = os.path.join(os.path.dirname(__file__), "static")
templates_directory = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_directory)

# Mount static files (required for url_for to work)
app.mount("/static", StaticFiles(directory=static_directory), name="static")

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))  # Increased from 10 to 60
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Rate limiting function
def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    now = time.time()
    minute_ago = now - 60
    
    # Clean old requests
    rate_limit_store[client_ip] = [
        req_time for req_time in rate_limit_store[client_ip] 
        if req_time > minute_ago
    ]
    
    # Check if under limit
    if len(rate_limit_store[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        return False
    
    # Add current request
    rate_limit_store[client_ip].append(now)
    return True

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    start_time = time.time()
    
    # Rate limiting
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Please try again later."}
        )
    
    response = await call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self' https://api.groq.com;"
    )
    
    # Add performance headers
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": "production" if os.getenv('VERCEL') else "development"
    }

@app.get("/health/ready")
async def readiness_check():
    """Readiness check for deployment"""
    checks = {
        "static_files": os.path.exists(static_directory),
        "templates": os.path.exists(templates_directory),
        "groq_api_configured": bool(GROQ_API_KEY)
    }
    
    all_ready = all(checks.values())
    status_code = 200 if all_ready else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "ready": all_ready,
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main application page"""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Error serving main page: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/debug/static")
async def debug_static():
    """Debug endpoint to check static files"""
    import glob
    static_files = glob.glob(os.path.join(static_directory, "*"))
    return {
        "static_directory": static_directory,
        "static_directory_exists": os.path.exists(static_directory),
        "files": [os.path.basename(f) for f in static_files],
        "current_dir": os.getcwd(),
        "script_dir": os.path.dirname(__file__)
    }

@app.get("/static/{file_path:path}")
async def serve_static_files(file_path: str):
    """Serve static files with proper content types and security"""
    try:
        full_path = os.path.join(static_directory, file_path)
        
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Security check - prevent directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(static_directory)):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Determine content type
        content_type = "text/plain"
        if file_path.endswith('.css'):
            content_type = "text/css"
        elif file_path.endswith('.js'):
            content_type = "application/javascript"
        elif file_path.endswith('.png'):
            content_type = "image/png"
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            content_type = "image/jpeg"
        elif file_path.endswith('.gif'):
            content_type = "image/gif"
        elif file_path.endswith('.svg'):
            content_type = "image/svg+xml"
        
        # Read file
        if content_type.startswith('text/') or content_type == 'application/javascript':
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            with open(full_path, 'rb') as f:
                content = f.read()
        
        # Create response with caching headers
        response = Response(content=content, media_type=content_type)
        response.headers["Cache-Control"] = "public, max-age=86400"  # 24 hours
        response.headers["ETag"] = f'"{hash(content)}"'
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving static file {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error serving file")

async def call_groq_api(prompt: str, num_ideas: int = 2, tone: str = "academic") -> dict:
    """Call Groq API with proper error handling and timeouts"""
    if not GROQ_API_KEY:
        logger.warning("No GROQ_API_KEY provided")
        return {"status": "error", "message": "API key not configured"}
    
    try:
        logger.info(f"Calling Groq API for {num_ideas} ideas with {tone} tone")
        
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
            "Content-Type": "application/json",
            "User-Agent": "ThesisBrainstorming/1.0"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500,
            "top_p": 0.9
        }
        
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{GROQ_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            logger.info(f"Groq API response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                logger.info(f"✅ Groq API SUCCESS - Generated {len(content)} characters")
                
                return {
                    "status": "success",
                    "ideas": content,
                    "api_used": "Groq (Live API)",
                    "model": payload["model"]
                }
            elif response.status_code == 401:
                logger.error("❌ Groq API: Invalid API key")
                return {"status": "error", "message": "Invalid API key"}
            elif response.status_code == 429:
                logger.error("❌ Groq API: Rate limit exceeded")
                return {"status": "error", "message": "API rate limit exceeded. Please try again later."}
            elif response.status_code == 503:
                logger.error("❌ Groq API: Service unavailable")
                return {"status": "error", "message": "API service temporarily unavailable"}
            else:
                logger.error(f"❌ Groq API error: {response.status_code}")
                return {"status": "error", "message": f"API error: {response.status_code}"}
                
    except httpx.TimeoutException:
        logger.error("❌ Groq API timeout")
        return {"status": "error", "message": "API request timed out"}
    except httpx.RequestError as e:
        logger.error(f"❌ Groq API request error: {str(e)}")
        return {"status": "error", "message": "API connection failed"}
    except Exception as e:
        logger.error(f"❌ Groq API unexpected error: {str(e)}")
        return {"status": "error", "message": "Unexpected API error"}

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
    request: Request,
    field_of_study: str = Form(..., min_length=2, max_length=200),
    num_ideas: int = Form(..., ge=1, le=10),
    thesis_type: str = Form(...),
    tone: str = Form(...),
    model: str = Form("llama-3.3-70b-versatile")
):
    """Generate thesis ideas with comprehensive validation and error handling"""
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        # Input validation
        valid_thesis_types = ["argumentative", "analytical", "expository", "comparative"]
        valid_tones = ["academic", "persuasive", "neutral", "critical"]
        
        if thesis_type not in valid_thesis_types:
            raise HTTPException(status_code=400, detail="Invalid thesis type")
        if tone not in valid_tones:
            raise HTTPException(status_code=400, detail="Invalid tone")
        
        logger.info(f"🎯 Generating {num_ideas} thesis ideas for '{field_of_study}' from IP: {client_ip}")
        
        # Create prompt
        prompt = get_prompt_template(field_of_study, num_ideas, tone, thesis_type)
        
        # Try Groq API first
        result = await call_groq_api(prompt, num_ideas, tone)
        
        if result["status"] == "success":
            logger.info(f"✅ Successfully generated thesis ideas using {result['api_used']}")
            return JSONResponse(content=result)
        
        # If API fails, use enhanced mock system
        logger.warning("⚠️ Groq API failed, using enhanced fallback")
        fallback_result = await fallback_to_mock(field_of_study, num_ideas, tone, thesis_type)
        return JSONResponse(content=fallback_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Generate endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

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

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Resource not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    logger.error(f"Internal server error on {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    
    # Production configuration
    config = {
        "host": "0.0.0.0",
        "port": int(os.getenv("PORT", 8001)),
        "log_level": "info",
        "access_log": True,
        "server_header": False,
        "date_header": False
    }
    
    print("🚀 Starting Production Thesis Brainstorming Application...")
    print(f"📊 Environment: {'Production' if os.getenv('VERCEL') else 'Development'}")
    print(f"🔑 API Status: {'Configured' if GROQ_API_KEY else 'Using Fallback'}")
    print(f"🛡️  Rate Limit: {MAX_REQUESTS_PER_MINUTE} requests/minute")
    
    uvicorn.run(app, **config)