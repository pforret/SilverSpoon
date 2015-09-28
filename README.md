# SilverSpoon
Set up an API for Raspberry Pi, based on a simple .INI config file


## Required files

* SilverSpoon.py - the program
* config/services.ini - the config file

## Start

* python SilverSpoon.py

## INI Syntax
	
	;; will be available as /dothis?file=example.mp4
	[dothis]
	;; start command in this folder
	folder=/var/video
	;; define default value for variables
	file=test.mp4
	;; command to execute in shell
	command="omxplayer {file}"