"""
AmershOp — Asistente IA Corporativo
Aplicación principal Streamlit con autenticación, tema oscuro y chat conversacional.
"""

# Cargar .env ANTES de cualquier otra importación
import os
from pathlib import Path
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_project_root / ".env", override=True)

import streamlit as st
import time

# Configurar la página ANTES de cualquier otro comando de Streamlit
st.set_page_config(
    page_title="AmershOp — Asistente IA",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config import (
    STORE_NAME, APP_TITLE, APP_DESCRIPTION, GOOGLE_API_KEY,
    DOCUMENTS_DIR, AUTH_USERS, SYSTEM_PROMPT
)
from vectorstore.chroma_store import VectorStoreManager
from agents.rag_agent import RAGAgent
from loaders.multi_loader import load_all_documents, SUPPORTED_EXTENSIONS


# ============================================================
# CSS PERSONALIZADO - Tema oscuro premium
# ============================================================
def inject_custom_css():
    """Inyecta estilos CSS personalizados para un look premium."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* === TEMA GENERAL === */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* === PANTALLA DE LOGIN === */
    .login-container {
        max-width: 420px;
        margin: 8vh auto;
        padding: 3rem 2.5rem;
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 25px 60px rgba(0,0,0,0.5), 0 0 40px rgba(83, 92, 236, 0.1);
    }

    .login-logo {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .login-title {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }

    .login-subtitle {
        text-align: center;
        color: #8892b0;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* === HEADER === */
    .app-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .app-header h1 {
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .app-header p {
        color: #8892b0;
        font-size: 0.85rem;
        margin: 0.3rem 0 0 0;
    }

    /* === SIDEBAR === */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #ccd6f6;
    }

    /* === STAT CARDS === */
    .stat-card {
        background: linear-gradient(145deg, #1e1e3f, #2a2a5a);
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.8rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }

    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* === CHAT MESSAGES === */
    .stChatMessage {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        margin-bottom: 0.5rem !important;
    }

    /* === SOURCES EXPANDER === */
    .source-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea22, #764ba222);
        color: #a8b2d1;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 0.15rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    /* === WELCOME CARD === */
    .welcome-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }

    .welcome-card h2 {
        background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .welcome-card p {
        color: #8892b0;
        font-size: 0.9rem;
    }

    /* === SUGGESTION CHIPS === */
    .suggestion-chip {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #a8b2d1;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.3rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .suggestion-chip:hover {
        background: rgba(102, 126, 234, 0.25);
        border-color: rgba(102, 126, 234, 0.4);
    }

    /* === ANIMACIÓN DE TYPING === */
    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }

    .typing-indicator span {
        animation: pulse 1.4s infinite;
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        margin: 0 2px;
    }

    .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

    /* === BOTONES === */
    .stButton > button {
        border-radius: 12px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    /* === FOOTER === */
    .app-footer {
        text-align: center;
        color: #4a5568;
        font-size: 0.7rem;
        padding: 1rem;
        margin-top: 2rem;
    }

    /* Ocultar hamburguesa y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# AUTENTICACIÓN
# ============================================================
def show_login_page():
    """Muestra la página de inicio de sesión con Google OAuth y usuario/contraseña."""
    st.markdown("""
    <div class="login-container">
        <div class="login-logo">🛒</div>
        <div class="login-title">AmershOp</div>
        <div class="login-subtitle">Asistente IA Corporativo</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("####")

        # --- Opción 1: Login con Google ---
        google_client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")

        if google_client_id and google_client_secret:
            try:
                from streamlit_google_auth import Authenticate

                auth = Authenticate(
                    secret_credentials_path="",
                    cookie_name="amershop_auth",
                    cookie_key="amershop_secret_key_123",
                    redirect_uri="http://localhost:8501",
                    client_id=google_client_id,
                    client_secret=google_client_secret,
                )

                auth.check_authentification()

                if st.session_state.get("connected"):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = st.session_state.get("user_info", {}).get("name", "Google User")
                    st.session_state["user_email"] = st.session_state.get("user_info", {}).get("email", "")
                    st.rerun()

                auth.login()
            except Exception as e:
                st.warning(f"⚠️ Google OAuth no disponible: {str(e)[:80]}")

            st.markdown("""
            <div style="text-align: center; margin: 1.5rem 0; color: #8892b0;">
                <span>─── o inicia con usuario ───</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <p style="color: #8892b0; font-size: 0.75rem;">
                    💡 Para habilitar Google Login, configura GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET en .env
                </p>
            </div>
            """, unsafe_allow_html=True)

        # --- Opción 2: Login con usuario/contraseña ---
        username = st.text_input(
            "👤 Usuario",
            placeholder="Ingresa tu usuario",
            key="login_user"
        )
        password = st.text_input(
            "🔒 Contraseña",
            type="password",
            placeholder="Ingresa tu contraseña",
            key="login_pass"
        )

        if st.button("🚀 Iniciar Sesión", use_container_width=True, type="primary"):
            if username in AUTH_USERS and AUTH_USERS[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem;">
            <p style="color: #8892b0; font-size: 0.75rem;">
                Credenciales de prueba: <code>admin</code> / <code>amershop2024</code>
            </p>
        </div>
        """, unsafe_allow_html=True)


def check_authentication():
    """Verifica si el usuario está autenticado."""
    return st.session_state.get("authenticated", False)


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
    """Verifica que los documentos estén indexados; si no, los indexa."""
    if vector_store.get_document_count() == 0:
        docs_path = Path(DOCUMENTS_DIR)
        if docs_path.exists() and any(docs_path.iterdir()):
            with st.spinner("📚 Indexando documentos por primera vez..."):
                count = vector_store.reindex_from_directory(str(docs_path))
                if count > 0:
                    st.success(f"✅ {count} fragmentos indexados exitosamente")
                else:
                    st.warning("⚠️ No se encontraron documentos para indexar")


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar(vector_store: VectorStoreManager):
    """Renderiza la barra lateral con información y controles."""
    with st.sidebar:
        # Logo y título
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 3rem;">🛒</span>
            <h2 style="background: linear-gradient(135deg, #667eea, #764ba2);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       margin: 0.5rem 0 0 0; font-size: 1.4rem;">AmershOp</h2>
            <p style="color: #8892b0; font-size: 0.8rem; margin: 0;">Asistente IA Corporativo</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Usuario actual
        username = st.session_state.get("username", "Desconocido")
        st.markdown(f"""
        <div class="stat-card">
            <div style="color: #ccd6f6; font-size: 0.9rem;">
                👤 Conectado como: <strong>{username}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Estadísticas
        doc_count = vector_store.get_document_count()
        sources = vector_store.get_indexed_sources()
        chat_count = len(st.session_state.get("messages", []))

        st.markdown("### 📊 Estadísticas")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{doc_count}</div>
                <div class="stat-label">Fragmentos</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(sources)}</div>
                <div class="stat-label">Documentos</div>
            </div>
            """, unsafe_allow_html=True)

        # Lista de documentos indexados
        if sources:
            with st.expander("📁 Documentos indexados", expanded=False):
                for src in sorted(sources):
                    ext = Path(src).suffix.lower()
                    icon_map = {
                        ".pdf": "📕", ".docx": "📘", ".xlsx": "📗",
                        ".pptx": "📙", ".md": "📝", ".csv": "📊",
                        ".json": "⚙️", ".html": "🌐"
                    }
                    icon = icon_map.get(ext, "📄")
                    st.markdown(f"- {icon} `{src}`")

        st.divider()

        # Controles
        st.markdown("### ⚙️ Controles")

        if st.button("🔄 Reindexar Documentos", use_container_width=True):
            with st.spinner("📚 Reindexando documentos..."):
                count = vector_store.reindex_from_directory(DOCUMENTS_DIR)
                st.success(f"✅ {count} fragmentos indexados")
                st.rerun()

        if st.button("🗑️ Limpiar Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()

        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # Formatos soportados
        with st.expander("📋 Formatos Soportados", expanded=False):
            formats = [
                ("📕 PDF", ".pdf"), ("📘 Word", ".docx"),
                ("📗 Excel", ".xlsx"), ("📙 PowerPoint", ".pptx"),
                ("📝 Markdown", ".md"), ("📊 CSV", ".csv"),
                ("⚙️ JSON", ".json"), ("🌐 HTML", ".html"),
            ]
            for name, ext in formats:
                st.markdown(f"- {name} (`{ext}`)")

        # Footer
        st.markdown("""
        <div class="app-footer">
            <p>AmershOp IA v1.0</p>
            <p>Powered by Gemini + LangChain</p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# CHAT PRINCIPAL
# ============================================================
def render_chat(agent: RAGAgent):
    """Renderiza la interfaz de chat principal."""
    # Header
    st.markdown("""
    <div class="app-header">
        <h1>🛒 AmershOp — Asistente IA Corporativo</h1>
        <p>Pregunta lo que necesites sobre los documentos internos de la empresa</p>
    </div>
    """, unsafe_allow_html=True)

    # Inicializar historial de mensajes
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Si no hay mensajes, mostrar bienvenida
    if not st.session_state["messages"]:
        username = st.session_state.get("username", "colaborador")
        st.markdown(f"""
        <div class="welcome-card">
            <h2>¡Hola, {username}! 👋</h2>
            <p>Soy el asistente virtual de AmershOp. Puedo ayudarte con información
            sobre políticas, productos, envíos, devoluciones y más.</p>
            <p style="margin-top: 1rem; font-size: 0.85rem;">Prueba con alguna de estas preguntas:</p>
        </div>
        """, unsafe_allow_html=True)

        # Sugerencias de preguntas
        suggestions = [
            "¿Cuál es la política de devoluciones?",
            "¿Cuánto cuesta el envío express?",
            "¿Qué métodos de pago aceptan?",
            "¿Cuántos días tengo para devolver un producto?",
            "¿Cuáles son los horarios de atención?",
            "¿Tienen envío gratuito?",
        ]

        cols = st.columns(3)
        for i, suggestion in enumerate(suggestions):
            with cols[i % 3]:
                if st.button(f"💬 {suggestion}", key=f"sug_{i}", use_container_width=True):
                    st.session_state["messages"].append({
                        "role": "user",
                        "content": suggestion
                    })
                    st.rerun()

    # Mostrar historial de mensajes
    for message in st.session_state["messages"]:
        role = message["role"]
        content = message["content"]
        avatar = "👤" if role == "user" else "🤖"

        with st.chat_message(role, avatar=avatar):
            st.markdown(content)

            # Mostrar fuentes si están disponibles
            if role == "assistant" and "sources" in message and message["sources"]:
                sources_html = " ".join(
                    [f'<span class="source-tag">📄 {src}</span>' for src in message["sources"]]
                )
                with st.expander("📎 Fuentes consultadas", expanded=False):
                    st.markdown(sources_html, unsafe_allow_html=True)

    # Input del chat
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # Agregar mensaje del usuario
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Generar respuesta
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner(""):
                # Indicador de typing
                typing_placeholder = st.empty()
                typing_placeholder.markdown("""
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                    <span style="color: #8892b0; font-size: 0.8rem; margin-left: 8px;">
                        Buscando en documentos...
                    </span>
                </div>
                """, unsafe_allow_html=True)

                try:
                    # Preparar historial para el agente
                    chat_history = [
                        (m["content"], st.session_state["messages"][i+1]["content"])
                        for i, m in enumerate(st.session_state["messages"][:-1])
                        if m["role"] == "user"
                        and i+1 < len(st.session_state["messages"])
                        and st.session_state["messages"][i+1]["role"] == "assistant"
                    ][-5:]  # Últimos 5 intercambios

                    # Consultar al agente
                    result = agent.query(
                        question=prompt,
                        chat_history=chat_history
                    )

                    typing_placeholder.empty()

                    answer = result.get("answer", "Lo siento, ocurrió un error al procesar tu pregunta.")
                    sources = result.get("sources", [])

                    st.markdown(answer)

                    # Mostrar fuentes
                    if sources:
                        sources_html = " ".join(
                            [f'<span class="source-tag">📄 {src}</span>' for src in sources]
                        )
                        with st.expander("📎 Fuentes consultadas", expanded=False):
                            st.markdown(sources_html, unsafe_allow_html=True)

                    # Guardar respuesta en historial
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:
                    typing_placeholder.empty()
                    error_msg = f"❌ Error al procesar la pregunta: {str(e)}"
                    st.error(error_msg)
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": error_msg,
                        "sources": []
                    })


# ============================================================
# MAIN
# ============================================================
def main():
    """Punto de entrada principal de la aplicación."""
    inject_custom_css()

    # Verificar API Key
    if not GOOGLE_API_KEY:
        st.error("""
        ⚠️ **API Key no configurada**

        Para usar el asistente, configura tu API Key de Google Gemini:

        1. Obtén tu API Key gratuita en [Google AI Studio](https://aistudio.google.com/)
        2. Crea un archivo `.env` en la raíz del proyecto
        3. Agrega: `GOOGLE_API_KEY=tu_api_key_aqui`
        4. Reinicia la aplicación
        """)
        st.stop()

    # Verificar autenticación
    if not check_authentication():
        show_login_page()
        return

    # Inicializar componentes
    try:
        vector_store = init_vector_store()
        agent = init_rag_agent(vector_store)
    except Exception as e:
        st.error(f"❌ Error al inicializar componentes: {str(e)}")
        st.info("Verifica que tu GOOGLE_API_KEY sea válida y que las dependencias estén instaladas.")
        st.stop()

    # Indexar documentos si es necesario
    ensure_documents_indexed(vector_store)

    # Renderizar interfaz
    render_sidebar(vector_store)
    render_chat(agent)


if __name__ == "__main__":
    main()
