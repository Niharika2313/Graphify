from flask import Flask
from .routes import main
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY","dev-key")

    app.register_blueprint(main)

    return app
