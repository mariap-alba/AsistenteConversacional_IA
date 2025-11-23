from flask import Blueprint, request, jsonify
from app.pipelines.response_pipeline import QueryResponse

response_bp = Blueprint("response",__name__)



@response_bp.route('/ask', methods=['POST'])
def ask():  
    """
    API POST/ask 
    Recibe la pregunta del usuario y envia la respuesta del asistente con el contexto.
    """ 
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "error": "No se encontro informacion"
        }), 400
    
    question = data.get("question")
    response = QueryResponse()
    retriver_doc = response.retriver(query_user=question)
    context_chunks = [doc["document"] for doc in retriver_doc]
    answer = response.response(query_user=question, retrieved_docs=retriver_doc)

    return jsonify({
        "answer": answer,
        "context": context_chunks
    }) 

@response_bp.route('/health', methods=['GET'])
def health():
    """
    API GET/health 
    Verificar la conexion
    """ 
    return jsonify({
        "status": "OK"
    })