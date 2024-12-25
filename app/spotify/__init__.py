from flask import Blueprint

spotify = Blueprint('spotify', __name__)

import app.spotify.routes