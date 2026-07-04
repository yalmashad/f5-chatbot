# F5 Secure Chatbot

A Docker Compose Streamlit app for testing OpenAI, OpenAI-compatible, or local Ollama models with optional F5 Guardrail protection and PDF/DOCX uploads.

## Quick Start

```bash
git clone https://github.com/yalmashad/f5-chatbot.git
cd f5-chatbot
cp .env.example .env
```

Edit `.env`, then start the app:

```bash
docker compose up -d --build
```

Open:

```text
http://localhost:8080
```

## Configuration

`.env` is for model, provider, and API key settings only.

```env
MODEL_PROVIDER=OpenAI

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o

OPENAI_COMPATIBLE_BASE_URL=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_MODEL=meta-llama/Llama-3.1-8B-Instruct

ENABLE_OLLAMA=true
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2

GUARDRAIL_HOSTNAME=https://www.us1.calypsoai.app
GUARDRAIL_API_KEY=
```

Values entered in the UI are kept only for the current browser session and are not written back to `.env`.

After editing `.env`, restart the container:

```bash
docker compose down
docker compose up -d --build
```

## Port

The host port is managed only in `docker-compose.yml`:

```yaml
ports:
  - "8080:8501"
```

If `8080` is already in use, change the left side, for example:

```yaml
ports:
  - "8501:8501"
```

Then restart:

```bash
docker compose down
docker compose up -d --build
```

## Reverse Proxy

When publishing through a reverse proxy or load balancer, WebSocket support must be enabled for Streamlit:

```text
/_stcore/stream
```

For F5 Distributed Cloud, enable WebSocket upgrade on the route and use HTTP/1.1 to the origin.

## Ollama

Ollama is for local model use. Set this in `.env` to hide it from the provider dropdown:

```env
ENABLE_OLLAMA=false
```

When running the app in Docker and Ollama on the host machine, use:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
```

## Notes

- Do not commit real API keys.
- `requirements.txt` is used by the Docker image build. Users do not need to run `pip install`.
- Supported uploads: PDF and DOCX, up to 10 MB.
