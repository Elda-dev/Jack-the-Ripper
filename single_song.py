import musicbrainzngs
import ripper
import os
import json

musicbrainzngs.set_useragent("testing metadata finder", "0.1")

with open("./config.json", "r", encoding="utf8") as jsonfile:
    config = json.load(jsonfile)
dest = config['default_directory']

print("What is the name of the song you'd like to download?")
album = input(">>> ")

result = musicbrainzngs.search_recordings(query=album, limit=50, offset=None, strict=False)

id_list = []

for release in result['recording-list']:
    try:
        detail = release['disambiguation']
        if detail == " ":
            detail = ""
    except KeyError:
        detail = ""
    print(u"[{id}] - {name} {detail} by {artist}".format(id=len(id_list), name=release["title"], detail=detail,
                                                         artist=release['artist-credit'][0]['name']))
    id_list.append(release['id'])

print("Please, pick which of the above songs to download.")
choice = int(input(">>> "))

recording = musicbrainzngs.get_recording_by_id(id_list[choice], includes=['releases', 'artists'])

album = musicbrainzngs.get_release_by_id(recording['recording']['release-list'][0]['id'],
                                         includes=['recordings', 'artists'])

print("Would you like to download the whole album? (Y/N)")
download_album = input(">>> ")

answers = ["Y", "y", "N", "n"]

while download_album not in answers:
    print("That is an invalid input, would you like to download the whole album? (Y/N)")
    download_album = input(">>> ")

if download_album.lower() == "y":
    download_album = True
else:
    download_album = False

print("Pick a destination (leave blank for default, located in config.json)")
destination = input(">>> ")

if destination == "":
    destination = dest

while os.path.isdir(destination) is False:
    print("That is not a valid destination, please, input a destination:")
    destination = input(">>>")
    if destination == "":
        destination = dest

if download_album:  # Download the whole album, very similar to Album.py

    track_list = album['release']['medium-list'][0]['track-list']

    print("Downloading " + album['release']['title'] + " by " + album['release']['artist-credit'][0]['artist'][
        'name'])

    if os.path.isdir(
            destination + "/" + album['release']['artist-credit'][0]['artist']['name'] + "/" + album['release'][
                'title'] + "/") is False:
        os.makedirs(
            destination + "/" + album['release']['artist-credit'][0]['artist']['name'] + "/" + album['release'][
                'title'] + "/", exist_ok=True)

    try:
        image = musicbrainzngs.get_image_front(album['release']['id'])
        img_path = destination + "/" + album['release']['artist-credit'][0]['artist']['name'] + ".jpg"
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
            ripper.download_music(title, album['release']['artist-credit'][0]['artist']['name'],
                                  album['release']['title'], destination, int(track['position']),
                                  img_path)
        except NameError:
            ripper.download_music(title, album['release']['artist-credit'][0]['artist']['name'],
                                  album['release']['title'], destination, int(track['position']))

    print(album['release']['title'] + " has been downloaded!")


else:  # Don't download album, only the song

    print("Downloading " + recording['recording']['title'] + " by " +
          recording['recording']['artist-credit'][0]['artist'][
              'name'])

    if os.path.isdir(
            destination + "/" + recording['recording']['artist-credit'][0]['artist']['name'] + "/" +
            album['release']['title'] + "/") is False:
        os.makedirs(
            destination + "/" + recording['recording']['artist-credit'][0]['artist']['name'] + "/" +
            album['release']['title'] + "/", exist_ok=True)

    try:
        image = musicbrainzngs.get_image_front(album['release']['id'])
        img_path = destination + "/" + recording['recording']['artist-credit'][0]['artist']['name'] + ".jpg"
        with open(img_path, 'wb') as handler:
            handler.write(image)
    except:
        img_path = "null"

    track_position = 0

    for element in album['release']['medium-list'][0]['track-list']:
        if element['recording']['id'] == recording['recording']['id']:
            track_position = element['position']
            break

    title = recording['recording']['title']
    title = title.replace(".", "")
    title = title.replace("/", "")
    title = title.replace(":", "")
    title = title.replace(";", "")

    try:
        ripper.download_music(title, recording['recording']['artist-credit'][0]['artist']['name'],
                              album['release']['title'], destination, track_position,
                              img_path)
    except NameError:
        ripper.download_music(title, recording['recording']['artist-credit'][0]['artist']['name'],
                              album['release']['title'], destination, track_position)

    print(title + " has been downloaded!")

if img_path != "null":
    os.remove(img_path)
