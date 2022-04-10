import ripper
import os
import musicbrainzng
import request
import json

with open("./config.json", "r", encoding="utf8") as jsonfile:
    config = json.load(jsonfile)
dest = config['default_directory']

blacklisted_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", "/", " "]
d = discogs_client.Client("album-song-finder", user_token="fzhtitURLAAQOKaUWAbBFhaeAsnlqGowVxwCEbaQ")

print("What is the name of the song you'd like to download?")
song_name = input(">>> ")
print("Who is it by? (artist name)")
artist = input(">>> ")
print("Pick a destination (leave blank for default)")
destination = input(">>> ")

if destination == "":
    destination = dest

while os.path.isdir(destination) is False:
    print("That is not a valid destination, please, input a destination:")
    destination = input(">>>")
    if destination == "":
        destination = "./Output"