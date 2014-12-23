Reddit Code Parser
======================

Welcome. This project aims to get all kinds of code from all kinds of sources.
Currently supported are:
  images from imgur
  pastebins
  gists
Future support is meant to implement support for hastebin and other code sources.
For the image side of things, deviantart and photobucket (maybe tinypic too) are meant to be getting support.

Requirements - code_requirements.py
======================
A .py file which includes code that all the other .py files rely on.
Other than this, everything else is standard library.

Image Parsing - imageparsing.py
======================


This finds all the imgur links in a given url's HTML/JSON and saves them to file.
Currently it writes file with the subreddit + the image code + .jpg
However, this will be getting another re-work to work better with json files and have a different kind of naming pattern.
Currently supported:
  imgur
  
Pastebin Parsing - pastebinparsing.py
======================


The next couple of "Parsing" scripts are all found in codeparsing.py
This reads pastebin links from any url given and writes them with a file with name pastebin_code + given extension.
This is the next re-write, after implementing hastebin

Gist Parsing - gistparsing.py
======================


This is definitely my favorite out of the lot. ( <3 GitHub for having an awesome website + API )
This reads gists from a given url, and writes them to file.
It creates a folder if the given gist has more files.
The format is:
For folders:
  Id of the gist
For Files:
  name of the file, including extension.
More features will be added, cause <3 GitHub

Hastebin Parsing - hastebinparsing.py
======================


A parser for hastebin which takes the hastebins and puts them in a file.
Surprisingly easy to make considering that Hastebin has a rather nice API.

Future Features / To-DO
======================


~~Hastebin support~~
Reddit "markdown" support.  
Suggest in comments/anywhere more features you'd like to be added!  
