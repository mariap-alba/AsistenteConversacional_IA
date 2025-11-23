import os, chromadb, fitz, tiktoken
from app.logs.logger import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from pathlib import Path

logger = get_logger("Ingestion PDF")

class Ingestion():

    def __init__(self):
        self.vectordb = "app/database/.chroma"
        self.model_name = "all-MiniLM-L6-v2"

    """
    =============================================
    METODO PARA LA EXTRACION DE TEXTO DEL PDF
    =============================================
    """  
    def load_pdf(self, document:str):        
        path_doc = f"app/source/{document}"        
        if not os.path.exists(path_doc):
            logger.error(f"No existe el archivo {document}")
            return ""

        doc = fitz.open(path_doc)   

        texto = ""
        for pagina in doc:
            texto += pagina.get_text("text") + "\n"

        doc.close()
        return texto
    
    """
    ==================================================
    METODO PARA GENERAR LOS CHUNKS DE APROX 500 TOKENS
    ==================================================
    """ 
    def chunking(self, text: str):
        logger.info("===== Generando chunks =====")

        enc = tiktoken.get_encoding("cl100k_base")
        def contar_tokens(txt: str):
            return len(enc.encode(txt))
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=150,
            length_function=contar_tokens,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        chunks = splitter.split_text(text)
        return chunks
    
    """
    ==================================================
    METODO PARA CREAR LA BASE DE DATOS VECTORIAL
    ==================================================
    """ 
    def create_coleccion(self, collection_name:str):
        client = chromadb.PersistentClient(path=str(self.vectordb))
        model_embendding = SentenceTransformerEmbeddingFunction(model_name=self.model_name, normalize_embeddings=True)

        logger.info("======= Creando coleccion =========")
        
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=model_embendding  
        )

        return collection
    

    """
    ==================================================
    METODO PARA REALIZAR LA INDEXACION EN LA DB
    ==================================================
    """ 
    def indexing(self, document:str, collection_name: str = "data"):
        
        # Extrae texto del documento
        text = self.load_pdf(document=document)
        if text == "":
            return 'Error al indexar documento'

        # Genera los chunks
        chunks = self.chunking(text=text)
        logger.info(f"Chunks generados {len(chunks)}")

        # Crear la coleccion en chroma
        collection = self.create_coleccion(collection_name=collection_name)
        logger.info("Colección creada con exito")

        ids = []
        metadatos = []
        for i in range(len(chunks)):
            ids.append(f"id{i}")
            metadatos.append({"source": document, "type": "PDF"})

        collection.add(documents=chunks, metadatas=metadatos, ids=ids)
        logger.info("Documento indextado")

        return "Documento indexado correctamente"