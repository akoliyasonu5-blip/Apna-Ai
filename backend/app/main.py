from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx

class Settings(BaseSettings):
    ollama_url: str = "http://ollama:11434"
    ollama_model: str = "qwen3:8b"
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
app = FastAPI(title="Apna AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.allowed_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    history: list[dict[str, str]] = Field(default_factory=list, max_length=30)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "apna-ai-api"}

@app.get("/api/model")
async def model_status():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{settings.ollama_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
        return {"provider": "self-hosted-ollama", "model": settings.ollama_model,
                "available": any(m.get("name", "").startswith(settings.ollama_model.split(":")[0]) for m in models)}
    except httpx.HTTPError:
        return {"provider": "self-hosted-ollama", "model": settings.ollama_model, "available": False}

@app.post("/api/chat")
async def chat(body: ChatRequest):
    messages = [{"role": "system", "content": "You are Apna AI, a helpful assistant. Reply in the user's language, especially Hindi when the user writes in Hindi."}]
    for item in body.history:
        role = item.get("role")
        content = item.get("content", "")
        if role in ("user", "assistant") and isinstance(content, str):
            messages.append({"role": role, "content": content[:12000]})
    messages.append({"role": "user", "content": body.message})
    try:
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(
                f"{settings.ollama_url}/api/chat",
                json={"model": settings.ollama_model, "messages": messages, "stream": False},
            )
            response.raise_for_status()
            data = response.json()
        return {"reply": data.get("message", {}).get("content", "")}
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="AI model took too long to respond")
    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail="Self-hosted AI model is not available yet")
