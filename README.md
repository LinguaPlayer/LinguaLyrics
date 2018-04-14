# Lingua Lyrics

Lingua Lyrics is a linux app that communicates with your music player to get the current song and then shows the lyric.

![screenshot](./LinguaRepo/assets/screenshot.png)

## How Lingua lyrics works
  Lingua lyrics gets the title and artist from your music player and searchs for its lyric
## My audio file doesn't have correct title and artist
  Lingua lyrics can find the correct title and artist using acoustic fingerprinting
## INSTALLING Lingua Lyrics

Just type:

	sudo python3 ./setup.py install

## UNINSTALLING Lingua Lyrics

Just type:

	sudo python3 ./uninstall.py

## Tested players

### clementine
	Completely supported
	
### vlc
	Completely supported

### smplayer
	Partially supported:
		music slider not works
		volume slider not works
	
### deepinmusic
	Partially supported:
		music slider not works
		pause button also mutes the player
### gnome-music
	Not supported yet
	
### rhythmbox
	Not supported yet
	
### audacious
	Not supported yet
	
## spotify
	Not supported yet
	
## TODO
- [x] GUI
- [x] Package the app
- [ ] Search in multiple lyric sources
- [x] Test with other player like VLC, Smplayer, Rhythmbox, Spotify,...
- [ ] Translation of words 
- [x] Find correct lyric with audio fingerprint
- [ ] Show all available lyrics and choose between them
- [ ] Download the cover art
- [ ] Offline view


## License

GNU General Public License v3.0

LinguaLyrics icon made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

Copyright © 2018, Habib Kazemi
