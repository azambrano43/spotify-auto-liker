# Spotify-auto-liker

This script allows users to automatically like songs from a playlist file on Spotify using the Spotify API.

## Requirements

- Python 3.x
- Spotify Developer Account
- A Spotify Developer application configured with the necessary permissions and in production mode

## Installation

1. Clone this repository or download the files.

2. Install the necessary dependencies:
   `pip install spotipy flask`

3. Configure your application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) and obtain your `client_id`.

4. Ensure the `redirect_uri` in your application is set to `http://127.0.0.1:43019/redirect`.

5. Update the `spotify-like.py` script with your `client_id`.

## Usage

1. Create a `playlists.txt` file in the same directory as the script. The file should have the following format, with the song URLs in the fourth column, separated by tabs:
   `Column1   Column2   Column3   spotify:track:track_id`

2. Run the script:
   `python spotify-like.py playlists.txt`

3. Follow the instructions in the browser to authenticate your Spotify account and grant permissions to the application.

## Example of `playlists.txt`

Entendido, aquí tienes el README completamente en inglés y en formato Markdown:

markdown
Copiar código
# Spotify Like Bot

This script allows users to automatically like songs from a playlist file on Spotify using the Spotify API.

## Requirements

- Python 3.x
- Spotify Developer Account
- A Spotify Developer application configured with the necessary permissions and in production mode

## Installation

1. Clone this repository or download the files.

2. Install the necessary dependencies:
   `pip install spotipy flask`

3. Configure your application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/login) and obtain your `client_id`.

4. Ensure the `redirect_uri` in your application is set to `http://127.0.0.1:43019/redirect`.

5. Update the `spotify-like.py` script with your `client_id`.

## Usage

1. Create a `playlists.txt` file in the same directory as the script. The file should have the following format, with the song URLs in the fourth column, separated by tabs:
   `Column1   Column2   Column3   spotify:track:track_id`

2. Run the script:
   `python spotify-like.py playlists.txt`

3. Follow the instructions in the browser to authenticate your Spotify account and grant permissions to the application.

## Example of `playlists.txt`

Track1  Artist1  Album1  spotify:track:7CyPwkp0oE8Ro9Dd5CUDjW
Track2  Artist2  Album2  spotify:track:6rqhFgbbKwnb9MLmUQDhG6
Track3  Artist3  Album3  spotify:track:3n3Ppam7vgaVa1iaRUc9Lp


## Notes
- Each user will need to authenticate their Spotify account through the browser and grant permissions to the application.


