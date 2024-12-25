from flask import Blueprint

# Mueve la creación del Blueprint aquí, antes de importar routes.py
main = Blueprint('main', __name__)

# Ahora importa las rutas
import app.main.routes