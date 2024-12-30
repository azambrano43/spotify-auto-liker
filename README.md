# Spotify Auto Backup-Restore

Spotify Auto Backup-Restore es una aplicación que te permite respaldar y restaurar tus canciones y playlists en Spotify, utilizando la API de Spotify y Flask para una interfaz interactiva.

## Instalación

1. **Instalar dependencias**  
   Ejecuta el siguiente comando para instalar todas las dependencias necesarias:

       python -m pip install -r requirements.txt

## Autenticación

El proyecto utiliza el método de autenticación de la API de Spotify adaptado del script `spotify-backup.py` de [caseychu](https://github.com/caseychu).

## Funcionalidades

### 1. Respaldo de Canciones y Playlists

- Guarda todas las canciones que te gustan y todas tus playlists en un archivo `.txt`.
- El archivo `.txt` generado contiene la siguiente información para cada canción: nombre, artistas, y URI.
- Adicionalmente guarda una línea indicando si la canción pertenece a una playlist o a las canciones que te gustan.

### 2. Restauración de Canciones y Playlists

- Usa el archivo `.txt` generado en el respaldo para restaurar tus canciones y playlists en Spotify.
- El programa automáticamente dará "like" a las canciones y recreará las playlists con su contenido original.

## Uso

### Ejecutar la aplicación

Inicia la aplicación Flask con el siguiente comando:

    python run.py

## Interfaz de usuario

Después de ejecutar el comando, la aplicación se ejecutará en el navegador. Desde la interfaz podrás:

- Realizar un respaldo de tus canciones y playlists en un archivo `.txt`.
- Restaurar tus canciones y playlists desde un archivo `.txt`.

## Notas

- Es necesario autenticar tu cuenta de Spotify a través del navegador y otorgar permisos a la aplicación.
- El método de autenticación de spotify utilizado en este proyecto fue adaptado de [caseychu](https://github.com/caseychu).

