#! /usr/bin/python3

import youtube_dl
import json
from decouple import config
import requests

# to add your yotube playlist to your spotify playlist
# note : I fnot working for you, then read the json data and find teh title of the song from it, make necessary in fetchSongs() for loop for getting title name.


class ytdSpotify:
    def __init__(self):
        self.token = config("SPOTIFY_TOKEN")
        # self.api_key = config("LAST_FM_API_KEY")
        self.user_id = config("SPOTIFY_USER_ID")
        self.playlist_id = ""
        self.spotify_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        self.dict_song = {}
        self.song_uris = []

    def fetchSongs(self):  # to get songs from lastFm
        ydl = {}

        url = "https://www.youtube.com/watch?v=yN_5jNxM0CU&list=PL-blrpNXfQykSPe9nAaWxRasjyvQYhLuk"
        result = youtube_dl.YoutubeDL(ydl).extract_info(f"{url}", download=False)

        for i in result["entries"][0]["chapters"]:
            song = i["title"]
            print(i["title"])
            artist = i["title"]
            self.dict_song[song] = artist
        print(song, " ", artist, "\n")

        print("GETTING SONGS URI\n")
        self.get_uri_from_spotify()
        print("ADDING SONGS\n")
        self.add_songs_to_spotify_playlist()
        print("SONGS ADDED\n")
        self.list_song_in_playlist()

    def get_uri_from_spotify(self):
        for song, artist in self.dict_song.items():
            # print(song, "- -", artist)
            # url_ = f"https://api.spotify.com/v1/search?query=track%3A{song}+artist%3A{artist}&type=track&offset=0&limit=10"   # when both artist and song name known

            url_ = f"https://api.spotify.com/v1/search?query=track%3A{song}&type=track&offset=0&limit=10"

            response_spotify = requests.get(url_, headers=self.spotify_headers)

            print(response_spotify.status_code)

            if response_spotify.status_code != 200:
                print("ERROR CONNECTINGF SPOTIFY")
                print("SUCCESS CONNECTED SPOTIFY")

            spotify_json_format = response_spotify.json()

            tracks_ = json.dumps(spotify_json_format, indent=4)

            print("Spotify")
            print(tracks_)
            uri = spotify_json_format["tracks"]["items"][0]["uri"]
            print(uri, "\n\n uri ")
            self.song_uris.append(uri)

    def add_songs_to_spotify_playlist(self):
        song_list = json.dumps(self.song_uris)
        self.playlist_id = "6jCbbKXJYMOeZx8TiNNimk"
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"

        add_list_song = requests.post(url, data=song_list, headers=self.spotify_headers)
        if add_list_song.status_code == 201:
            print("ADDED SONGS SUCCESSFULLY")
        else:
            print("Error")

    def list_song_in_playlist(self):
        url_ = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        response_ = requests.get(url_, headers=self.spotify_headers)
        json_response = response_.json()
        if response_.status_code == 201 or response_.status_code == 200:
            print("SUCCESS")
            for item in json_response["items"]:
                print(item["track"]["name"])

        else:
            print("ERROR")


add_songs = ytdSpotify()
add_songs.fetchSongs()
