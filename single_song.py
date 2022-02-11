import ripper

song_name = input("Pick a song to download:    ")
print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or './Output'
ripper.DownloadMusic(song_name, destination, song_name)
