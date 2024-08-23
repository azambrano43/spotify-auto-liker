your_client_id = "REPLACE_THIS_WITH_YOUR_OWN_CLIENT_ID"

import argparse
import codecs
import http.client
import http.server
import json
import logging
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

class SpotifyAPI:
    # Requires an OAuth token.
    def __init__(self, auth):
        self._auth = auth

    # Gets a resource from the Spotify API and returns the object.
    def get(self, url, params={}, tries=3):
        # Construct the correct URL.
        if not url.startswith('https://api.spotify.com/v1/'):
            url = 'https://api.spotify.com/v1/' + url
        if params:
            url += ('&' if '?' in url else '?') + urllib.parse.urlencode(params)

        # Try the sending off the request a specified number of times before giving up.
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

    # Adds a track to the user's saved tracks
    def like_track(self, track_id, tries=3):
        url = 'https://api.spotify.com/v1/me/tracks?ids=' + track_id
        for _ in range(tries):
            try:
                req = urllib.request.Request(url, method='PUT')
                req.add_header('Authorization', 'Bearer ' + self._auth)
                res = urllib.request.urlopen(req)
                if res.status == 200:
                    logging.info(f"Liked track: {track_id}")
                    return
                elif res.status == 403:
                    logging.error(f"Permission denied: {res.read().decode()}")
                    return
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    logging.error(f"HTTP Error 403: Forbidden - {e.reason}")
                    logging.error(f"Response: {e.read().decode()}")
                    return
                else:
                    logging.info(f"Couldn't like track {track_id}: {e}")
                    time.sleep(2)
                    logging.info('Trying again...')
        logging.error(f"Failed to like track {track_id} after {tries} attempts")

    # Pops open a browser window for a user to log in and authorize API access.
    # Authentication method adapted from Casey Chu's repository
    # https://github.com/caseychu/spotify-backup
    @staticmethod
    def authorize(client_id, scope):
        url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode({
            'response_type': 'token',
            'client_id': client_id,
            'scope': scope,
            'redirect_uri': 'http://127.0.0.1:{}/redirect'.format(SpotifyAPI._SERVER_PORT)
        })
        logging.info(f'Logging in (click if it doesn\'t open automatically): {url}')
        webbrowser.open(url)

        # Start a simple, local HTTP server to listen for the authorization token... (i.e. a hack).
        server = SpotifyAPI._AuthorizationServer('127.0.0.1', SpotifyAPI._SERVER_PORT)
        try:
            while True:
                server.handle_request()
        except SpotifyAPI._Authorization as auth:
            return SpotifyAPI(auth.access_token)

    # The port that the local server listens on. Don't change this,
    # as Spotify only will redirect to certain predefined URLs.
    _SERVER_PORT = 43019

    class _AuthorizationServer(http.server.HTTPServer):
        def __init__(self, host, port):
            http.server.HTTPServer.__init__(self, (host, port), SpotifyAPI._AuthorizationHandler)

        # Disable the default error handling.
        def handle_error(self, request, client_address):
            raise

    class _AuthorizationHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            # The Spotify API has redirected here, but access_token is hidden in the URL fragment.
            # Read it using JavaScript and send it to /token as an actual query string...
            if self.path.startswith('/redirect'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<script>location.replace("token?" + location.hash.slice(1));</script>')

            # Read access_token and use an exception to kill the server listening...
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

        # Disable the default logging.
        def log_message(self, format, *args):
            pass

    class _Authorization(Exception):
        def __init__(self, access_token):
            self.access_token = access_token

def main():
    parser = argparse.ArgumentParser(description='Automatically like songs from a given playlist file.')
    parser.add_argument('file', help='input filename (e.g. playlists.txt)')
    parser.add_argument('separator', nargs='?', default='\t', help='separator used in the .txt file (default: tab, use "\t" for tab, "," for comma)')
    args = parser.parse_args()

    # Log into the Spotify API.
    spotify = SpotifyAPI.authorize(client_id= your_client_id, scope='user-library-modify')

    logging.info('Reading file and liking songs...')
    track_ids = []
    with open(args.file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:  # Skip the first line if it's a header
            columns = line.split(args.separator) # Use the separator provided by the user or the default
            if len(columns) >= 4:
                track_url = columns[3].strip()
                if track_url.startswith('spotify:track:'):
                    track_ids.append(track_url.split(':')[-1])

    # Like each track
    for track_id in track_ids:
        spotify.like_track(track_id)

    logging.info('Finished liking songs.')

if __name__ == '__main__':
    main()
