from app.spotify.spotify_api import SpotifyAPI
from flask import session, g

def authorize_spotify(scope):
    return SpotifyAPI.authorize(scope=scope)

def get_spotify_client():
    if 'spotify_client' not in g:
        token = session.get('client_token')
        if not token:
            raise RuntimeError("No Spotify token found in session.")
        g.spotify_client = SpotifyAPI(token)
    return g.spotify_client

def handle_file_upload(file_path):
    spotify_client = get_spotify_client()

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    liked_tracks = []
    playlists = {}
    current_playlist = None

    for line in lines:
        if not line.strip():
            continue

        if '\t' in line:
            # Procesa las canciones
            track_info = line.strip().split('\t')
            if len(track_info) == 2:
                track_name, uri = track_info
                if 'Liked' in current_playlist:
                    liked_tracks.append(uri)
                else:
                    # Si la playlist no existe en el diccionario, crear una lista vacía
                    if current_playlist not in playlists:
                        playlists[current_playlist] = []
                    # Añadir la canción a la lista de la playlist correspondiente
                    playlists[current_playlist].append(uri)
            else:
                print(f"Error: La línea no tiene el formato esperado -> {line.strip()}")
        else:
            # Nueva playlist encontrada
            current_playlist = line.strip()

    # Procesar los "likes"
    for track_uri in liked_tracks:
        track_id = track_uri.split(":")[-1]
        spotify_client.like_track(track_id)

    # Crear las playlists y añadir todas sus canciones
    for playlist_name, tracks in playlists.items():
        # Crear la playlist una sola vez y luego agregar sus canciones
        playlist_name = playlist_name.split('Playlist: ')[-1]
        playlist_name = playlist_name[0].upper() + playlist_name[1:-1]
        #print(playlist_name)

        playlist = spotify_client.create_playlist(playlist_name)
        # Añadir todas las canciones de esta playlist
        for track_uri in tracks:
            track_id = track_uri.split(":")[-1]
            spotify_client.add_track_to_playlist(playlist['id'], track_id)