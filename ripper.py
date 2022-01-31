from pytube import YouTube
from pytube import Search

s = Search("Never gonna give you up")
results = s.results
videoid = results[0]
videoid = videoid.video_id

yt = YouTube("http://youtube.com/watch?v=" + videoid)
audiostreams = yt.streams.filter(file_extension='mp4', only_audio=True)
highestquality = 0
for element in audiostreams:
    quality = int(element.abr.replace('kbps', ''))
    if quality > highestquality:
        highestquality = quality
for element in audiostreams:
    if element.abr == (str(highestquality) + 'kbps'):
        stream = yt.streams.get_by_itag(element.itag)
        stream.download()
