import os
import random
from typing import List, Optional
from fastapi import FastAPI, Request, Form, HTTPException, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from pydantic import BaseModel
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Thesis Statement Generator")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Configuration
API_KEY = "sk-79659c72ae1f42d699a756602c83065b"  # Replace with your actual API key
DEFAULT_MODEL = "gemma2:2b"  # Update as needed

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
    "Algorithms & Complexity Theory"
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
        model: str = Form(DEFAULT_MODEL),
        x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    try:
        # Randomly select diverse subfields
        selected_subfields = random.sample(SUBFIELDS, 3)

        # Build the prompt
        prompt = f"""
        Generate 3 unique thesis ideas in the field of Computer Science. Each idea should focus on a different subfield from the following:
        {', '.join(selected_subfields)}.
        Ensure a theoretical approach with a formal tone.
        """

        # 1️⃣ Attempt Open-WebUI API
        if WEBUI_ENABLED:
            try:
                messages = [{"role": "user", "content": prompt}]
                request_payload = {"model": model, "messages": messages}
                print(f"Attempting Open-WebUI API with payload: {json.dumps(request_payload)}")

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{WEBUI_BASE_URL}/chat/completions",
                        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                        json=request_payload,
                        timeout=60.0
                    )

                if response.status_code == 200:
                    result = response.json()
                    generated_text = result["choices"][0].get("message", {}).get("content", "").strip()
                    if generated_text:
                        return {"generated_thesis": generated_text}
            except Exception as e:
                print(f"Open-WebUI API attempt failed: {str(e)}")

        # 2️⃣ Fallback to Local Ollama API
        if OLLAMA_ENABLED:
            try:
                print("Falling back to Ollama API")
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{OLLAMA_API_URL}/generate",
                        json={"model": model, "prompt": prompt, "stream": False},
                        timeout=60.0
                    )

                if response.status_code == 200:
                    result = response.json()
                    return {"generated_thesis": result.get("response", "").strip()}
            except Exception as e:
                print(f"Ollama API attempt failed: {str(e)}")

        raise HTTPException(status_code=500, detail="Failed to generate thesis statements from any available LLM API")

    except Exception as e:
        print(f"Error generating thesis statements: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating thesis statements: {str(e)}")


@app.get("/models")
async def get_models(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

    try:
        models = []

        if WEBUI_ENABLED:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{WEBUI_BASE_URL}/models",
                        headers={"Authorization": f"Bearer {API_KEY}"}
                    )

                if response.status_code == 200:
                    models = [model["id"] for model in response.json().get("data", []) if "id" in model]
            except Exception as e:
                print(f"Error fetching models from Open-WebUI API: {str(e)}")

        if OLLAMA_ENABLED and not models:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{OLLAMA_API_URL}/tags")

                if response.status_code == 200:
                    models = [model.get("name") for model in response.json().get("models", [])]
            except Exception as e:
                print(f"Error fetching models from Ollama: {str(e)}")

        return {"models": models or [DEFAULT_MODEL, "gemma2:2b", "qwen2.5:0.5b", "deepseek-r1:1.5b", "deepseek-coder:latest"]}

    except Exception as e:
        print(f"Unexpected error in get_models: {str(e)}")
        return {"models": [DEFAULT_MODEL]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)