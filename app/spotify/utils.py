from app.spotify.spotify_api import SpotifyAPI

def authorize_spotify(client_id, scope):
    return SpotifyAPI.authorize(client_id=client_id, scope=scope)

def handle_file_upload(file_path, client_id):
    scope = 'playlist-modify-public playlist-modify-private user-library-modify user-library-read'
    spotify_client = authorize_spotify(client_id, scope)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    liked_tracks = []
    playlists_to_create = []
    current_playlist = None

    for line in lines:
        if not line.strip():
            # Si la línea está vacía o contiene solo espacios, sáltala.
            continue

        if '\t' in line:
            # Procesa las líneas con tabulación.
            track_info = line.strip().split('\t')
            if len(track_info) == 2:
                # Asegúrate de que hay exactamente dos elementos tras el split.
                track_name, uri = track_info
                if 'Liked' in current_playlist:
                    liked_tracks.append(uri)  # Añade a la lista de canciones "Liked"
                else:
                    playlists_to_create.append((current_playlist, uri))  # Añade a la playlist
            else:
                print(f"Error: La línea no tiene el formato esperado -> {line.strip()}")
        else:
            # Procesa las líneas que definen el nombre de una playlist.
            current_playlist = line.strip()

    #print(f"{liked_tracks}")

    for track_uri in liked_tracks:
        track_id = track_uri.split(":")[-1]
        #print(track_id)
        spotify_client.like_track(track_id)

    for playlist_name, track_uri in playlists_to_create:
        playlist = spotify_client.create_playlist(client_id, playlist_name)
        track_id = track_uri.split(":")[-1]
        spotify_client.add_track_to_playlist(playlist['id'], track_id)
