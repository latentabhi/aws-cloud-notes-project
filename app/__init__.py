from flask import Flask
from dotenv import load_dotenv
from .database import init_db
from .routes import routes


def create_app():
    load_dotenv()
    app = Flask(__name__)

    init_db()
    app.register_blueprint(routes)

    return app
