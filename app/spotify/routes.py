from flask import Blueprint, render_template, request, session, flash, redirect, url_for, current_app
from app.spotify.utils import handle_file_upload, get_spotify_client
from app.spotify.spotify_api import SpotifyAPI
from app.spotify import spotify
import os

@spotify.route('/backup_options', methods=['GET', 'POST'])
def backup_options():
    if request.method == 'POST':
        return redirect(url_for('spotify.process_backup'))

    spotify_client = get_spotify_client()
    playlists = spotify_client.list('me/playlists')

    return render_template('backup_options.html', playlists=playlists)

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

    file_path = os.path.join(current_app.config['GENERATED_FILES_FOLDER'], 'backup.txt')
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

    flash('Backup completed successfully! File saved as backup.txt.', 'success')
    return redirect(url_for('main.index'))

@spotify.route('/upload_like', methods=['GET', 'POST'])
def upload_like():
    return render_template('upload_like.html')

@spotify.route('/process_like', methods=['POST'])
def process_like():
    file = request.files.get('file')
    if not file:
        flash("No file selected.", 'error')
        return redirect(url_for('spotify.upload_like'))

    file_path = os.path.join(current_app.config['TEMP_UPLOADS_FOLDER'], file.filename)
    file.save(file_path)

    try:
        handle_file_upload(file_path)
        flash('Liked tracks and created playlists successfully!', 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        flash(f"Error processing file: {e}", 'error')
        return redirect(url_for('spotify.upload_like'))
