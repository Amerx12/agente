# 🛒 AmershOp — Agente IA Corporativo

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-2.0_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![OCI](https://img.shields.io/badge/Oracle_Cloud-OCI-F80000?style=for-the-badge&logo=oracle&logoColor=white)

**Asistente virtual inteligente para colaboradores de AmershOp, una tienda online de tecnología.**

Responde preguntas basándose en documentos internos de la empresa, soportando 8 formatos de archivo diferentes.

</div>

---

## 📸 Demo en Producción (OCI)

> *Captura de pantalla del agente ejecutándose en Oracle Cloud Infrastructure:*

<!-- TODO: Reemplazar con la captura real del deploy en OCI -->
<!-- ![AmershOp Agent en OCI](./assets/demo_oci.png) -->

---

## 🎯 Descripción

AmershOp IA es un **agente de inteligencia artificial corporativo** que funciona como una base de conocimiento conversacional, centralizada y siempre disponible. Los colaboradores de la empresa pueden hacer preguntas en lenguaje natural y recibir respuestas precisas basadas en los documentos internos.

### Características principales

- 🤖 **Chat conversacional** con historial y contexto
- 📄 **8 formatos de documentos** soportados (PDF, DOCX, XLSX, PPTX, MD, CSV, JSON, HTML)
- 🔍 **RAG (Retrieval-Augmented Generation)** con búsqueda semántica MMR
- 📎 **Citación de fuentes** en cada respuesta
- 🔐 **Autenticación de usuarios** para control de acceso
- 🎨 **Interfaz premium** con tema oscuro y animaciones
- 🐳 **Containerizado** con Docker para fácil despliegue
- ☁️ **Deploy en OCI** (Oracle Cloud Infrastructure)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                  │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Login   │  │  Chat UI     │  │  Sidebar Stats   │  │
│  │  Page    │  │  + History   │  │  + Controls      │  │
│  └──────────┘  └──────┬───────┘  └──────────────────┘  │
│                       │                                  │
├───────────────────────┼──────────────────────────────────┤
│                  BACKEND (Python)                        │
│                       │                                  │
│  ┌────────────────────▼────────────────────┐            │
│  │          RAG Agent (LangChain)          │            │
│  │  ┌──────────┐  ┌───────────────────┐   │            │
│  │  │ Document │  │  Gemini 2.0 Flash │   │            │
│  │  │ Grader   │  │  (LLM + Embeddings)│  │            │
│  │  └──────────┘  └───────────────────┘   │            │
│  └────────────────────┬────────────────────┘            │
│                       │                                  │
│  ┌────────────────────▼────────────────────┐            │
│  │        ChromaDB (Vector Store)          │            │
│  │     Búsqueda MMR · Persistente          │            │
│  └────────────────────┬────────────────────┘            │
│                       │                                  │
│  ┌────────────────────▼────────────────────┐            │
│  │      Multi-Format Document Loaders      │            │
│  │  PDF · DOCX · XLSX · PPTX · MD · CSV   │            │
│  │          · JSON · HTML                   │            │
│  └─────────────────────────────────────────┘            │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                  OCI (Oracle Cloud)                       │
│  ┌──────────────┐        ┌──────────────────┐           │
│  │   Compute    │        │  Object Storage  │           │
│  │  A1.Flex VM  │        │  (Documentos)    │           │
│  │  Always Free │        │  Always Free     │           │
│  └──────────────┘        └──────────────────┘           │
└──────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologías

| Categoría | Tecnología | Propósito |
|:---|:---|:---|
| **LLM** | Google Gemini 2.0 Flash | Generación de respuestas |
| **Embeddings** | Google Embedding-001 | Vectorización de documentos |
| **Framework IA** | LangChain | Orquestación RAG |
| **Vector DB** | ChromaDB | Almacenamiento y búsqueda vectorial |
| **Frontend** | Streamlit | Interfaz de usuario web |
| **Contenedores** | Docker | Containerización |
| **Cloud** | Oracle Cloud (OCI) | Hosting en producción |

---

## 📁 Estructura del Proyecto

```
agente/
├── app.py                     # Aplicación principal Streamlit
├── config.py                  # Configuración centralizada
├── generate_docs.py           # Generador de documentos de ejemplo
├── requirements.txt           # Dependencias Python
├── Dockerfile                 # Containerización
├── docker-compose.yml         # Orquestación Docker
├── .env.example               # Template de variables de entorno
│
├── agents/                    # Agentes de IA
│   ├── rag_agent.py           # Agente RAG principal
│   └── document_grader.py     # Verificador de relevancia
│
├── loaders/                   # Cargadores de documentos
│   └── multi_loader.py        # Soporte multi-formato
│
├── vectorstore/               # Base de datos vectorial
│   └── chroma_store.py        # Gestión de ChromaDB
│
├── documents/                 # Documentos de la empresa
│   ├── politica_privacidad.pdf
│   ├── politica_reembolso.docx
│   ├── faq.md
│   ├── guia_envios.html
│   ├── terminos_condiciones.pdf
│   ├── catalogo_productos.xlsx
│   ├── precios_envio.csv
│   ├── config_tienda.json
│   └── presentacion_empresa.pptx
│
└── chroma_db/                 # Vector store (auto-generado)
```

---

## 🚀 Instalación y Uso Local

### Prerrequisitos

- Python 3.11+
- [API Key de Google Gemini](https://aistudio.google.com/) (gratuita)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/amershop-agente-ia.git
cd amershop-agente-ia
```

### Paso 2: Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

```bash
# Copiar el template
cp .env.example .env

# Editar .env y agregar tu API Key de Gemini
# GOOGLE_API_KEY=tu_api_key_aqui
```

### Paso 5: Generar documentos de ejemplo

```bash
python generate_docs.py
```

### Paso 6: Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible en: **http://localhost:8501**

### Credenciales de prueba

| Usuario | Contraseña |
|:---|:---|
| `admin` | `amershop2024` |
| `colaborador1` | `collab001` |
| `rrhh` | `recursosh01` |
| `ventas` | `ventas2024` |
| `soporte` | `soporte01` |

---

## 🐳 Docker

### Construir y ejecutar con Docker Compose

```bash
# Crear archivo .env con tu API Key
echo "GOOGLE_API_KEY=tu_api_key" > .env

# Construir y levantar
docker-compose up -d --build

# Ver logs
docker-compose logs -f
```

### Construir manualmente

```bash
docker build -t amershop-agent .
docker run -d -p 8501:8501 --env-file .env amershop-agent
```

---

## ☁️ Deploy en Oracle Cloud Infrastructure (OCI)

### Servicios OCI Utilizados

1. **OCI Compute** (Always Free - VM.Standard.A1.Flex): Servidor de la aplicación
2. **OCI Object Storage** (Always Free): Almacenamiento de documentos

### Pasos de Deploy

#### 1. Crear instancia Compute

1. Accede a la [consola de OCI](https://cloud.oracle.com/)
2. Ve a **Compute → Instances → Create Instance**
3. Selecciona:
   - Shape: **VM.Standard.A1.Flex** (Always Free)
   - OCPUs: **2**
   - RAM: **12 GB**
   - Image: **Ubuntu 22.04**
4. Descarga la clave SSH

#### 2. Configurar la VM

```bash
# Conectar por SSH
ssh -i tu_clave.key ubuntu@<IP_PUBLICA>

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo apt install docker-compose -y
```

#### 3. Desplegar la aplicación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/amershop-agente-ia.git
cd amershop-agente-ia

# Configurar API Key
echo "GOOGLE_API_KEY=tu_api_key" > .env

# Generar documentos
pip3 install reportlab python-docx openpyxl python-pptx
python3 generate_docs.py

# Levantar con Docker
docker-compose up -d --build
```

#### 4. Abrir puertos (Security List)

1. En la consola OCI: **Networking → Virtual Cloud Networks**
2. Selecciona tu VCN → **Security Lists** → Default
3. Agrega **Ingress Rule**:
   - Source CIDR: `0.0.0.0/0`
   - Protocol: TCP
   - Destination Port: `8501`

#### 5. Acceder a la aplicación

```
http://<IP_PUBLICA_DE_TU_VM>:8501
```

---

## 📋 Documentos de Ejemplo

El proyecto incluye 9 documentos de ejemplo realistas en español para la tienda AmershOp:

| Documento | Formato | Categoría |
|:---|:---|:---|
| Política de Privacidad | PDF | Legal |
| Política de Reembolso | DOCX | Operacional |
| Preguntas Frecuentes | Markdown | Atención al Cliente |
| Guía de Envíos | HTML | Logística |
| Términos y Condiciones | PDF | Legal |
| Catálogo de Productos | Excel | Comercial |
| Precios de Envío | CSV | Logística |
| Configuración de Tienda | JSON | Sistemas |
| Presentación Corporativa | PPTX | Estratégico |

---

## 🔒 Seguridad

- **Autenticación**: Sistema de login con usuario y contraseña
- **API Key**: Almacenada en variables de entorno (nunca en código)
- **Docker**: Ejecución aislada en contenedor
- **.gitignore**: Archivos sensibles excluidos del repositorio

---

## 🤝 Créditos

Proyecto desarrollado como parte del desafío de Inteligencia Artificial de [Alura LATAM](https://www.aluracursos.com/).

---

<div align="center">

**Hecho con ❤️ por Amer**

🛒 AmershOp — Tecnología para Todos

</div>
