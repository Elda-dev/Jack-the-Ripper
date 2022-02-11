from pytube import YouTube
from pytube import Search
import eyed3
from moviepy.editor import *
import os


def DownloadMusic(songname, artist, album, destination_path, filename):
    # grabbing the video ID of the top user search
    s = Search(songname + " by " + artist)
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
    pathname = yt.title
    out_file = stream.download(output_path=destination_path)
    # encoding the file as a .mp3
    mp4path = destination_path + "/" + pathname + ".mp4"
    print(mp4path)
    mp3path = destination_path + "/" + songname + ".mp3"
    print(mp3path)
    mp4_to_mp3(mp4path, mp3path)
    # adding tags
    song = eyed3.load(mp3path)
    song.initTag()
    song.tag.artist = artist
    song.tag.album = album
    print(song.tag.artist)
    print(song.tag.album)
    os.remove(mp4path)


#print(EasyID3.valid_keys.keys())

def mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close() # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")