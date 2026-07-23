"""
AmershOp — Asistente IA Corporativo
Aplicación principal Streamlit, versión funcional.
"""

# Cargar .env ANTES de cualquier otra importación
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
)

from config import GROQ_API_KEY, DOCUMENTS_DIR
from vectorstore.chroma_store import VectorStoreManager
from agents.rag_agent import RAGAgent

# ============================================================
# INICIALIZACIÓN DE COMPONENTES
# ============================================================
@st.cache_resource
def init_vector_store():
    """Inicializa el vector store (singleton)."""
    return VectorStoreManager()


@st.cache_resource
def init_rag_agent(_vector_store):
    """Inicializa el agente RAG (singleton)."""
    return RAGAgent(vector_store_manager=_vector_store)


def ensure_documents_indexed(vector_store: VectorStoreManager):
    """Verifica que los documentos estén indexados; si no, los indexa silenciosamente."""
    if vector_store.get_document_count() == 0:
        docs_path = Path(DOCUMENTS_DIR)
        if docs_path.exists() and any(docs_path.iterdir()):
            vector_store.reindex_from_directory(str(docs_path))

# ============================================================
# ESTILOS VISUALES PREMIUM
# ============================================================
def inject_custom_css():
    st.markdown("""
        <style>
        /* Importar fuente moderna */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
        
        html, body, [class*="st-"] {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Prevenir que la fuente reemplace los iconos de Material */
        .material-symbols-rounded, .material-icons {
            font-family: 'Material Symbols Rounded' !important;
        }

        /* Fondo principal con gradiente oscuro dinámico */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 15% 50%, #100b21, #08050e 40%, #000000 100%);
            color: #ffffff;
        }

        /* Barra lateral con Glassmorphism */
        [data-testid="stSidebar"] {
            background: rgba(15, 15, 30, 0.4) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-right: 1px solid rgba(138, 43, 226, 0.2);
        }

        /* Ocultar botones nativos (Stop, Deploy, Menu) para una apariencia más limpia */
        .stDeployButton {display:none;}
        [data-testid="stHeader"] { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        [data-testid="stStatusWidget"] { display: none !important; }
        
        /* Ocultar el botón de ampliar imagen (fullscreen) */
        button[title="View fullscreen"] {
            display: none !important;
        }

        /* Estilo premium limpio para botones (menos "IA", más corporativo) */
        .stButton>button {
            background-color: #1e1e2e;
            color: #e0e0e0;
            border: 1px solid #3a3a5a;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 500;
            letter-spacing: 0.3px;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #2a2a40;
            border-color: #5a5a8a;
            color: white;
            transform: translateY(-1px);
        }

        /* Burbujas de chat premium */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Input de chat brillante */
        [data-testid="stChatInput"] {
            border: 1px solid rgba(138, 43, 226, 0.3) !important;
            border-radius: 20px !important;
            background: rgba(10, 10, 20, 0.8) !important;
            box-shadow: 0 0 15px rgba(138, 43, 226, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    """Renderiza la barra lateral limpia sin estadísticas."""
    with st.sidebar:
        # Logo generado
        logo_path = r"C:\Users\amer\.gemini\antigravity\brain\3c18fde8-32f9-4d64-98e7-349552d1dcb2\dragon_logo_1784779205766.jpg"
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
            
        st.markdown("<h1 style='text-align: center; color: #b388ff; margin-bottom: 30px;'>AmershOp IA</h1>", unsafe_allow_html=True)
        
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

    st.header("Asistente IA Corporativo")
    st.write("Pregunta sobre las políticas, envíos o productos de AmershOp.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    # Inicializar variable para capturar un prompt de los botones de sugerencia
    suggestion_prompt = None

    if not st.session_state["messages"]:
        st.info("💡 Sugerencias de preguntas:")
        suggestions = [
            "¿Cuál es la política de devoluciones?",
            "¿Cuánto cuesta el envío express?",
            "¿En qué moneda están los precios?",
            "¿Tienen envío gratuito?",
        ]
        
        cols = st.columns(2)
        for i, suggestion in enumerate(suggestions):
            if cols[i % 2].button(suggestion, key=f"sug_{i}"):
                suggestion_prompt = suggestion

    # Renderizar historial de mensajes
    for message in st.session_state["messages"]:
        avatar_icon = "🐉" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Fuentes"):
                    for src in message["sources"]:
                        st.write(f"- {src}")

    # Obtener el prompt ya sea del input normal o de un botón de sugerencia
    user_input = st.chat_input("Escribe tu pregunta...")
    prompt = suggestion_prompt or user_input

    if prompt:
        # Mostrar el mensaje del usuario de inmediato
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Generar respuesta
        with st.chat_message("assistant", avatar="🐉"):
            with st.spinner("Buscando respuesta..."):
                try:
                    # Formatear el historial para LangChain: [("human", "msg"), ("ai", "msg")]
                    chat_history = []
                    for m in st.session_state["messages"][:-1]:
                        role = "human" if m["role"] == "user" else "ai"
                        chat_history.append((role, m["content"]))
                    chat_history = chat_history[-10:]

                    result = agent.query(question=prompt, chat_history=chat_history)
                    
                    answer = result.get("answer", "Error al generar respuesta.")
                    sources = result.get("sources", [])

                    st.markdown(answer)
                    if sources:
                        with st.expander("Fuentes"):
                            for src in sources:
                                st.write(f"- {src}")

                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
