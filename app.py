import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from spotify_api import SpotifyAPI

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de las carpetas
app.config['GENERATED_FILES_FOLDER'] = 'generated_files'
app.config['TEMP_UPLOADS_FOLDER'] = 'temp_uploads'

# Crear las carpetas si no existen
if not os.path.exists(app.config['GENERATED_FILES_FOLDER']):
    os.makedirs(app.config['GENERATED_FILES_FOLDER'])
if not os.path.exists(app.config['TEMP_UPLOADS_FOLDER']):
    os.makedirs(app.config['TEMP_UPLOADS_FOLDER'])

# Página inicial: selecciona acción
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['client_id'] = request.form['client_id']
        session['action'] = request.form['action']
        if session['action'] == 'backup':
            return redirect(url_for('backup_options'))
        elif session['action'] == 'auto_like':
            return redirect(url_for('upload_like'))
    return render_template('index.html')

# Opciones para respaldo
@app.route('/backup_options', methods=['GET', 'POST'])
def backup_options():
    if request.method == 'POST':
        session['backup_scope'] = request.form.getlist('scope')
        return redirect(url_for('process_backup'))

    client_id = session.get('client_id')
    scope = 'playlist-read-private'

    spotify = SpotifyAPI.authorize(client_id=client_id, scope=scope)
    playlists = spotify.list('me/playlists')  # Obtener playlists del usuario

    return render_template('backup_options.html', playlists=playlists)

# Procesar respaldo
@app.route('/process_backup')
def process_backup():
    client_id = session.get('client_id')
    scope = ' '.join(['playlist-read-private', 'user-library-read'])

    spotify = SpotifyAPI.authorize(client_id=client_id, scope=scope)

    data = []
    if 'liked' in session['backup_scope']:
        # Obtener canciones que le gustaron al usuario
        liked = spotify.list('me/tracks')
        data.append({'type': 'liked', 'data': liked})
    
    # Procesar playlists seleccionadas
    for playlist_id in session['backup_scope']:
        if playlist_id == 'liked':
            continue  # Saltar el ID especial de "liked"
        
        # Obtener las canciones de la playlist seleccionada
        playlist_tracks = spotify.list(f'playlists/{playlist_id}/tracks')
        playlist_name = spotify.get(f'playlists/{playlist_id}')['name']  # Obtener nombre de la playlist
        data.append({'type': f'playlist: {playlist_name}', 'data': playlist_tracks})

    # Escribir datos a un archivo en la carpeta 'generated_files'
    file_path = os.path.join(app.config['GENERATED_FILES_FOLDER'], 'backup.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"\n{item['type'].capitalize()}:\n")
            for track in item['data']:
                try:
                    # Verificar si la canción tiene nombre
                    track_name = track['track'].get('name')
                    if not track_name:
                        continue  # Omitir si no tiene nombre
                    
                    # Obtener artistas y URI
                    artist_name = ', '.join(artist['name'] for artist in track['track']['artists'])
                    uri = track['track']['uri']
                    
                    # Escribir en el archivo
                    f.write(f"{track_name} - {artist_name}\t{uri}\n")
                except KeyError:
                    continue  # Omitir canciones con datos malformados

    flash('Backup completed successfully! File saved as backup.txt.', 'success')
    return redirect(url_for('index'))

@app.route('/upload_like', methods=['GET', 'POST'])
def upload_like():
    return render_template('upload_like.html')

@app.route('/process_like', methods=['POST', 'GET'])
def process_like():
    if request.method == 'POST':
        # Obtener el archivo del formulario
        file = request.files.get('file')
        if not file:
            flash("No file selected.", 'error')
            return redirect(url_for('upload_like'))  # Redirigir si no se seleccionó un archivo

        # Guardar el archivo en la carpeta 'temp_uploads'
        file_path = os.path.join(app.config['TEMP_UPLOADS_FOLDER'], file.filename)
        file.save(file_path)

        try:
            # Leer el archivo .txt
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Filtrar canciones y crear listas de canciones a dar like
            liked_tracks = []
            playlists_to_create = []
            current_playlist = None

            for line in lines:
                # Ignorar líneas vacías o encabezados
                if not line.strip():
                    continue

                # Procesar canción
                if '\t' in line:
                    track_info = line.strip().split('\t')
                    track_name, uri = track_info[0], track_info[1]
                    if 'Liked' in current_playlist:
                        liked_tracks.append(uri)  # Agregar la canción a la lista de canciones a dar like
                    else:
                        playlists_to_create.append((current_playlist, uri))  # Crear una playlist si es necesario
                else:
                    current_playlist = line.strip()  # Usar el nombre de la playlist

            # Conectar a Spotify para dar like a las canciones y crear playlists
            client_id = session.get('client_id')
            scope = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'
            spotify = SpotifyAPI.authorize(client_id=client_id, scope=scope)

            # Dar like a las canciones usando el método like_track
            for track_uri in liked_tracks:
                try:
                    track_id = track_uri.split(":")[-1]  # Obtener el track_id de la URI
                    spotify.like_track(track_id)  # Llamada para darle like a la canción
                    print(f"Liked track: {track_uri}")
                except Exception as e:
                    #print(f"Error liking track {track_uri}: {e}")
                    continue

            # Crear playlists si es necesario usando el método create_playlist
            for playlist_name, track_uri in playlists_to_create:
                try:
                    # Crear la playlist (si no existe)
                    playlist = spotify.create_playlist(client_id, playlist_name)  # Crear la playlist con el nombre dado
                    # Agregar la canción a la playlist usando el método adecuado
                    track_id = track_uri.split(":")[-1]  # Obtener el track_id de la URI
                    spotify.add_track_to_playlist(playlist['id'], track_id)  # Agregar la canción a la playlist
                    print(f"Added {track_uri} to playlist: {playlist_name}")
                except Exception as e:
                    print(f"Error adding track to playlist {playlist_name}: {e}")
            
            flash('Liked tracks and created playlists successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f"Error processing file: {e}", 'error')
            return redirect(url_for('upload_like'))  # Redirigir si hay un error en el procesamiento

    return render_template('upload_like.html')


if __name__ == '__main__':
    app.run(debug=True)
