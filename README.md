# F5 Secure Chatbot

A Streamlit chatbot UI for testing model responses and document uploads with optional F5 Guardrail protection.

## Features

- OpenAI model provider
- OpenAI-compatible model provider
- Optional Ollama provider for local models
- F5 Guardrail `Inline` and `Out-of-band` modes
- PDF and DOCX document uploads
- `.env` based startup configuration
- Docker Compose deployment

## Clone

```bash
git clone https://github.com/yalmashad/f5-chatbot.git
cd f5-chatbot
```

## Configuration

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Any value left empty can be entered in the app UI during a session.

```env
MODEL_PROVIDER=OpenAI

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

OPENAI_COMPATIBLE_BASE_URL=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_MODEL=meta-llama/Llama-3.1-8B-Instruct

ENABLE_OLLAMA=true
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2

GUARDRAIL_HOSTNAME=https://www.us1.calypsoai.app
GUARDRAIL_API_KEY=

APP_PORT=8080
```

The `.env` file stays in the cloned project directory on your machine. Docker Compose reads it when the container starts and passes those values into the container. You edit `.env` before running the app; you do not need to edit files inside the running container.

The UI loads values from `.env` when a new session starts. Values entered in the UI are kept only for the current browser session and are not written back to `.env`.

Legacy names `F5AI_API_KEY`, `F5_GUARDRAIL_API_KEY`, `CALYPSO_HOSTNAME`, `OPENAI_COMPATIBLE_HOSTNAME`, and `OPENAI_COMPATIBLE_KEY` are also accepted.

## Model Providers

### OpenAI

Use this provider with OpenAI models.

Required values:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`

### OpenAI Compatible

Use this provider with an API that supports the OpenAI chat completions schema.

Required values:

- `OPENAI_COMPATIBLE_BASE_URL`, usually ending in `/v1`
- `OPENAI_COMPATIBLE_API_KEY`
- `OPENAI_COMPATIBLE_MODEL`

### Ollama

Ollama is intended for local model use. Set `ENABLE_OLLAMA=false` to remove it from the provider dropdown.

Required values when enabled:

- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`

If you run the app directly on your machine, the usual Ollama URL is:

```env
OLLAMA_BASE_URL=http://localhost:11434/v1
```

If you run the app in Docker and Ollama on your host machine, use:

```env
OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
```

## Guardrail Modes

### Inline

The app sends the prompt to the F5 Guardrail Prompt API and returns the Guardrail response directly.

### Out-of-band

The app scans the user prompt, sends the prompt to the selected model provider, then scans the model response before displaying it.

### Disabled

The app sends prompts directly to the selected model provider and does not call F5 Guardrail APIs.

## Document Uploads

- Supported formats: PDF and DOCX
- Maximum file size: 10 MB
- Maximum extracted text: 100,000 characters
- Scanned PDFs that require OCR are not supported

The app extracts document text locally, sends the combined prompt and document text to F5 Guardrail, then sends document context to the model only after inspection clears.

## Run Locally With Python

Requirements:

- Python 3.10+
- An OpenAI, OpenAI-compatible, or Ollama model endpoint
- An F5 Guardrail API key if using `Inline` or `Out-of-band`

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run f5_chatbot.py
```

Open:

```text
http://localhost:8501
```

## Run With Docker Compose

Build and start:

```bash
docker compose up -d --build
```

Open:

```text
http://localhost:8080
```

To use a different local host port, edit `APP_PORT` in `.env`:

```env
APP_PORT=8501
```

Then restart:

```bash
docker compose up -d --build
```

Open:

```text
http://localhost:8501
```

Stop the app:

```bash
docker compose down
```

## Notes

- Do not commit real API keys.
- Keep `.env` local to your machine.
- Secret fields in the UI use password inputs.
