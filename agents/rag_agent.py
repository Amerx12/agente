import logging
from typing import Dict, Any, List, Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from agents.document_grader import DocumentGrader
from config import LLM_MODEL

logger = logging.getLogger(__name__)

class RAGAgent:
    """
    Agente principal de RAG (Retrieval-Augmented Generation) para AmershOp.
    Orquesta la recuperación de documentos y la generación de respuestas.
    """

    def __init__(self, vector_store_manager):
        """
        Inicializa el agente RAG.

        Args:
            vector_store_manager: Gestor del almacén de vectores.
        """
        self.vector_store_manager = vector_store_manager
        self.llm = ChatGroq(model_name=LLM_MODEL, temperature=0.1)
        self.document_grader = DocumentGrader()
        
        # Sistema de prompt en español según los requerimientos
        system_prompt = """Eres el asistente virtual corporativo de AmershOp, una tienda online de tecnología.
Tu rol es responder preguntas de los colaboradores basándote ÚNICAMENTE en los documentos internos de la empresa proporcionados como contexto.

Reglas:
- Responde siempre en español
- Cita el documento fuente entre corchetes [nombre_archivo] al final de cada afirmación
- Si no encuentras la información en el contexto, responde: 'No encontré información sobre este tema en los documentos disponibles. Te sugiero consultar con el área correspondiente.'
- Sé conciso pero completo en tus respuestas
- No inventes información que no esté en los documentos
- Si la pregunta es un saludo, responde amablemente y ofrece tu ayuda

Contexto:
{context}"""

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{question}")
            ]
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()

    def query(self, question: str, chat_history: Optional[list] = None) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario, recupera documentos relevantes y genera una respuesta.

        Args:
            question (str): La pregunta del usuario.
            chat_history (list, opcional): Historial de conversación.

        Returns:
            dict: Diccionario que contiene:
                - 'answer' (str): La respuesta generada.
                - 'sources' (list): Lista de nombres de archivos fuente.
                - 'context_docs' (list): Lista de objetos Document utilizados como contexto.
        """
        if chat_history is None:
            chat_history = []
            
        try:
            # 1. Recuperar documentos relevantes del almacén de vectores (k=5, MMR)
            raw_docs = self.vector_store_manager.search(question, k=5)
            
            # 2. Opcionalmente evaluar la relevancia de los documentos
            relevant_docs = []
            for doc in raw_docs:
                if self.document_grader.grade(question, doc):
                    relevant_docs.append(doc)
            
            # Si no hay documentos relevantes después de filtrar, evitar usar nada 
            # (o se podría usar un documento genérico para forzar la respuesta de no información)
            if not relevant_docs and raw_docs:
                logger.info("Ningún documento superó el filtro de relevancia.")
                
            # Extraer fuentes y preparar contexto
            sources = list(set([doc.metadata.get("source", "desconocido") for doc in relevant_docs]))
            
            # Formatear el contexto para el prompt, incluyendo la fuente para facilitar la cita
            context_text = "\n\n".join([f"Fuente: {doc.metadata.get('source', 'desconocido')}\nContenido: {doc.page_content}" for doc in relevant_docs])
            
            # 3 & 4. Construir prompt con contexto y llamar a Gemini
            answer = self.chain.invoke({
                "context": context_text,
                "question": question,
                "chat_history": chat_history
            })
            
            # 5. Devolver resultados
            return {
                "answer": answer,
                "sources": sources,
                "context_docs": relevant_docs
            }
            
        except Exception as e:
            logger.error(f"Error procesando la consulta RAG: {e}")
            return {
                "answer": "Ocurrió un error al procesar tu consulta. Por favor, intenta de nuevo más tarde.",
                "sources": [],
                "context_docs": []
            }
