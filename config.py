import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    GENERATED_FILES_FOLDER = os.getenv('GENERATED_FILES_FOLDER', 'generated_filesss')
    TEMP_UPLOADS_FOLDER = os.getenv('TEMP_UPLOADS_FOLDER', 'temp_uploads')
    SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:43019/redirect'

    @staticmethod
    def init_app(app):
        print("Initializing app with config...")
        # Ensure required folders exist
        os.makedirs(Config.GENERATED_FILES_FOLDER, exist_ok=True)
        os.makedirs(Config.TEMP_UPLOADS_FOLDER, exist_ok=True)