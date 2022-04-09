import ripper
import discogs_client
import os
import requests
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

results = d.search(song_name, artist=artist, track=song_name, type='release')

dl = True

try:
    result = results[0]
    print("Found song")
except IndexError:
    print("No album found that corresponds with this song!")
    ripper.DownloadMusic(row[0], row[1], row[2])
    dl = False

if dl:
    try:
        cover_art = requests.get(result.images[0]['resource_url']).content
        img_path = destination + "/" + result.title + ".jpg"
        with open(img_path, 'wb') as handler:
            handler.write(cover_art)
        print("Found cover art")
    except IndexError:
        print("no image")

    name = str(result.artists[0].name)

    for letter in blacklisted_characters:
        name = name.replace(letter, "")



    n = 0

    for i in range(len(result.tracklist)):
        if song_name.strip().lower() in result.tracklist[n].title.strip().lower():

            print("Downloading " + result.tracklist[n].title + " by " + name + " to " + destination)

            try:
                ripper.DownloadMusic(result.tracklist[n].title, name, result.title, destination, n+1,
                                     img_path, result.genres[0])
            except NameError:
                ripper.DownloadMusic(result.tracklist[n].title, name, result.title, destination, n + 1,
                                     "null", result.genres[0])
        n += 1

    if img_path:
        os.remove(img_path)

print(song_name + " has been downloaded!")