import csv
import ripper
import os
import requests
import discogs_client
import json

blacklisted_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", "/", " "]
d = discogs_client.Client("album-song-finder", user_token="fzhtitURLAAQOKaUWAbBFhaeAsnlqGowVxwCEbaQ")


def downloadcsv(input_csv, local_destination):
    csvlist = []
    with open(input_csv, newline='', encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            csvlist.append(row)
        for row in csvlist:
            if row[4] != "Album" and row[0] != "Track name":

                dl = True

                try:
                    results = d.search(row[0], artist=row[1], track=row[0], type='release')

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
                            img_path = local_destination + "/" + result.title + ".jpg"
                            with open(img_path, 'wb') as handler:
                                handler.write(cover_art)
                            print("Found cover art")
                        except IndexError:
                            print("no image")

                    n = 0

                    print(len(result.tracklist))

                    for i in range(len(result.tracklist)):
                        print("Downloading " + result.tracklist[n].title + " by " + row[1] + " to " + local_destination)

                        try:
                            ripper.DownloadMusic(row[0], row[1], row[2], local_destination, n + 1,
                                                 img_path, result.genres[0])
                        except NameError:
                            ripper.DownloadMusic(row[0], row[1], row[2], local_destination, n + 1,
                                                 "null", result.genres[0])
                        n += 1

                    if img_path:
                        os.remove(img_path)

                    print(song_name + " has been downloaded!")
                except:
                    continue


with open("./config.json", "r", encoding="utf8") as jsonfile:
    config = json.load(jsonfile)
dest = config['default_directory']

print("Pick a destination (leave blank for default)")
destination = input(">>> ")

if destination == "":
    destination = dest

while os.path.isdir(destination) is False:
    print("That is not a valid destination, please, input a destination:")
    destination = input(">>>")
    if destination == "":
        destination = "./Output"

csv_path = input("csv file name:")
downloadcsv(csv_path, destination)
