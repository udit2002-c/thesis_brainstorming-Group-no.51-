import os
import random
import logging
from typing import List, Optional
from fastapi import FastAPI, Request, Form, HTTPException, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Configure if mock mode should be used when APIs fail
MOCK_MODE = True

app = FastAPI(title="Thesis Statement Generator")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Configuration
API_KEY = "sk-79659c72ae1f42d699a756602c83065b"
DEFAULT_MODEL = "gemma2:2b"

# Open-WebUI API Settings
WEBUI_ENABLED = True
WEBUI_BASE_URL = "https://chat.ivislabs.in/api"

# Ollama API (Local) Settings
OLLAMA_ENABLED = True
OLLAMA_HOST = "localhost"
OLLAMA_PORT = "11434"
OLLAMA_API_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api"

# Define subfields for diversity
SUBFIELDS = [
    "Cybersecurity",
    "Software Engineering",
    "Databases",
    "Networking",
    "Cloud Computing",
    "Blockchain Technology",
    "Quantum Computing",
    "Embedded Systems",
    "Human-Computer Interaction",
    "Algorithms & Complexity Theory",
    "Artificial Intelligence"
]


class ThesisRequest(BaseModel):
    field_of_study: str
    num_ideas: int = 3
    thesis_type: str = "argumentative"
    tone: Optional[str] = "academic"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate_thesis(
        field_of_study: str = Form(...),
        num_ideas: int = Form(3),
        thesis_type: str = Form("argumentative"),
        tone: str = Form("academic"),
        model: str = Form(DEFAULT_MODEL),
        x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    try:
        # Create a simple, effective prompt
        prompt = f"Generate {num_ideas} {thesis_type} thesis ideas in the field of {field_of_study}. Use a {tone} tone. Make the ideas specific and innovative. Format each idea with a number and a brief explanation."

        logger.debug(f"Using prompt: {prompt}")

        response_text = None

        # 1. Try Open-WebUI API
        if WEBUI_ENABLED:
            try:
                logger.debug("Attempting Open-WebUI API...")
                messages = [{"role": "user", "content": prompt}]

                # Different format for API request
                request_payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000
                }

                logger.debug(f"WebUI payload: {json.dumps(request_payload)}")

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WEBUI_BASE_URL}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json=request_payload,
                        timeout=30.0
                    )

                logger.debug(f"WebUI response status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    logger.debug(f"WebUI response: {json.dumps(result)[:200]}...")

                    # Handle different response formats
                    if "choices" in result and len(result["choices"]) > 0:
                        if "message" in result["choices"][0]:
                            response_text = result["choices"][0]["message"].get("content", "").strip()
                        elif "text" in result["choices"][0]:
                            response_text = result["choices"][0]["text"].strip()

                    if response_text:
                        logger.debug("Successfully retrieved response from WebUI API")
            except Exception as e:
                logger.error(f"Open-WebUI API failed: {str(e)}")

        # 2. Try Ollama API if WebUI failed
        if OLLAMA_ENABLED and not response_text:
            try:
                logger.debug("Attempting Ollama API...")

                # Different request format for Ollama
                ollama_payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 1000
                    }
                }

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{OLLAMA_API_URL}/generate",
                        json=ollama_payload,
                        timeout=30.0
                    )

                logger.debug(f"Ollama response status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    logger.debug(f"Ollama response: {json.dumps(result)[:200]}...")
                    response_text = result.get("response", "").strip()

                    if response_text:
                        logger.debug("Successfully retrieved response from Ollama API")
            except Exception as e:
                logger.error(f"Ollama API failed: {str(e)}")

        # 3. Use mock data if all APIs failed and mock mode is enabled
        if not response_text:
            if MOCK_MODE:
                logger.warning("Using mock data as fallback")

                # Create reasonable mock thesis ideas based on the input fields
                mock_text = generate_mock_thesis(field_of_study, num_ideas, thesis_type, tone)
                response_text = mock_text
            else:
                logger.error("All APIs failed and mock mode is disabled")
                raise HTTPException(
                    status_code=503,
                    detail="Service unavailable: Could not connect to any language model API"
                )

        return {"generated_thesis": response_text}

    except Exception as e:
        logger.error(f"Error in generate_thesis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating thesis statements: {str(e)}")


def generate_mock_thesis(field, num_ideas, thesis_type, tone):
    """Generate mock thesis ideas when APIs are not available"""

    # Templates for different thesis types
    thesis_templates = {
        "argumentative": [
            f"A critical examination of the ethical implications of {field} in modern society.",
            f"Why traditional approaches to {field} are insufficient for addressing contemporary challenges.",
            f"The case for integrating {field} methodologies across interdisciplinary boundaries.",
            f"Challenging conventional wisdom: A new paradigm for {field} research.",
            f"The urgent need for regulatory frameworks in {field} to address emerging concerns."
        ],
        "analytical": [
            f"A comparative analysis of theoretical frameworks in {field}: Strengths and limitations.",
            f"Identifying patterns and trends in the evolution of {field} over the past decade.",
            f"Decomposing the complex relationships between key variables in {field} research.",
            f"A systematic review of methodological approaches in contemporary {field} studies.",
            f"Quantitative assessment of factors influencing outcomes in {field} implementations."
        ],
        "expository": [
            f"Exploring the historical development of key concepts in {field}.",
            f"Clarifying misconceptions about fundamental principles in {field}.",
            f"Illuminating the connections between {field} and related disciplines.",
            f"Examining the practical applications of theoretical {field} concepts.",
            f"Demystifying complex processes in {field} for broader understanding."
        ],
        "comparative": [
            f"Contrasting Eastern and Western approaches to {field}: Philosophical underpinnings.",
            f"Traditional versus emerging methodologies in {field}: A critical comparison.",
            f"Theoretical versus practical applications in {field}: Bridging the divide.",
            f"A cross-cultural examination of {field} practices across different regions.",
            f"Comparing the effectiveness of competing frameworks in {field} research."
        ]
    }

    # Default to argumentative if thesis_type not found
    templates = thesis_templates.get(thesis_type.lower(), thesis_templates["argumentative"])

    # Select random thesis ideas up to the requested number
    selected_ideas = random.sample(templates, min(len(templates), num_ideas))

    # Format the response
    result = ""
    for i, idea in enumerate(selected_ideas, 1):
        result += f"Thesis Idea {i}: {idea}\n\n"

    return result.strip()


@app.get("/check-api-status")
async def check_api_status(x_api_key: str = Header(None)):
    """Endpoint to check the status of connected APIs"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    status = {"webui": "unknown", "ollama": "unknown"}

    # Check WebUI
    if WEBUI_ENABLED:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{WEBUI_BASE_URL}/models",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    timeout=5.0
                )
            status["webui"] = "available" if response.status_code == 200 else f"error ({response.status_code})"
            if response.status_code == 200:
                try:
                    data = response.json()
                    status["webui_models"] = [model["id"] for model in data.get("data", []) if "id" in model]
                except:
                    status["webui_models"] = ["Error parsing model list"]
        except Exception as e:
            status["webui"] = f"unavailable ({str(e)})"

    # Check Ollama
    if OLLAMA_ENABLED:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{OLLAMA_API_URL}/tags", timeout=5.0)
            status["ollama"] = "available" if response.status_code == 200 else f"error ({response.status_code})"
            if response.status_code == 200:
                try:
                    data = response.json()
                    status["ollama_models"] = [model["name"] for model in data.get("models", [])]
                except:
                    status["ollama_models"] = ["Error parsing model list"]
        except Exception as e:
            status["ollama"] = f"unavailable ({str(e)})"

    return JSONResponse(content=status)


@app.get("/models")
async def get_models(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    try:
        models = []

        # Try to get models from WebUI
        if WEBUI_ENABLED:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{WEBUI_BASE_URL}/models",
                        headers={"Authorization": f"Bearer {API_KEY}"},
                        timeout=5.0
                    )

                if response.status_code == 200:
                    models_data = response.json()
                    if "data" in models_data and isinstance(models_data["data"], list):
                        models = [model["id"] for model in models_data["data"] if "id" in model]
                    else:
                        logger.warning("Unexpected models response format from WebUI")
            except Exception as e:
                logger.error(f"Error fetching models from Open-WebUI API: {str(e)}")

        # Try to get models from Ollama
        if OLLAMA_ENABLED and not models:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{OLLAMA_API_URL}/tags", timeout=5.0)

                if response.status_code == 200:
                    models_data = response.json()
                    if "models" in models_data and isinstance(models_data["models"], list):
                        models = [model["name"] for model in models_data["models"] if "name" in model]
                    else:
                        logger.warning("Unexpected models response format from Ollama")
            except Exception as e:
                logger.error(f"Error fetching models from Ollama: {str(e)}")

        # If no models found, provide fallback options
        if not models:
            logger.info("Using fallback model list")
            models = [DEFAULT_MODEL, "gemma2:2b", "qwen2.5:0.5b", "deepseek-r1:1.5b", "deepseek-coder:latest"]

        return {"models": models}

    except Exception as e:
        logger.error(f"Unexpected error in get_models: {str(e)}")
        return {"models": [DEFAULT_MODEL]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)