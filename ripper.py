from pytube import YouTube
from pytube import Search
import eyed3
from moviepy.editor import *
import os


def DownloadMusic(songname, artist, album, destination_path="./Output", songid=-1, coverartpath="null", genre="null"):
    # grabbing the video ID of the top user search
    s = Search(artist + " " + songname)
    results = s.results
    videoid = results[0].video_id
    # querying youtube and obtaining the video
    yt = YouTube("http://youtube.com/watch?v=" + videoid)
    print(yt)
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
    out_file = stream.download(output_path=destination_path, filename="newdownload.mp4")
    # encoding the file as a .mp3
    print(destination_path)
    mp4path = destination_path + "/newdownload.mp4"
    print(mp4path)
    if os.path.isdir(destination_path + "/" + artist + "/" + album + "/") is False:
        os.makedirs(destination_path + "/" + artist + "/" + album + "/", exist_ok=True)
    mp3path = destination_path + "/" + artist + "/" + album + "/" + songname + ".mp3"
    print(mp3path)
    mp4_to_mp3(mp4path, mp3path)
    # adding tags
    song = eyed3.load(mp3path)
    song.initTag()
    song.tag.artist = artist
    song.tag.album = album
    if songid != -1:
        song.tag.track_num = songid
    if coverartpath != "null":
        song.tag.images.set(0, open(coverartpath, 'rb').read(), 'image/jpeg')
        song.tag.images.set(3, open(coverartpath, 'rb').read(), 'image/jpeg')
    if genre != "null":
        song.tag.genre = genre
    song.tag.save(version=eyed3.id3.ID3_V2_3)
    print(song.tag.artist)
    print(song.tag.album)
    os.remove(mp4path)


def mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close()  # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
