# Spotify Liker

This project is a script that automatically likes songs on Spotify.

## Prerequisites

Install python necessary dependencies:
    
    pip install spotipy flask

Before using this script, you need a `.txt` file with a list of your songs. You can find a program that creates this file, such as `spotify-backup.py`, created by [caseychu](https://github.com/caseychu) in  their [GitHub repository](https://github.com/caseychu/spotify-backup/tree/master).

Your .txt file of your songs should look like this:

tr01_name‎‎ ‎ ‎ ‎ tr01_artists‎‎ ‎ ‎ ‎ tr01_album‎‎ ‎ ‎ ‎ tr01_uri‎‎ ‎ ‎ ‎ tr01_release_date  
tr02_name‎‎ ‎ ‎ ‎ tr02_artists‎‎ ‎ ‎ ‎ tr02_album‎‎ ‎ ‎ ‎ tr02_uri‎‎ ‎ ‎ ‎ tr02_release_date  
tr03_name‎‎ ‎ ‎ ‎ tr03_artists‎‎ ‎ ‎ ‎ tr03_album‎‎ ‎ ‎ ‎ tr03_uri‎‎ ‎ ‎ ‎ tr03_release_date  
   
## Usage

1. Generate a `.txt` file with your songs using `spotify-backup.py` or a similar tool.
2. Place the `.txt` file in the same directory as `spotify-liker.py`.
3. Run the `spotify-liker.py` script to automatically like the songs on Spotify.

You can run the script from the command line:

    python spotify-liker.py playlist_name.txt

By default, it assumes that the attributes of each song in your .txt are tab separated, if this is not the case, you can include the separator it uses:

    python spotify-liker.py playlist_name.txt ","
    python spotify-liker.py playlist_name.txt ";"

## Notes
- Each user will need to authenticate their Spotify account through the browser and grant permissions to the application to work.

## Acknowledgements

I would like to express my gratitude to [caseychu](https://github.com/caseychu) for the authentication method used in `spotify-backup.py`, which was adapted for use in this project. Additionally, I sincerely thank [caseychu](https://github.com/caseychu) for their work and apologize for using their Spotify Developer client ID. Please rest assured that it was used with the best of intentions and only for the purposes of this project.




