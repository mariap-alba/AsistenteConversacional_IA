from flask import Flask
from flask_cors import CORS
from app.routers.response import response_bp

def create_app():
    app = Flask(__name__)

    CORS(app)
    app.register_blueprint(response_bp)

    return app

app = create_app()
