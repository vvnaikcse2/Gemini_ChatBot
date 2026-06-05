import streamlit as st
import google.generativeai as genai

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="✨",
    layout="centered",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .stChatMessage { border-radius: 12px; }
    .stChatInputContainer { padding-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("✨ Gemini Chatbot")
st.caption("Powered by Google · gemini-1.5-flash")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    model_choice = st.selectbox(
        "Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
        index=0,
    )

    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful, friendly, and concise assistant.",
        height=120,
    )

    max_tokens = st.slider("Max output tokens", 256, 8192, 1024, step=128)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, step=0.05)

    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown(
        "**Setup:** add your `GEMINI_API_KEY` to "
        "[Streamlit secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)."
    )

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render history ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask me anything…"):

    # Check for API key
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error(
            "⚠️ **API key missing.** "
            "Add `GEMINI_API_KEY` to your Streamlit secrets and redeploy."
        )
        st.stop()

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Configure Gemini
    genai.configure(api_key=api_key)

    # system_instruction must be a Content-like dict with explicit text parts
    # (bare strings are rejected by the gRPC layer on newer SDK versions)
    system_instruction = {
        "role": "system",
        "parts": [{"text": system_prompt.strip() or "You are a helpful assistant."}],
    }

    model = genai.GenerativeModel(
        model_name=model_choice,
        system_instruction=system_instruction,
        generation_config=genai.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        ),
    )

    # Build Gemini history (all turns except the latest user prompt).
    # Parts must be explicit {"text": "..."} dicts — bare strings cause
    # serialisation errors over gRPC.
    gemini_history = []
    for msg in st.session_state.messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [{"text": msg["content"]}]})

    # Stream assistant reply
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""

        chat = model.start_chat(history=gemini_history)
        response_stream = chat.send_message(
            {"role": "user", "parts": [{"text": prompt}]},
            stream=True,
        )

        for chunk in response_stream:
            if chunk.text:
                full_reply += chunk.text
                placeholder.markdown(full_reply + "▌")

        placeholder.markdown(full_reply)

    st.session_state.messages.append({"role": "assistant", "content": full_reply})
