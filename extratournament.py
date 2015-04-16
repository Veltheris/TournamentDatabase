#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
"""
Extra Credit Implementation of a Swiss-system tournament - Includes support for multiple tournaments + draws
"""
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteTournament(tid):
    """Remove all records for the given tournament from the database.

    Args:
      tid: The id of the tournament. set to 'all' to delete all matches.
    """
    db = connect()
    c = db.cursor()
    #If tid is 'all', delete all matches.
    if tid=='all':
        c.execute('DELETE FROM tournmatches *;')
        c.execute('DELETE FROM tournplayers *;')
        c.execute('DELETE FROM tournaments *;')
    #Otherwise, delete all matches from that tournament.
    else:
        c.execute('DELETE FROM tournmatches * where tid = %s;', (tid,))
        c.execute('DELETE FROM tournplayers * where tid = %s;', (tid,))
        c.execute('DELETE FROM tournaments * where tid = %s;', (tid,))
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    #Delete all entries in players
    c.execute('DELETE FROM players *;')
    db.commit()
    db.close()

def listTournaments():
    """List all Registered Tournaments."""
    db = connect()
    c = db.cursor()    
    #list all of the tournaments.
    c.execute("SELECT * FROM tournaments;")
    return c.fetchall()
    db.close()

def listPlayers(tid='all'):
    """List all Players in the Players Registry.

    Args:
      tid: [Optional] The id of the tournament to count. Leave blank for global registry.
    """
    db = connect()
    c = db.cursor()    
    #If tid='all', list all players
    if tid=='all':
        c.execute("SELECT * FROM players;")
    #otherwise, select all of a given tournaments players.
    else:
        c.execute("SELECT players.id, players.name FROM players, tournplayers WHERE players.id = tournplayers.pid AND tid = %s;",(tid,))
    return c.fetchall()
    db.close()

def registerTournament(name, description):
    """Adds a tournament to the database.
  
    Args:
      name: the name of the tournament (need not be unique).
      description: a short description of the tournament (need not be unique).
    """
    db = connect()
    c = db.cursor()    
    #insert the tournament into the table. It's id is assigned automatically
    c.execute("INSERT INTO tournaments(tournament, description) values (%s,%s);", (name, description))
    db.commit()
    db.close()

def countPlayers(tid='all'):
    """Returns the number of players currently registered.

    Args:
      tid: [Optional] The id of the tournament to count. Leave blank for global registry.
    """
    db = connect()
    c = db.cursor()
    #If tid is on default value, select all players in the database.   
    if tid=='all':
        c.execute('SELECT count(players.name) from players;')
    #Otherwise, select the players registered to the given tournament
    else:
        c.execute('SELECT count(tournplayers.pid) from tournplayers where tid = %s;', (tid,))
    #Grab the results
    count = c.fetchall()
    db.close()
    #Return just the number to the program
    return count[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()    
    #insert the player into the table. Their id is assigned automatically
    c.execute("INSERT INTO players(name) values (%s);", (name,))
    db.commit()
    db.close()

def addPlayer(tid,playerid):
    """Adds a player to the given tournament.
  
    Players must have been registered first.    
  
    Args:
      tid: the tournament id.
      playerid: the players assigned id.
    """
    db = connect()
    c = db.cursor()    
    #insert the player into the table. Their id is assigned automatically
    c.execute("INSERT INTO tournplayers(tid,pid) values (%s,%s);", (tid,playerid))
    db.commit()
    db.close()

def playerStandings(tid='all'):
    """Returns a list of the players and their win records, sorted by wins.

    Args:
      tid: [Optional] The id of the tournament to view the standings for. Leave blank for global registry.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        tid: [only if tid='all'] the id of the tournament
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        draws: the number of matches the player tied in
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    #Grab the results of the standings view.
    #If tid is on default value, select all players in the database.   
    if tid=='all':
        c.execute('select * from tournstandings;')
    #otherwise look only to the given tournament
    else:
        c.execute('select id, name, wins, draws, matches from tournstandings where tid = %s',(tid,))
    standings = c.fetchall()
    db.close()
    return standings

def swissStandings(tid='all'):
    """Returns a list of the players and their points.

    Players have 3 points per win, and one point per draw.

    Args:
      tid: [Optional] The id of the tournament to view the standings for. Leave blank for global registry.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        tid: [only if tid='all'] the id of the tournament
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        draws: the number of matches the player tied in
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    #Grab the results of the standings view.
    #If tid is on default value, select all players in the database.   
    if tid=='all':
        c.execute('select * from threepointstandings;')
    #otherwise look only to the given tournament
    else:
        c.execute('select id, name, wins, draws, matches from threepointstandings where tid = %s',(tid,))
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(tid, firstid, secondid, result):
    """Records the outcome of a single match between two players.

    Args:
      tid:  the id of the tournament the match was played in
      firstid: the id of the first player 
      secondid:  the id of the second player
      result: the result of the match. 0 for draw, 1 for first player victory, 2 for second player victory.
    """
    db = connect()
    c = db.cursor()    
    c.execute("INSERT INTO tournmatches (tid, firstid, secondid, result) VALUES (%s,%s,%s,%s);",(tid, firstid, secondid, result))
    db.commit()
    db.close()

def swissPairings(tid):
    """Returns a list of pairs of players for the next round of a match.
  
    Args:
      tid:  the id of the tournament the match was played in
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    #Create a blank pairing that we will populate
    pairing = []
    #Count how many players there is
    count = countPlayers(tid)
    #Pairing won't work if there is less than two players, so just return an error message if there is.
    if (count < 2):
        return "Not Enough Players to pair."
    #Grab the player standings
    stand = swissStandings(tid)
    #Grab every other player in the table, and pair them against the player directly below them
    for i in range(0,count,2):
        pairing.append((stand[i][0],stand[i][1],stand[i+1][0],stand[i+1][1]))
    #Return the generated Pairings
    return pairing
