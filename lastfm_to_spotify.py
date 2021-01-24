#! /usr/bin/python3

import json
from decouple import config
import requests
import sys


class lastFmSpotify:
    def __init__(self):
        self.token = config("SPOTIFY_TOKEN")
        self.api_key = config("LAST_FM_API_KEY")
        self.user_id = config("SPOTIFY_USER_ID")
        self.playlist_id = ""
        self.spotify_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        self.dict_song = {}
        self.song_uris = []

    def fetchSongs(self):  # to get songs from lastFm
        params = {"limit": 1, "api_key": self.api_key}
        url = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&format=json"
        response_lastfm = requests.get(url, params=params)
        if response_lastfm.status_code != 200:
            print("ERROR")
            self.exceptionalExceptions(
                response_lastfm.status_code, response_lastfm.text()
            )

        json_format = response_lastfm.json()
        # tracks_ = json.dumps(json_format, indent=4)

        for item in json_format["tracks"]["track"]:
            song = item["name"]
            artist = item["artist"]["name"]
            print(song, artist, "\n")
            self.dict_song[song] = artist
        print("GETTING SONGS URI\n")
        self.get_uri_from_spotify()
        self.create_spotfiy_playlist()
        print("PLAYLIST CREATED\n")
        print("ADDING SONGS\n")
        self.add_songs_to_spotify_playlist()
        print("SONGS ADDED\n")
        self.list_song_in_playlist()

    def get_uri_from_spotify(self):
        for song, artist in self.dict_song.items():
            # print(song, "- -", artist)
            url_ = f"https://api.spotify.com/v1/search?query=track%3A{song}+artist%3A{artist}&type=track&offset=0&limit=10"

            response_spotify = requests.get(url_, headers=self.spotify_headers)

            # print(response_spotify.status_code)

            if response_spotify.status_code != 200:
                print("ERROR CONNECTINGF SPOTIFY")
                self.exceptionalExceptions(
                    response_spotify.status_code, response_spotify.text()
                )

                # print("SUCCESS CONNECTED SPOTIFY")

            spotify_json_format = response_spotify.json()

            # tracks_ = json.dumps(spotify_json_format, indent=4)

            # print("Spotify")
            # print(tracks_)
            uri = spotify_json_format["tracks"]["items"][0]["uri"]
            # print(uri, "\n\n uri ")
            self.song_uris.append(uri)

    def create_spotfiy_playlist(self):
        data = {
            "name": "API Last_FM top charts",
            "description": "songs via API",
            "public": False,
        }

        data = json.dumps(data)
        url_ = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response_create_spotify = requests.post(
            url_, data=data, headers=self.spotify_headers
        )
        # print(response_create_spotify.status_code)

        if response_create_spotify.status_code == 201:

            json_id = response_create_spotify.json()
            # print("JSONID = ", json_id["id"])
            self.playlist_id = json_id["id"]

            print("SPOTIFY PLAYLIST CREATED!, ID = ", self.playlist_id)
        else:
            print("error creating playlist")
            self.exceptionalExceptions(
                response_create_spotify.status_code, response_create_spotify.text()
            )

    def add_songs_to_spotify_playlist(self):
        song_list = json.dumps(self.song_uris)

        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"

        add_list_song = requests.post(url, data=song_list, headers=self.spotify_headers)
        if add_list_song.status_code == 201:
            print("ADDED SONGS SUCCESSFULLY")
        else:
            print("ERror")
            self.exceptionalExceptions(add_list_song.status_code, add_list_song.text())

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
            self.exceptionalExceptions(json_response.status_code, json_response.text())

    def exceptionalExceptions(self, status_code, err):
        print("EXCEPTION OCCURRED with status_code = ", status_code)
        print("ERROR:", err)

        sys.exit(0)


if __name__ == "__main__":
    add_songs = lastFmSpotify()
    add_songs.fetchSongs()
