from flask import Flask
from config import Config
from app.spotify import spotify as spf_bprint
from app.main import main as main_bprint

def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object(Config)
    Config.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(main_bprint)
    app.register_blueprint(spf_bprint)

    return app