"""
AmershOp — Asistente IA Corporativo
Aplicación principal Streamlit.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_project_root / ".env", override=True)

import streamlit as st

st.set_page_config(
    page_title="AmershOp — Asistente IA",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config import GROQ_API_KEY, DOCUMENTS_DIR
from vectorstore.chroma_store import VectorStoreManager
from agents.rag_agent import RAGAgent

# ============================================================
# CONSTANTES
# ============================================================
LOGO_PATH = os.path.join(_project_root, "assets", "logo.jpg")
# Fallback al logo generado si no existe en assets/
if not os.path.exists(LOGO_PATH):
    LOGO_PATH = r"C:\Users\amer\.gemini\antigravity\brain\3c18fde8-32f9-4d64-98e7-349552d1dcb2\dragon_logo_1784779205766.jpg"

# ============================================================
# INICIALIZACIÓN (cached)
# ============================================================
@st.cache_resource
def init_vector_store():
    return VectorStoreManager()

@st.cache_resource
def init_rag_agent(_vector_store):
    return RAGAgent(vector_store_manager=_vector_store)

def ensure_documents_indexed(vs: VectorStoreManager):
    if vs.get_document_count() == 0:
        docs_path = Path(DOCUMENTS_DIR)
        if docs_path.exists() and any(docs_path.iterdir()):
            vs.reindex_from_directory(str(docs_path))

# ============================================================
# ESTILOS CSS — Limpio y sin hacks
# ============================================================
def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap');

        /* Fuente elegante solo en textos */
        .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, label,
        div[data-testid="stMarkdownContainer"] {
            font-family: 'Outfit', sans-serif !important;
        }

        /* Fondo galaxia */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 10% 20%, #0d081c 0%, #06040b 50%, #000000 100%);
            color: #f0f0f5;
        }

        /* Header glassmorphism que combina con todo */
        [data-testid="stHeader"] {
            background: rgba(12, 9, 25, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid rgba(138, 43, 226, 0.2) !important;
        }

        /* Sidebar glassmorphism */
        [data-testid="stSidebar"] {
            background: rgba(12, 9, 25, 0.5) !important;
            backdrop-filter: blur(16px);
            border-right: 1px solid rgba(138, 43, 226, 0.15);
        }

        /* Botones elegantes */
        .stButton>button {
            background: linear-gradient(145deg, #1a1a2e, #12121e);
            color: #d1d1e0;
            border: 1px solid rgba(138, 43, 226, 0.3);
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(145deg, #252542, #181829);
            border-color: rgba(138, 43, 226, 0.6);
            color: white;
            transform: translateY(-2px);
        }

        /* Burbujas de chat */
        [data-testid="stChatMessage"] {
            background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
            border: 1px solid rgba(138, 43, 226, 0.1);
        }

        /* Input de chat */
        [data-testid="stChatInput"] {
            background: transparent !important;
        }
        [data-testid="stChatInput"] > div {
            border: 1px solid rgba(138, 43, 226, 0.6) !important;
            border-radius: 20px !important;
            background: rgba(15, 12, 28, 0.85) !important;
            padding: 2px 10px;
            box-shadow: 0 0 20px rgba(138, 43, 226, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=280)
        st.markdown(
            "<h1 style='text-align:center; color:#b388ff; margin-bottom:30px;'>AmershOp</h1>",
            unsafe_allow_html=True,
        )
        st.markdown("### Acciones Rápidas")
        if st.button("✨ Nuevo Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()

# ============================================================
# MAIN
# ============================================================
def main():
    if not GROQ_API_KEY:
        st.error("⚠️ API Key de Groq no configurada en el archivo .env")
        st.stop()

    try:
        vector_store = init_vector_store()
        agent = init_rag_agent(vector_store)
    except Exception as e:
        st.error(f"Error al inicializar componentes: {e}")
        st.stop()

    inject_custom_css()
    ensure_documents_indexed(vector_store)
    render_sidebar()

    st.header("¿En qué podemos ayudarte hoy?")
    st.write("Resuelve tus dudas sobre productos, envíos, devoluciones y más.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    suggestion_prompt = None
    if not st.session_state["messages"]:
        st.info("💡 Preguntas frecuentes:")
        suggestions = [
            "¿Cuál es la política de devoluciones?",
            "¿Cuánto cuesta el envío express?",
            "¿En qué moneda están los precios?",
            "¿Tienen envío gratuito?",
            "¿Cuánto tarda en llegar mi pedido?",
            "¿Qué hago si mi producto llegó dañado?",
            "¿Qué métodos de pago aceptan?",
            "¿Puedo rastrear mi pedido?",
        ]
        cols = st.columns(2)
        for i, s in enumerate(suggestions):
            if cols[i % 2].button(s, key=f"sug_{i}"):
                suggestion_prompt = s

    # Renderizar historial
    avatar_logo = LOGO_PATH if os.path.exists(LOGO_PATH) else "🐉"
    for msg in st.session_state["messages"]:
        av = avatar_logo if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=av):
            st.markdown(msg["content"])

    # Input del usuario
    user_input = st.chat_input("Escribe tu pregunta...")
    prompt = suggestion_prompt or user_input

    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=avatar_logo):
            with st.spinner("✨ Preparando tu respuesta..."):
                try:
                    chat_history = [
                        ("human" if m["role"] == "user" else "ai", m["content"])
                        for m in st.session_state["messages"][:-1]
                    ][-10:]

                    result = agent.query(question=prompt, chat_history=chat_history)
                    answer = result.get("answer", "Error al generar respuesta.")

                    st.markdown(answer)
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": answer,
                    })
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
