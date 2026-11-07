# AI Blog Generator

A Streamlit app that generates structured, multilingual blog posts using the
Groq API and a LangGraph workflow.

## Requirements

- Python 3.10 or newer
- A Groq API key

## Setup

1. Create and activate a virtual environment.
2. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set `GROQ_API_KEY` to your own key.
   The default model is `qwen/qwen3.8-27b`; override it with `GROQ_MODEL` if
   needed.
4. Start the app:

   ```powershell
   streamlit run app.py
   ```

## Architecture

- `app.py` provides the Streamlit interface, progress and error feedback, and
  the Markdown download.
- `graph/workflow.py` runs a LangGraph workflow with request preparation,
  conditional input routing, LLM generation, and output validation.
- `agents/blog_writer.py` calls the configured Groq chat completion API.
- `prompts/blog_prompt.py` defines the multilingual blog structure.
- `config/settings.py` loads API settings from environment variables or `.env`.

Never commit `.env` or put API keys in source code.
