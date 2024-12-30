from flask import Blueprint, render_template, request, session, flash, redirect, url_for, current_app, jsonify, send_file
from app.spotify.utils import handle_file_upload, get_spotify_client
from app.spotify.spotify_api import SpotifyAPI
from app.spotify import spotify
import os
from datetime import datetime
import unicodedata

@spotify.route('/backup_options', methods=['GET', 'POST'])
def backup_options():
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud (JSON)
        data = request.get_json()
        selected_scopes = data.get('scopes', [])

        if selected_scopes:
            # Guardamos las opciones seleccionadas en la sesión
            session['backup_scope'] = selected_scopes
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'No options selected'}), 400

    # Si es un GET, mostrar la lista de playlists
    spotify_client = get_spotify_client()

    # Obtén directamente la lista de playlists
    playlists_data = spotify_client.list('me/playlists')  # Ya es una lista

    # Renderiza la plantilla con los datos de las playlists
    return render_template('backup_options.html', playlists=playlists_data)


@spotify.route('/process_backup')
def process_backup():
    spotify_client = get_spotify_client()

    data = []
    if 'liked' in session['backup_scope']:
        liked = spotify_client.list('me/tracks')
        data.append({'type': 'liked', 'data': liked})

    for playlist_id in session['backup_scope']:
        if playlist_id == 'liked':
            continue
        playlist_tracks = spotify_client.list(f'playlists/{playlist_id}/tracks')
        playlist_name = spotify_client.get(f'playlists/{playlist_id}')['name']
        data.append({'type': f'playlist: {playlist_name}', 'data': playlist_tracks})

    # Obtener la fecha y hora actual y el nombre de usuario para crear un nombre único de archivo
    username = session.get('client_name', 'anonymous')  # Suponiendo que el nombre de usuario está en la sesión

    # Limpiar el nombre de usuario (eliminando tildes y caracteres especiales)
    safe_username = ''.join(c for c in unicodedata.normalize('NFD', username) if unicodedata.category(c) != 'Mn')

    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'backup_{current_time}_{safe_username}.txt'

    # Ruta completa del archivo
    file_path = os.path.join(current_app.config['GENERATED_FILES_FOLDER'], filename)
    print(file_path)

    # Crear el archivo
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"\n{item['type'].capitalize()}:\n")
            for track in item['data']:
                try:
                    track_name = track['track'].get('name')
                    if not track_name:
                        continue
                    artist_name = ', '.join(artist['name'] for artist in track['track']['artists'])
                    uri = track['track']['uri']
                    f.write(f"{track_name} - {artist_name}\t{uri}\n")
                except KeyError:
                    continue

    # Flash de éxito
    flash(f'Backup completed successfully! File saved as {filename}.', 'success')

    # Sentencia para solucionar problemas con el path
    # 'file_path' anterior --> Ruta relativa
    # 'file_path' nuevo --> Ruta absoluta
    file_path = os.path.abspath(os.path.join(current_app.config['GENERATED_FILES_FOLDER'], filename))

    # Enviar el archivo como respuesta para que se descargue automáticamente
    return send_file(file_path, as_attachment=True, download_name=filename)

@spotify.route('/upload_like', methods=['GET', 'POST'])
def upload_like():
    return render_template('upload_like.html')

@spotify.route('/process_like', methods=['POST'])
def process_like():
    file = request.files.get('file')
    if not file:
        flash("No file selected.", 'error')
        return jsonify({"status": "error", "message": "No file selected."}), 400

    file_path = os.path.join(current_app.config['TEMP_UPLOADS_FOLDER'], file.filename)
    file.save(file_path)

    try:
        handle_file_upload(file_path)
        flash('Liked tracks and created playlists successfully!', 'success')
        return jsonify({"status": "success", "redirect_url": url_for('main.index')}), 200
    except Exception as e:
        flash(f"Error processing file: {e}", 'error')
        return jsonify({"status": "error", "message": f"Error processing file: {e}"}), 500
