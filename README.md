# F5 Secure Chatbot

Streamlit chatbot for testing F5 Guardrail with OpenAI or Ollama. Users can type a prompt and attach a PDF or DOCX from the same chat input.

## Clone

```bash
git clone https://github.com/yalmashad/f5-chatbot.git
cd f5-chatbot
```

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit requests python-dotenv openai pypdf python-docx
```

## Configure

Create a `.env` file:

```env
MODEL_PROVIDER=OpenAI
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o-mini

GUARDRAIL_API_KEY=your-f5-guardrail-key
GUARDRAIL_HOSTNAME=https://www.us1.calypsoai.app

OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2
```

Use `MODEL_PROVIDER=Ollama` only if Ollama is running locally.

## Run

```bash
streamlit run f5_chatbot.py
```

## Document Uploads

- Supported: PDF and DOCX
- Maximum file size: 10 MB
- Maximum extracted text: 100,000 characters
- Scanned PDFs that require OCR are not supported

The app extracts document text locally, sends the combined prompt and document text to F5 Guardrail, then sends document context to the model only after inspection clears.
