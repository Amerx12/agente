# 🛒 Amershop — Asistente IA Corporativo

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=for-the-badge&logo=groq&logoColor=white)
![Oracle_Cloud](https://img.shields.io/badge/Oracle_Cloud-OCI-F80000?style=for-the-badge&logo=oracle&logoColor=white)

**Asistente virtual inteligente de atención y consulta corporativa para la tienda de tecnología Amershop.**

</div>

---

## 🎯 Descripción

**Amershop** es un sistema de asistencia inteligente basado en arquitectura **RAG (Retrieval-Augmented Generation)**. Permite a colaboradores y clientes consultar políticas, guías de envío, reembolsos y catálogo de productos en lenguaje natural con respuestas instantáneas y precisas.

---

## ✨ Características Principales

- 🤖 **Motor IA Ultra-Rápido:** Desarrollado con **Groq (LLaMA 3.1 8B Instant)** y embeddings de HuggingFace.
- 🔐 **Autenticación Multi-Opción:**
  - **Google Identity Services (GIS):** Integración con el SDK oficial de inicio de sesión con Google.
  - **Acceso Corporativo:** Inicio de sesión con correo y contraseña.
  - **Acceso Invitado:** Pruebas directas de la plataforma.
- 🚨 **Cartel LED 24/7 Animado:** Indicador visual de disponibilidad continua en tiempo real.
- 🎨 **Diseño Galaxia Glassmorphism:** Tema oscuro premium, bordes redondeados y efectos neón traslúcidos.
- 📄 **Multiformato RAG:** Indexación automática de archivos PDF, DOCX, XLSX, PPTX, MD, CSV, JSON y HTML.

---

## 📁 Estructura del Proyecto

```
agente/
├── .streamlit/           # Configuración del servidor Streamlit (config.toml)
├── agents/               # Agentes de IA y evaluador de relevancia
│   ├── document_grader.py
│   └── rag_agent.py
├── assets/               # Recursos gráficos (logo.jpg)
├── documents/            # Base de conocimiento (Políticas, FAQ, Guías)
├── loaders/              # Cargadores multiformato de archivos
├── vectorstore/          # Base de datos vectorial (FAISS / ChromaDB)
├── .env.example          # Plantilla de variables de entorno
├── app.py                # Aplicación principal de Streamlit
├── config.py             # Configuración centralizada
└── requirements.txt      # Dependencias de Python
```

---

## 🚀 Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/TU_USUARIO/agente.git
   cd agente
   ```

2. **Crear entorno virtual e instalar dependencias:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configurar el archivo `.env`:**
   Copia el archivo `.env.example` a `.env` e ingresa tu API Key de Groq:
   ```env
   GROQ_API_KEY=tu_api_key_de_groq
   GOOGLE_CLIENT_ID=tu_client_id_opcional
   ```

4. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```
   Abre [http://localhost:8501](http://localhost:8501) en tu navegador.

---

## ☁️ Despliegue en Oracle Cloud (OCI Always Free)

1. **Crear una Instancia en Oracle Cloud:**
   - SO: Ubuntu 22.04 LTS
   - Shape: `VM.Standard.E2.1.Micro` o `VM.Standard.A1.Flex` (Gratis siempre).

2. **Abrir el Puerto 8501:**
   - En las reglas de entrada de tu VCN en Oracle Cloud, permite tráfico TCP en el puerto `8501`.
   - En la consola de la VM (Ubuntu):
     ```bash
     sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8501 -j ACCEPT
     sudo netfilter-persistent save
     ```

3. **Instalar y Ejecutar en la VM:**
   ```bash
   sudo apt update && sudo apt install python3-pip git -y
   git clone https://github.com/TU_USUARIO/agente.git
   cd agente
   pip3 install -r requirements.txt
   nano .env # (Agrega tu GROQ_API_KEY)

   nohup python3 -m streamlit run app.py --server.port 8501 --server.headless true &
   ```

---

## 🛡️ Licencia
Desarrollado para **Amershop**. Todos los derechos reservados.
