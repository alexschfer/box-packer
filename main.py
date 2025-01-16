from sys import exit
import random, sqlite3, os, sys

spacer = "    "

ascii_art = r'''
                            ___           ___            ___         ___           ___           ___           ___           ___
             _____         /\  \         /|  |          /\  \       /\  \         /\__\         /|  |         /\__\         /\  \
            /::\  \       /::\  \       |:|  |         /::\  \     /::\  \       /:/  /        |:|  |        /:/ _/_       /::\  \
           /:/\:\  \     /:/\:\  \      |:|  |        /:/\:\__\   /:/\:\  \     /:/  /         |:|  |       /:/ /\__\     /:/\:\__\
          /:/ /::\__\   /:/  \:\  \   __|:|__|       /:/ /:/  /  /:/ /::\  \   /:/  /  ___   __|:|  |      /:/ /:/ _/_   /:/ /:/  /
         /:/_/:/\:|__| /:/__/ \:\__\ /::::\__\_____ /:/_/:/  /  /:/_/:/\:\__\ /:/__/  /\__\ /\ |:|__|____ /:/_/:/ /\__\ /:/_/:/__/___
         \:\/:/ /:/  / \:\  \ /:/  / ~~~~\::::/___/ \:\/:/  /   \:\/:/  \/__/ \:\  \ /:/  / \:\/:::::/__/ \:\/:/ /:/  / \:\/:::::/  /
          \::/_/:/  /   \:\  /:/  /      |:|~~|      \::/__/     \::/__/       \:\  /:/  /   \::/~~/~      \::/_/:/  /   \::/~~/~~~~
           \:\/:/  /     \:\/:/  /       |:|  |       \:\  \      \:\  \        \:\/:/  /     \:\~~\        \:\/:/  /     \:\~~\
            \::/  /       \::/  /        |:|__|        \:\__\      \:\__\        \::/  /       \:\__\        \::/  /       \:\__\
             \/__/         \/__/         |/__/          \/__/       \/__/         \/__/         \/__/         \/__/         \/__/
'''

def main():
    # Welcome Promt
    print(
ascii_art,
'''
 ========================================================= Welcome to BoxPacker 1.0 =========================================================

    BoxPacker is a utility designed to streamline the process of rebuilding folders of playlists in the Rekordbox database.
    It accepts a folder containing downloaded playlists, which may include copies of the same tracks across multiple playlists.
    The program scans Rekordbox’s existing track list to identify matching songs,
    then searches for the associated playlists or creates and rebuilds them in the Rekordbox database.

    Note that the tracks must already be imported into Rekordbox prior to running the program,
    ensuring that BoxPacker can properly link the songs to their respective playlists.

    This tool simplifies the integration of Playlist folders into Rekordbox by automating playlist creation, organization, and song matching.
''')

    # Prompt the user for the playlists path
    playlists_path = input(spacer +
'''
    Example file structure

    Downloads
    |
    |-- Playlist_A
    |   |-- Track_1.flac  <- Redundant Copy
    |   |-- Track_2.flac
    |
    |-- Plalyist_B
    |   |-- Track_3.flac
    |   |-- Track_1.flac  <- Redundant Copy
    v   |-- Track_4.flac

''' + "    Path to Downloaded Playlists: ").strip()
    check_directory(playlists_path)

    db_path = input(spacer + "Path to recordbox3.db Database file: ").strip()
    check_file(db_path)
    check_sqlite_db(db_path)

    playlists = collect_tracks_from_playlists(playlists_path)
    print(playlists.keys)


def collect_tracks_from_playlists(playlist_folder_path):
    playlist_tracks = {}  # Dictionary to store playlist names and their tracks

    # Loop through all directories (playlists) inside the playlist folder
    for playlist_name in os.listdir(playlist_folder_path):
        playlist_path = os.path.join(playlist_folder_path, playlist_name)

        # Check if it's a directory (playlist)
        if os.path.isdir(playlist_path):
            tracks = []  # List to store track file names in this playlist

            # Loop through all files in the playlist directory
            for track in os.listdir(playlist_path):
                track_path = os.path.join(playlist_path, track)

                # Check if it's a valid track file (by file extension, you can modify this list)
                if os.path.isfile(track_path) and track.lower().endswith(('.mp3', '.wav', '.flac', '.aiff', '.m4a')):
                    tracks.append(track)

            # If there are tracks in the playlist, add them to the dictionary
            if tracks:
                playlist_tracks[playlist_name] = tracks

    return playlist_tracks

# Function to check if the path is a valid directory
def check_directory(path):
    if not os.path.isdir(path):
        print(f"Error: The path {path} is not a valid directory.")
        sys.exit()
        return False
    return True

# Function to check if the path is a valid file
def check_file(path):
    if not os.path.isfile(path):
        print(f"Error: The path {path} is not a valid file.")
        sys.exit()
        return False
    return True

# Function to check if the Rekordbox DB file is a valid SQLite database
def check_sqlite_db(path):
    try:
        conn = sqlite3.connect(path)
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error: The file at {path} is not a valid SQLite database.")
        sys.exit()
        return False

if __name__ == "__main__":
    main()
