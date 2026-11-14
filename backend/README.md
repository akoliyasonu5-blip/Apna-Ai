# Apna AI self-hosted backend (starter)

This backend calls an Ollama model running on the same private Docker network. It does not require Gemini or another hosted-model API key.

## Initial model target

`qwen3:8b` is the initial model target for Hindi/English chat. For a small launch of around 10 users, plan for a dedicated NVIDIA GPU server with about 16 GB VRAM as a practical starting point; simultaneous requests, context length, and quantization affect capacity. A CPU-only server can run some models but will usually respond much more slowly.

## First deployment steps (on your GPU server)

1. Install Docker Engine and the NVIDIA Container Toolkit on an Ubuntu LTS GPU server.
2. Copy this folder to the server and create `.env` from `.env.example`.
3. Set a long random `POSTGRES_PASSWORD` in `.env` (do not commit `.env`).
4. In `docker-compose.yml`, enable the NVIDIA GPU reservation under the `ollama` service.
5. Run `docker compose up -d --build`.
6. Pull the model once: `docker compose exec ollama ollama pull qwen3:8b`.
7. Check `http://127.0.0.1:8000/health` and then `http://127.0.0.1:8000/api/model` from the server.

The API currently exposes `/api/chat`, `/api/model`, and `/health`. PostgreSQL storage is provisioned but user authentication, per-user chat persistence, file uploads, backups, HTTPS/domain, and production rate limits are still Phase 2/3 work. Do not expose Ollama or PostgreSQL ports publicly. Put the API behind HTTPS and authentication before public use.
