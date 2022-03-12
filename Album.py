import discogs_client
import ripper
import os
import requests

d = discogs_client.Client("album-song-finder", user_token="fzhtitURLAAQOKaUWAbBFhaeAsnlqGowVxwCEbaQ")

album = input("What is the name of the album you'd like to download?")
artist = input("Who is the artist?")
print("Pick a destination (leave blank for default)")
destination = input(">>>")

if destination == "":
    destination = "./Output"

while os.path.isdir(destination) is False:
    print("That is not a valid destination, please, input a destination:")
    destination = input(">>>")
    if destination == "":
        destination = "./Output"

results = d.search(album, artist=artist, type='release')
result = results[0]

if os.path.isdir(destination + "/" + result.title + "/") is False:
    os.mkdir(destination + "/" + result.title + "/")

n = 0

try:
    print(result.images[0])
    cover_art = requests.get(result.images[0]['resource_url']).content
    img_path = destination + "/" + result.title + "/" + result.title + ".jpg"
    with open(img_path, 'wb') as handler:
        handler.write(cover_art)
except IndexError:
    print("no image")

for i in range(len(result.tracklist)):
    print(result.tracklist[n].title)
    print(result.artists[0].name)
    print(destination)
    print(n+1)
    try:
        ripper.DownloadMusic(result.tracklist[n].title, result.artists[0].name, result.title, destination, n+1,
                             img_path, result.genres[0])
    except NameError:
        ripper.DownloadMusic(result.tracklist[n].title, result.artists[0].name, result.title, destination, n + 1,
                             "null", result.genres[0])
    n += 1

if img_path:
    os.remove(img_path)

print(result.title + " has been downloaded!")