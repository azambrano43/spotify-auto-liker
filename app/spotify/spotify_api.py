import codecs
import json
import logging
import re
import time
import urllib.parse
import urllib.request
import webbrowser
import http.server
import sys
import requests

class SpotifyAPI:
    
    BASE_URL = 'https://api.spotify.com/v1/'  # Definir BASE_URL como constante de clase

    def __init__(self, auth):
        self._auth = auth

    # Método para "cerrar sesión"
    def logout(self):
        """Invalida el token actual y cierra la sesión en Spotify (si aplica)."""
        logging.info("Logging out and invalidating token.")
        self._auth = None  # Elimina el token actual de la instancia.
        webbrowser.open('https://accounts.spotify.com/en/logout')  # Redirige para cerrar sesión en Spotify.
        logging.info('Logged out succesfully!!!')

    # Obtiene un recurso desde la API de Spotify y devuelve el objeto.
    def get(self, url, params={}, tries=3):
        if not url.startswith(self.BASE_URL):
            url = self.BASE_URL + url
        if params:
            url += ('&' if '?' in url else '?') + urllib.parse.urlencode(params)

        for _ in range(tries):
            try:
                req = urllib.request.Request(url)
                req.add_header('Authorization', 'Bearer ' + self._auth)
                res = urllib.request.urlopen(req)
                reader = codecs.getreader('utf-8')
                return json.load(reader(res))
            except Exception as err:
                logging.info('Couldn\'t load URL: {} ({})'.format(url, err))
                time.sleep(2)
                logging.info('Trying again...')
        sys.exit(1)

    # La API de Spotify divide listas largas en varias páginas. Este método obtiene todas las páginas.
    def list(self, url, params={}):
        last_log_time = time.time()
        response = self.get(url, params)
        items = response['items']

        while response['next']:
            if time.time() > last_log_time + 15:
                last_log_time = time.time()
                logging.info(f"Loaded {len(items)}/{response['total']} items")

            response = self.get(response['next'])
            items += response['items']
        return items

    # Abre el navegador para que el usuario inicie sesión y autorice el acceso a la API.
    @staticmethod
    def authorize(scope, client_id = 'a851bce480d24360803b7e4c64a098c3'):
        url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode({
            'response_type': 'token',
            'client_id': client_id,
            'scope': scope,
            'redirect_uri': 'http://127.0.0.1:{}/redirect'.format(SpotifyAPI._SERVER_PORT)
        })
        logging.info(f'Logging in (click if it doesn\'t open automatically): {url}')
        webbrowser.open(url)

        server = SpotifyAPI._AuthorizationServer('127.0.0.1', SpotifyAPI._SERVER_PORT)
        try:
            while True:
                server.handle_request()
        except SpotifyAPI._Authorization as auth:
            return auth.access_token
    

    # Método para dar like a una canción
    def like_track(self, track_id):
        url = f'me/tracks'
        headers = {
            'Authorization': f'Bearer {self._auth}',
            'Content-Type': 'application/json'
        }
        data = {
            'ids': [track_id]
        }
        response = requests.put(self.BASE_URL + url, json=data, headers=headers)
        if response.status_code == 200:
            logging.info(f"Track liked: {track_id}")
            return {"message": f"Track {track_id} liked successfully"}
        else:
            logging.error(f"Error liking track {track_id}: {response.status_code} - {response.text}")
            raise Exception(f"Error liking track {track_id}: {response.status_code} - {response.text}")

    # Método para crear una nueva playlist
    def create_playlist(self, name, description=''):

        user_id = self.get('me')['id']

        url = f'users/{user_id}/playlists'
        
        data = {
            'name': name,
            'description': description,
            'public': True
        }
        headers = {
            'Authorization': f'Bearer {self._auth}',
            'Content-Type': 'application/json'
        }
        response = requests.post(self.BASE_URL + url, json=data, headers=headers)
        if response.status_code == 201:
            logging.info(f"Playlist created: {name}")
            return response.json()
        else:
            logging.error(f"Error creating playlist {name}: {response.status_code} - {response.text}")
            raise Exception(f"Error creating playlist {name}: {response.status_code} - {response.text}")

    # Método para agregar una canción a una playlist
    def add_track_to_playlist(self, playlist_id, track_id):
        url = f'playlists/{playlist_id}/tracks'
        headers = {
            'Authorization': f'Bearer {self._auth}',
            'Content-Type': 'application/json'
        }
        data = {
            'uris': [f'spotify:track:{track_id}']
        }
        response = requests.post(self.BASE_URL + url, json=data, headers=headers)
        if response.status_code == 201:
            logging.info(f"Track {track_id} added to playlist {playlist_id}")
            return response.json()
        else:
            logging.error(f"Error adding track {track_id} to playlist {playlist_id}: {response.status_code} - {response.text}")
            raise Exception(f"Error adding track {track_id} to playlist {playlist_id}: {response.status_code} - {response.text}")

    # Puerto del servidor local que escucha la redirección de Spotify.
    _SERVER_PORT = 43019

    # Clase interna para manejar el servidor de autorización.
    class _AuthorizationServer(http.server.HTTPServer):
        def __init__(self, host, port):
            http.server.HTTPServer.__init__(self, (host, port), SpotifyAPI._AuthorizationHandler)

        def handle_error(self, request, client_address):
            raise

    # Clase interna para manejar la solicitud de autorización.
    class _AuthorizationHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith('/redirect'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<script>location.replace("token?" + location.hash.slice(1));</script>')

            elif self.path.startswith('/token?'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<script>close()</script>Thanks! You may now close this window.')

                access_token = re.search('access_token=([^&]*)', self.path).group(1)
                logging.info(f'Received access token from Spotify: {access_token}')
                raise SpotifyAPI._Authorization(access_token)

            else:
                self.send_error(404)

        def log_message(self, format, *args):
            pass

    # Clase interna para manejar el token de autorización.
    class _Authorization(Exception):
        def __init__(self, access_token):
            self.access_token = access_token
