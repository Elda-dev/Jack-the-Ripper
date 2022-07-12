import urllib.error

import musicbrainzngs
import ripper
import os
import json

musicbrainzngs.set_useragent("MP3 Metadata Collector", "0.2")

with open("./config.json", "r", encoding="utf8") as jsonfile:
    config = json.load(jsonfile)
dest = config['default_directory']

print("What is the name of the album you'd like to download?")
album = input(">>> ")

result = musicbrainzngs.search_release_groups(album)
id_list = []

for release in result['release-group-list']:
    try:
        detail = release['disambiguation']
        if detail == " ":
            detail = ""
    except KeyError:
        detail = ""
    print(u"[{id}] - {name} {detail} by {artist}".format(id=len(id_list), name=release["title"], detail=detail,
                                                         artist=release['artist-credit'][0]['name']))
    id_list.append(release['release-list'][0]['id'])

print("Please, pick which of the above albums to download.")
choice = int(input(">>> "))

result = musicbrainzngs.get_release_by_id(id_list[choice], includes=['recordings', 'artists'])
track_list = result['release']['medium-list'][0]['track-list']

print("Pick a destination (leave blank for default, located in config.json)")
destination = input(">>> ")

if destination == "":
    destination = dest

while os.path.isdir(destination) is False:
    print("That is not a valid destination, please, input a destination:")
    destination = input(">>>")
    if destination == "":
        destination = dest

print("Downloading " + result['release']['title'] + " by " + result['release']['artist-credit'][0]['artist']['name'])

if os.path.isdir(destination + "/" + result['release']['artist-credit'][0]['artist']['name'] + "/" + result['release'][
    'title']) is False:
    os.makedirs(destination + "/" + result['release']['artist-credit'][0]['artist']['name'] + "/" + result['release'][
        'title'], exist_ok=True)

try:
    image = musicbrainzngs.get_image_front(id_list[choice])
    img_path = destination + "/" + result['release']['artist-credit'][0]['artist']['name'] + ".jpg"
    with open(img_path, 'wb') as handler:
        handler.write(image)
except:
    img_path = "null"


for track in track_list:

    title = track['recording']['title']
    title = title.replace(".", "")
    title = title.replace("/", "")
    title = title.replace(":", "")
    title = title.replace(";", "")

    try:
        ripper.download_music(title, result['release']['artist-credit'][0]['artist']['name'],
                              result['release']['title'], destination, int(track['position']),
                              img_path)
    except NameError:
        ripper.download_music(title, result['release']['artist-credit'][0]['artist']['name'],
                              result['release']['title'], destination, int(track['position']))

if img_path != "null":
    os.remove(img_path)

print(result['release']['title'] + " has been downloaded!")
