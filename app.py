"""
Amershop — Asistente IA Corporativo
Aplicación principal Streamlit.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_project_root / ".env", override=True)

import streamlit as st

st.set_page_config(
    page_title="Amershop — Asistente IA",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config import GROQ_API_KEY, DOCUMENTS_DIR, GOOGLE_CLIENT_ID
import streamlit.components.v1 as components
from vectorstore.chroma_store import VectorStoreManager
from agents.rag_agent import RAGAgent

# ============================================================
# CONSTANTES
# ============================================================
LOGO_PATH = os.path.join(_project_root, "assets", "logo.jpg")

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

        /* Input de chat e inputs de formulario */
        [data-testid="stChatInput"] {
            background: transparent !important;
        }
        [data-testid="stChatInput"] > div, div[data-baseweb="input"] {
            border: 1px solid rgba(138, 43, 226, 0.6) !important;
            border-radius: 12px !important;
            background: rgba(15, 12, 28, 0.85) !important;
            color: white !important;
        }

        /* Tarjeta de Login Glassmorphism */
        .login-card {
            background: rgba(15, 12, 28, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(138, 43, 226, 0.3);
            border-radius: 20px;
            padding: 35px 28px;
            box-shadow: 0 0 40px rgba(138, 43, 226, 0.25);
            text-align: center;
            margin-bottom: 25px;
        }

        /* Avatar de Usuario en Sidebar */
        .user-profile-badge {
            background: rgba(138, 43, 226, 0.15);
            border: 1px solid rgba(138, 43, 226, 0.3);
            border-radius: 12px;
            padding: 14px;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Cartel LED Animado "ACTIVO LAS 24 HORAS" */
        @keyframes pulse-green {
            0% {
                box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.8);
                transform: scale(0.95);
            }
            70% {
                box-shadow: 0 0 0 12px rgba(0, 255, 136, 0);
                transform: scale(1.05);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(0, 255, 136, 0);
                transform: scale(0.95);
            }
        }

        .led-banner {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            background: rgba(12, 8, 25, 0.85);
            border: 1px solid rgba(138, 43, 226, 0.6);
            border-radius: 20px;
            padding: 14px 22px;
            margin: 15px 0 25px 0;
            box-shadow: 0 0 25px rgba(138, 43, 226, 0.35), inset 0 0 15px rgba(138, 43, 226, 0.2);
            backdrop-filter: blur(12px);
        }

        .led-dot {
            width: 12px;
            height: 12px;
            background-color: #00ff88;
            border-radius: 50%;
            display: inline-block;
            animation: pulse-green 1.8s infinite;
            box-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88;
        }

        .led-text {
            color: #ffffff;
            font-weight: 700;
            font-size: 15px;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            text-shadow: 0 0 8px rgba(179, 136, 255, 0.9), 0 0 18px rgba(138, 43, 226, 0.7);
        }

        .led-subtext {
            color: #b0b0e0;
            font-size: 13px;
            font-weight: 400;
            letter-spacing: 0.5px;
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
            "<h1 style='text-align:center; color:#b388ff; margin-bottom:15px;'>Amershop</h1>",
            unsafe_allow_html=True,
        )

        # Mostrar Badge de Perfil si está autenticado
        if st.session_state.get("authenticated", False):
            user_name = st.session_state.get("user_name", "Usuario")
            user_email = st.session_state.get("user_email", "")
            auth_type = st.session_state.get("auth_type", "Invitado")

            st.markdown(f"""
                <div class="user-profile-badge">
                    <div style="font-size: 24px; margin-bottom: 5px;">👤</div>
                    <div style="font-weight: 600; color: #ffffff;">{user_name}</div>
                    <div style="font-size: 12px; color: #b388ff;">{user_email if user_email else auth_type}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("### Acciones Rápidas")
        if st.button("✨ Nuevo Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()

        if st.session_state.get("authenticated", False):
            st.markdown("---")
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                st.session_state["authenticated"] = False
                st.session_state["user_name"] = None
                st.session_state["user_email"] = None
                st.session_state["messages"] = []
                st.rerun()

# ============================================================
# LOGIN SCREEN
# ============================================================
def render_login():
    """Renderiza la interfaz de inicio de sesión elegante."""
    inject_custom_css()

    col1, col2, col3 = st.columns([1, 2.2, 1])

    with col2:
        # Centrar el logo usando columnas internas
        img_col1, img_col2, img_col3 = st.columns([1, 1.2, 1])
        with img_col2:
            if os.path.exists(LOGO_PATH):
                st.image(LOGO_PATH, width=140)

        st.markdown("""
            <div style="text-align: center; margin-top: 10px; margin-bottom: 15px;">
                <h1 style="color: #b388ff; font-weight: 600; margin-bottom: 5px; font-size: 32px;">Bienvenido a Amershop</h1>
                <p style="color: #a0a0c0; font-size: 14px; margin-top: 0; margin-bottom: 15px;">Inicia sesión para acceder al asistente virtual corporativo</p>
            </div>
        """, unsafe_allow_html=True)

        # Cartel LED "ACTIVO LAS 24 HORAS" en la pantalla de inicio de sesión
        st.markdown("""
            <div class="led-banner">
                <span class="led-dot"></span>
                <span class="led-text">ACTIVO LAS 24 HORAS</span>
                <span class="led-subtext">• ATENCIÓN Y SOPORTE CONTINUO 24/7</span>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            # Formulario Estándar Email/Password
            with st.form("login_form", clear_on_submit=False):
                email = st.text_input("Correo Electrónico", placeholder="usuario@amershop.com")
                password = st.text_input("Contraseña", type="password", placeholder="••••••••")

                submitted = st.form_submit_button("Iniciar Sesión con Correo", use_container_width=True)

                if submitted:
                    if email and password:
                        st.session_state["authenticated"] = True
                        st.session_state["user_name"] = email.split("@")[0].capitalize()
                        st.session_state["user_email"] = email
                        st.session_state["auth_type"] = "Cuenta Corporativa"
                        st.success(f"¡Bienvenido, {st.session_state['user_name']}!")
                        st.rerun()
                    else:
                        st.error("Por favor ingresa tu correo y contraseña.")

            st.markdown("""
                <div style='text-align: center; margin: 15px 0 10px 0; color: #8080a0; font-size: 13px; font-weight: 500;'>
                    — O —
                </div>
            """, unsafe_allow_html=True)

            if st.button("👤 Acceder como Invitado", key="btn_guest_login", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["user_name"] = "Invitado"
                st.session_state["user_email"] = ""
                st.session_state["auth_type"] = "Acceso Invitado"
                st.rerun()

            st.markdown("""
                <div style='text-align: center; margin: 25px 0 15px 0; color: #a0a0d0; font-size: 13px; font-weight: 500;'>
                    — O AUTENTÍCATE CON GOOGLE (GIS) —
                </div>
            """, unsafe_allow_html=True)

            # Componente Oficial Google Identity Services (GIS) al final de todo
            gis_id = GOOGLE_CLIENT_ID if GOOGLE_CLIENT_ID else "demo-client-id.apps.googleusercontent.com"

            components.html(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <script src="https://accounts.google.com/gsi/client" async defer></script>
                    <style>
                        body {{
                            margin: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            background: transparent;
                        }}
                    </style>
                </head>
                <body>
                    <script>
                        function handleCredentialResponse(response) {{
                            try {{
                                var base64Url = response.credential.split('.')[1];
                                var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                                var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {{
                                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                                }}).join(''));
                                var data = JSON.parse(jsonPayload);
                                
                                window.parent.location.href = window.parent.location.pathname + 
                                    "?gis_login=1&email=" + encodeURIComponent(data.email) + 
                                    "&name=" + encodeURIComponent(data.name || data.email.split('@')[0]);
                            }} catch(e) {{
                                console.error("Error al procesar respuesta GIS:", e);
                            }}
                        }}
                    </script>

                    <div id="g_id_onload"
                        data-client_id="{gis_id}"
                        data-context="signin"
                        data-ux_mode="popup"
                        data-callback="handleCredentialResponse"
                        data-auto_select="false">
                    </div>

                    <div class="g_id_signin"
                        data-type="standard"
                        data-shape="pill"
                        data-theme="filled_black"
                        data-text="signin_with"
                        data-size="large"
                        data-logo_alignment="left">
                    </div>
                </body>
                </html>
            """, height=55)


# ============================================================
# MAIN
# ============================================================
def main():
    if not GROQ_API_KEY:
        st.error("⚠️ API Key de Groq no configurada en el archivo .env")
        st.stop()

    # Procesar Callback de Google Identity Services (GIS) vía Query Params
    query_params = st.query_params
    if "gis_login" in query_params:
        email = query_params.get("email", "usuario@gmail.com")
        name = query_params.get("name", email.split("@")[0].capitalize())
        st.session_state["authenticated"] = True
        st.session_state["user_name"] = name
        st.session_state["user_email"] = email
        st.session_state["auth_type"] = "Google Identity Services (GIS)"
        st.query_params.clear()
        st.rerun()

    # Inicializar estado de autenticación
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Si no está autenticado, mostrar pantalla de Login
    if not st.session_state["authenticated"]:
        render_login()
        return

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
        # Cartel LED "ACTIVO LAS 24 HORAS" estilo Neón
        st.markdown("""
            <div class="led-banner">
                <span class="led-dot"></span>
                <span class="led-text">ACTIVO LAS 24 HORAS</span>
                <span class="led-subtext">• ATENCIÓN Y SOPORTE CONTINUO 24/7</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<p style='color: #b388ff; font-weight: 500; margin-bottom: 12px;'>💡 Preguntas frecuentes sugeridas:</p>", unsafe_allow_html=True)

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
