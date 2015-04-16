#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
"""
Implementation of a Swiss-system tournament
"""
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    #Delete all the entries in matches
    c.execute('DELETE FROM matches *;')
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

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    #Do a count of players in players    
    c.execute('SELECT count(players.name) from players;')
    #Grab the results
    count = c.fetchall()
    db.close()
    #Return just the number to the program
    return count[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()    
    #insert the player into the table. Their id is assigned automatically
    c.execute("INSERT INTO players(name) values (%s);", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    #Grab the results of the standings view.
    c.execute('select * from standings;')
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()    
    c.execute("INSERT INTO matches (winnerid, loserid) VALUES (%s,%s);",(winner, loser))
    db.commit()
    db.close()
    
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
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
    count = countPlayers()
    #Pairing won't work if there is less than two players, so just return an error message if there is.
    if (count < 2):
        return "Not Enough Players to pair."
    #Grab the player standings
    stand = playerStandings()
    #Grab every other player in the table, and pair them against the player directly below them
    for i in range(0,count,2):
        pairing.append((stand[i][0],stand[i][1],stand[i+1][0],stand[i+1][1]))
    #Return the generated Pairings
    return pairing
