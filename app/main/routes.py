from flask import Blueprint, render_template, session, request, redirect, url_for
from app.main import main
from app.spotify.utils import authorize_spotify, get_spotify_client

@main.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        scope = ' '.join(['playlist-read-private', 
                          'playlist-modify-public', 
                          'playlist-modify-private', 
                          'playlist-read-collaborative',
                          'user-library-modify', 
                          'user-library-read'])
        
        client_token = authorize_spotify(scope)
        session['client_token'] = client_token
        session['client_name'] = get_spotify_client().get_user_name()

        print("Token y nombre del cliente inicializados!!!")

        # Redirige al índice principal después de iniciar sesión
        return redirect(url_for('main.index'))
    
    # Renderiza la página de inicio de sesión
    return render_template('login.html')

@main.route('/logout')
def logout_user():

    spotify_client = get_spotify_client()
    spotify_client.logout()

    print("Cerrando sesión")
    return redirect(url_for('main.login_user'))

@main.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['action'] = request.form.get('action', '')
        
        if session['action'] == 'backup':
            # Redirige a la opción de backup
            return redirect(url_for('spotify.backup_options'))
        elif session['action'] == 'auto_like':
            # Redirige a la opción de auto like
            return redirect(url_for('spotify.upload_like'))
    
    # Renderiza un template para la página principal
    return render_template('index.html')
