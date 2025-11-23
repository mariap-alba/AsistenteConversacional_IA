import chromadb
from app.logs.logger import get_logger
from langchain_ollama.llms import OllamaLLM

logger = get_logger("Query Response")

class QueryResponse():
    
    def __init__(self):
        """
        Se inicia el modelo generativo Open Source Ollama
        """
        try:
            self.collection = "data"
            self.vectordb = "app/database/.chroma"
            self.model_name = "llama3.2:1b"
            self.llm = OllamaLLM(model=self.model_name)
            logger.info(f"Modelo open-source '{self.model_name}' inicializado correctamente con Ollama")
        except Exception as e:
            logger.error(f"Error inicializando modelo Open Source: {e}")


    
    def retriver(self, query_user: str , n_result: int = 4):
        """
        Se realiza la busqueda en la base de datos vectorial ChromaDB a partir de la consulta ingresada por el usuario.
        Extrae el documento, los metadatos y la distancia (similitud coseno).
        Si la distancia es menor significa que coincide.
        """
        client = chromadb.PersistentClient(path=self.vectordb)        
        collection = client.get_collection(name=self.collection)
        
        resultado = collection.query(
            query_texts=[query_user],
            n_results=n_result
        )

        documents = resultado.get('documents', [[]])[0]
        metadatas = resultado.get('metadatas', [[]])[0]
        distances = resultado.get('distances', [[]])[0]

        if not (len(documents) == len(metadatas) == len(distances)):
            logger.error("Error: las listas de documentos, metadatos y distancias no coinciden.")
            return []

        retrieved_docs = []
        logger.info(f"Se encontraron {len(documents)} fragmentos relevantes (scores de distancia, menor es mejor):")
        for i, doc in enumerate(documents):
            distance = distances[i]
            metadata = metadatas[i]
            retrieved_docs.append({
                'document': doc,
                'metadata': metadata,
                'distance': distance
            })
            logger.info(f"  - Doc {i + 1}: Distancia = {distance:.4f}, Archivo = {metadata.get('source')}, "
                        f"type = {metadata.get('type')}")

        return retrieved_docs
    
    def response(self, query_user: str, retrieved_docs: list[dict]):
        """
        Genera una respuesta usando el modelo OllamaLLM basado en el contexto de ChromaDB.
        """
        logger.info("--- Paso 2: Generando respuesta con Ollama... ---")
        logger.info(f"Pregunta ingresada por el usuario:  {query_user}")

        if not self.llm:
            return "Error: Modelo Ollama no inicializado."

        if not retrieved_docs:
            return "No se encontró información relevante para responder a esta pregunta."

        # Construir contexto
        context_chunks = [doc["document"] for doc in retrieved_docs]
        context = "\n\n====================\n\n".join(context_chunks)
        
        PROMPT = f"""
            Responde ÚNICAMENTE usando el siguiente CONTEXTO.
            No inventes. Si la respuesta NO está en el contexto, di exactamente:
            "No tengo información suficiente en el contexto."

            CONTEXTO:
            {context}

            ---

            PREGUNTA:
            {query_user}

            ---

            INSTRUCCIÓN:
            - Usa el contenido textual del contexto para responder.
            - NO agregues información fuera del contexto.
            - Responde en español.
            - Sé claro, preciso y extrae la respuesta LITERAL del texto cuando sea posible.

            RESPUESTA:
            """
        try:            
            respuesta = self.llm.invoke(PROMPT)
            logger.info("====== Respuesta generada correctamente. =====")
            return respuesta
        except Exception as e:
            logger.error(f"Error usando OllamaLLM: {e}")
            return f"Error al contactar modelo Ollama: {e}"