Tournament Database
===================

This is a python program to act as a backend for a tournament.

Table of Contents
 -Requirements
 -Installation/Setup
 -Extra Credit
 -Changelog
 -Comments

Requirements
------------
Python [Required] - Designed for 2.7, though it may work on others.
 -see https://www.python.org/downloads/ for download.
psycopg2 [Required] - A Python Module to connect with PostgreSQL.
 -see http://initd.org/psycopg/docs/install.html#installation for installation instructions.
PostgreSQL [Required] - A SQL Implementation.
 -see http://www.postgresql.org/download/ for download

Installation/Setup
------------------
 -Place the TournamentDatabase folder somewhere on the computer
 -To set up the database, navigate to the folder with Terminal (Or Equivalent) and run "psql"
 -Once in psql, run the command "\i tournament.sql". This will create the database and set up the tables.
 -Once the command finishes, exit psql by running "\q" or pressing Control-D
 -The tournament backend is now ready to function. You can test it by running the tournament_test file.
   -To run through command line/terminal, navigate to the TournamentProject folder and run "Python tournament_test.py".
   -To run on Windows, right click tournament_test.py and select open with Python.exe.
 -To make use of the backend, run "Python" in the command line while in the TournamentProject folder.
 -While in python, run either "import tournament" or "from tournament import *"
   -importing tournament directly requires the functions to be given as "tournament.[functionname]"
   -importing all functions means they can be run directly as "[functionname]"
 -For information on the functions, run "import tournament" and "help(tournament)"
   -"help([Functionname])" will show the help entry for a function again


Extra Credit
------------
Support for multiple tournaments as well as matches ending in a draw are in extratournament.py. Use is the same as the regular tournament.py. Simply type "import extratournament" instead.
Here is a summary of the changed functions:
 -deleteMatches replaced with deleteTournament, which removes a tournament's records.
 -listPlayers and listTournaments, to simply list the entries. listPlayers can be narrowed by tournament.
 -registerTournament, to create new tournaments.
 -addPlayer adds a given player to a tournament, allowing them to participate.
 -reportMatch now takes four arguments, to specify the tournament and players involved, as well as the result of the match.
 -playerStandings now shows draws in addition to wins.
 -swissStandings gives players sorted by points. 3 points for a win, 1 for a draw.
 -siwssPairings uses swissStandings for more accurate pairings.
 -countPlayers and playerStandings now can optionally be given a tournament id.


Changelog
---------
Version 1.0
-First Submitted Version.

Comments
--------
SQL Can be really annoying at times. Once you get the hang of how to setup the tables though, it is very useful.
Implementing the Draws was the hardest part. The current method has a distinction between being the first player listed or the second. While that may not be useful in all tournaments, for some it allows useful searching. Chess Tournaments typically try to balance matches spent as white and black, and a count of how often a player is in first or second slot could be used to do that.
