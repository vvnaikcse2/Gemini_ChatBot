# ✨ Gemini Chatbot — Streamlit

A streaming chatbot built with Google's Gemini API and Streamlit, ready to deploy on Streamlit Community Cloud.

## Features
- 🔄 Streaming responses (tokens appear as they're generated)
- 🧠 Full conversation history sent on every turn
- 🎛️ Sidebar controls: model selector, system prompt, max tokens, temperature, clear chat
- 🎨 Dark theme

---

## Local development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your API key
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "AIza..."' > .streamlit/secrets.toml

# 3. Run
streamlit run app.py
```

Get a free Gemini API key at https://aistudio.google.com/app/apikey

---

## Deploy to Streamlit Community Cloud

1. Push this folder as the root of a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select repo, branch, set **Main file path** to `app.py`.
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "AIza-your-real-key"
   ```
5. Click **Deploy** — done!

> ⚠️ Never commit `.streamlit/secrets.toml`. It's already in `.gitignore`.

---

## Project structure

```
chatbot/
├── app.py                        # Streamlit app
├── requirements.txt              # google-generativeai + streamlit
├── .gitignore
└── .streamlit/
    ├── config.toml               # Theme & server settings
    └── secrets.toml.example      # Key template (safe to commit)
```
