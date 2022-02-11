import ripper

song_name = input("Pick a song to download:    ")
artist = input("What artist is the song by?: ")
album = input("What album is it from?: ")
print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or './Output'
ripper.DownloadMusic(song_name, artist, album, destination, song_name)
