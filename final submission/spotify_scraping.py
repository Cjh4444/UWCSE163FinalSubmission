import base64
import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv
import time

load_dotenv()

CLIENT_ID: str = os.getenv("CLIENT_ID")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")


def get_token():
    """
    Grabs session token from Spotify API using client id and secret key
    Returns:
        str: token for api authentication
    """
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token: str):
    """
    Converts session token to header to be used for API calls

    Args:
        token (str): session token

    Returns:
        str: header string
    """
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    """
    Searches Spotify's database and returns the artist id associated
    with the provided name

    Args:
        token (str): session token
        artist_name (str): name of artist to search for

    Returns:
        str: Spotify id for given artist
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    time.sleep(0.4)
    return json_result[0]


def get_artist_top_songs(token, artist_id):
    """
    Returns the top 10 tracks for a given artist

    Args:
        token (str): session token
        artist_id (str): Spotify artist ID

    Returns:
        list[dict]: list of 10 songs with relevant statistics
    """
    url = (
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    )
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    # print(result.headers["Retry-After"])
    json_result = json.loads(result.content)["tracks"]
    time.sleep(0.5)
    return json_result


def get_track_features(token, track_id) -> dict:
    """
    Returns track features of a given song

    Args:
        token (str): session token
        track_id (str): Spotify track ID

    Returns:
        dict: dictionary all track features of a song
    """
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    # print(result.headers)
    json_result: dict = json.loads(result.content)
    json_result.pop("uri")
    json_result.pop("track_href")
    json_result.pop("analysis_url")
    time.sleep(0.5)
    return json_result


def get_track_analysis(token, track_id) -> dict:
    """
    Returns track analysis of a given song

    Args:
        token (str): session token
        track_id (str): Spotify track ID

    Returns:
        dict: dictionary all track analysis of a song
    """
    url = f"https://api.spotify.com/v1/audio-analysis/{track_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result: dict = json.loads(result.content)

    important_data: dict = json_result["track"]

    drop_keys = [
        "duration",
        "loudness",
        "tempo",
        "num_samples",
        "sample_md5",
        "offset_seconds",
        "window_seconds",
        "analysis_sample_rate",
        "analysis_channels",
        "end_of_fade_in",
        "start_of_fade_out",
        "codestring",
        "code_version",
        "echoprintstring",
        "echoprint_version",
        "synchstring",
        "synch_version",
        "rhythmstring",
        "rhythm_version",
    ]

    for key in drop_keys:
        important_data.pop(key)

    time.sleep(0.4)
    return important_data


def main():
    """
    Searches for and creates a csv of all top 100 artist ids,
    and then creates a csv of the top 1000 songs with all
    relevant details for analysis
    """
    token = get_token()

    with open("artists.csv") as f:
        top_1000_songs = []
        for artist in f:
            artist_id = search_for_artist(token, artist.strip())["id"]
            for song in get_artist_top_songs(token, artist_id):
                top_1000_songs.append(song["id"])
            print(f"{artist.strip()} completed")
        df = pd.DataFrame(top_1000_songs)
        df.to_csv("top1000songs.csv", index=False)

    with open("top1000songs.csv") as f:
        output = []
        for idx, song in enumerate(f):
            track_info = get_track_features(token, song.strip())
            track_info.update(get_track_analysis(token, song.strip()))
            output.append(track_info)

            print(f"{song} completed")

            if (idx % 100) == 0:
                df = pd.DataFrame(output)
                df.to_csv("1000songdata.csv", index=False)


if __name__ == "__main__":
    main()
