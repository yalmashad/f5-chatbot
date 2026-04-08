# F5 Secure Chatbot

A Streamlit-based chatbot UI that supports:

- OpenAI models
- Local LLMs through Ollama
- F5 Guardrail protection in `Inline` or `Out-of-band` mode
- Managing API keys and model settings directly from the UI
- Saving configuration to `.env`

## Features

- Switch between `OpenAI` and `Ollama` from the Settings panel
- Show only the settings relevant to the selected provider
- Choose an OpenAI model from a list of common models or enter one manually
- Load local Ollama models into a dropdown when Ollama is available
- Enter and save `OPENAI_API_KEY` in the UI
- Enter and save `F5AI_API_KEY` in the UI as `F5 Guardrail API key`
- Load values from `.env` automatically on startup
- Clear chat history from the sidebar
- Optional debug output for guardrail responses

## How It Works

The app supports three chat flows:

1. `Guardrail disabled`
   The app sends prompts directly to the selected model provider:
   - OpenAI
   - Ollama

2. `Inline`
   The app sends the prompt to the F5 Guardrail Prompt API and returns its response directly.

   In this mode, model settings are disabled in the UI because they do not affect the response.

3. `Out-of-band`
   The app scans the user prompt with the F5 Guardrail Scan API, sends the prompt to the selected model provider, then scans the model response before displaying it.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) installed locally if you want to use local models
- An OpenAI API key if you want to use OpenAI
- An F5 Guardrail API key if you want to use `Inline` or `Out-of-band`

## Install

```bash
pip install streamlit requests python-dotenv openai
```

## Run

```bash
streamlit run f5_chatbot.py
```

## Configuration

The application reads configuration from `.env` and can also update it from the sidebar Settings form.

Example `.env`:

```env
MODEL_PROVIDER=OpenAI
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o-mini

OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2

F5AI_API_KEY=your-f5-guardrail-key

CALYPSO_SCAN_URL=https://www.us1.calypsoai.app/backend/v1/scans
CALYPSO_PROMPT_API_URL=https://www.us1.calypsoai.app/backend/v1/prompts
```

## Using OpenAI

1. Open the app.
2. In `Settings`, choose `OpenAI` as the model provider.
3. Choose a common OpenAI model from the dropdown, or select `Custom...` and enter one manually.
4. Enter your `OpenAI API key`.
5. Click `Save settings`.

If Guardrail is disabled or set to `Out-of-band`, the app will use OpenAI for chat responses.

## Using Ollama

1. Start Ollama locally.
2. Make sure the Ollama API is available, usually at `http://localhost:11434/v1`.
3. Pull a model if needed, for example:

```bash
ollama pull llama3.2
```

4. Open the app.
5. In `Settings`, choose `Ollama` as the model provider.
6. Confirm the Ollama base URL.
7. Choose one of the detected local Ollama models from the dropdown, or enter one manually if needed.
8. Click `Save settings`.

If Guardrail is disabled or set to `Out-of-band`, the app will use Ollama for chat responses.

## Guardrail Modes

### Inline

- Uses the F5 Guardrail Prompt API directly
- Requires `F5AI_API_KEY`
- Does not use the selected OpenAI or Ollama model for the response

### Out-of-band

- Scans the prompt before model execution
- Sends the prompt to OpenAI or Ollama
- Scans the model response before showing it
- Requires `F5AI_API_KEY`

### Disabled

- Sends prompts directly to OpenAI or Ollama
- Does not call the F5 Guardrail APIs

## Secrets and UI Behavior

- Secret inputs use password fields
- Settings saved in the UI are written back to `.env`
- Manual edits to `.env` are loaded on the next rerun

## Notes

- The app currently stores settings in a local `.env` file for convenience.
- If you plan to publish this repository, do not commit real API keys.
