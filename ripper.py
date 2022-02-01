from pytube import YouTube
from pytube import Search
import os


def DownloadMusic(songname, destination_path, filename, author, album):
    # grabbing the video ID of the top user search
    s = Search(songname)
    results = s.results
    videoid = results[0].video_id
    # querying youtube and obtaining the video
    yt = YouTube("http://youtube.com/watch?v=" + videoid)
    # isolating audio streams of the .mp4 format
    audiostreams = yt.streams.filter(file_extension='mp4', only_audio=True)
    # sorting audio streams based on the audio quality, and finding the highest streaming quality available
    highestquality = 0
    for element in audiostreams:
        quality = int(element.abr.replace('kbps', ''))
        if quality > highestquality:
            highestquality = quality
    # obtaining the file of the highest quality
    for element in audiostreams:
        if element.abr == (str(highestquality) + 'kbps'):
            stream = yt.streams.get_by_itag(element.itag)
    # setting the output path - if none entered, use this
    # grabbing the file
    out_file = stream.download(output_path=destination_path)
    # encoding the file as a .mp3
    base, ext = os.path.splitext(out_file)
    filename = filename.replace("/", ".")
    new_file = "./Output/" + filename + '.mp3'
    os.rename(out_file, new_file)



"""song_name = input("Pick a song to download:    ")
print("Enter the destination (leave blank for current directory)")
destination = str(input(">> ")) or './Output'
DownloadMusic(song_name, destination)"""