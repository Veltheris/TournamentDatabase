-- Table definitions for the tournament project.
-- 
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
-- 
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the database if it doesn't already exist and navigate to it.
CREATE DATABASE tournament;
\c tournament;

-- It would be bad if this setup only half works, so start it as a batch.
begin;

create table players(id serial primary key, name text);

-- Create the table to store the matches
-- If a player is deleted, keep the matches they played but remove their id, keeping the foreign key satisfied. matchid can be used to easily update or delete a specific match.
create table matches(matchid serial primary key, winnerid integer references players on delete set null, loserid integer references players on delete set null);

-- create a view to list the matches with the names of the winners and losers.
create view fullmatches as select matchid, winnerid, a.name as winner, loserid, b.name as loser from players as a, players as b, matches where winnerid = a.id and loserid = b.id;

-- create a view to give the rankings.
create view standings as
select players.id, players.name,
       (select count(*) from matches where matches.winnerid = players.id) as wins,
       (select count(*) from matches where players.id in (winnerid, loserid)) as matches
from players
order by wins desc;

commit;

-- ===========================================================
-- Extra Credit Tables:
-- These tables support the extratournament.py functionality of draws and multiple tournaments. Player Ids are global.

-- begin the batch.
begin;

-- Tournaments, A table to hold all tournaments.
create table tournaments(tid serial primary key, tournament text, description text);

-- Tournament Players, A table to hold what players are assigned to what tournaments. The primary key is so a player cannot be assigned to the same tournament twice.
create table tournplayers(tid integer references tournaments, pid integer references players on delete cascade, primary key (tid,pid));

-- Tournament Matches, which lists the match and it's detail. Matchid is for easy update and removal of matches. The foreign key pairs make sure that only players in a given tournament can play a match in it.
create table tournmatches(matchid serial primary key, tid integer, firstid integer, secondid integer, result integer, foreign key (tid, firstid) references tournplayers(tid, pid) on delete cascade, foreign key (tid, secondid) references tournplayers(tid, pid) on delete cascade);

-- create a view to list the Tournament Matches with the names of the players.
create view tournfullmatches as select matchid, tid, firstid, a.name as firstplayer, secondid, b.name as secondplayer, result from players as a, players as b, tournmatches where firstid = a.id and secondid = b.id;

-- create a view to give the Tournament Standings.
-- The Standings table does not take into account the full worth of the draws, such that a player who has tied multiple matches may show up lower than they actually would be.
-- However, the value of a draw varies from tournament to tournament.
-- Listing just the Wins and Draws means further views could be made to calculate the points automatically.
create view tournstandings as
select tid, players.id, players.name,
       ((select count(*) from tournmatches where tournmatches.firstid = players.id and tournmatches.tid = tournplayers.tid and tournmatches.result = 1 ) +
        (select count(*) from tournmatches where tournmatches.secondid = players.id and tournmatches.tid = tournplayers.tid and tournmatches.result = 2)) as wins,
       (select count(*) from tournmatches where players.id in (secondid, firstid) and tournmatches.tid = tournplayers.tid and tournmatches.result = 0) as draws,
       (select count(*) from tournmatches where players.id in (secondid, firstid) and tournmatches.tid = tournplayers.tid) as matches
from players, tournplayers where tournplayers.pid = players.id
order by tid asc, wins desc, draws desc;

-- This creates a view that calculates each players points according to the common chess rules; three points for a win, and one for a draw.
create view threepointstandings as
select a.tid, a.id, a.name,
       ((select wins from tournstandings as b where a.id = b.id and a.tid = b.tid) * 3 + (select draws from tournstandings as c where c.id = a.id and c.tid = a.tid)) as points, a.matches
from tournstandings as a
order by tid asc, points desc;

commit;
