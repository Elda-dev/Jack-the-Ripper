# Jack the Ripper

Who knew sailing the seven seas would come with this level of privacy and comfort? Jack the Music Man is a simple database-driven audio downloader designed to work with a Jellyfin media server.

To run it, you will need the following dependancies:

- `musicbrainzngs`
- `pytube`
- `eye3d`
- `moviepy`

`single_song.py` and `Album.py` work standalone, simply enter credentials and if they exist within the database, it will do it's best to download them to the specified output folder.  Do not run `ripper.py` as this simply houses functions which the other files use.

`csv_crawler.py` requires a specific CSV format: 

**Track Name** - **Artist Name** - **Album** - **Playlist Name**

At the moment **Playlist Name** is not in use, but the other categories are required for `csv_crawler.py` to work properly. This is the same format as exported by [Tune my Music](https://www.tunemymusic.com/Spotify-to-File.php), so if you'd like to move from Spotify to Jellyfin, this tool may be able to help.

If you'd like to change the default path that `single_song.py`, ` Album.py`, and `csv_crawler.py` save to, you can do so in `config.json`
