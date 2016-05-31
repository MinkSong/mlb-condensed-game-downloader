import csv
import pickle

from mlb_strings import *
from mlb_paths import *


def LIND_score_for_game_dict(gameDict):


    # our formula is very simple: WPA + aLI + HR / 4.5 (every 5 home runs is insanity!)
    score = 0.0

    score += float(gameDict['WPA'])
    score += float(gameDict['aLI'])
    score += float(gameDict['HR']) / 4.5

    return score



# first, create a dictionary of the batting games, using the date and teams as the key
batting_games = {}
with open(batting_file) as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        key = game_key_for_dict(row)
        score = LIND_score_for_game_dict(row)
        batting_games[key] = score

pitching_games = {}

with open(pitching_file) as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        key = game_key_for_dict(row)
        score = LIND_score_for_game_dict(row)
        pitching_games[key] = score


all_games = batting_games
for game_key, pitching_score in pitching_games.iteritems():
    if game_key in batting_games:
        batting_score = batting_games[game_key]
        if pitching_score > batting_score:
            all_games[game_key] = pitching_score
        #print "replacing batting score:", batting_score, "with pitching score:", pitching_score, "for", game_key
    else:
        all_games[game_key] = pitching_score


# read the game dicts into memory


condensed_url_dict = pickle.load(open(condensed_url_dict_filepath, "r"))
game_id_dict = pickle.load(open(game_id_dict_filepath, "r"))

#print game_id_dict

sorted_by_score = sorted(all_games, key=all_games.get, reverse=True)
teams_represented = set()
winning_teams = set()
i = 0
while len(teams_represented) < 30:
    game_key = sorted_by_score[i]
    score = all_games[game_key]

    date_url = None

    game_date = game_key[0:10]
    ymd = game_date.split("-")
    url_date = ymd[1] + "/" + ymd[2] + "/" + ymd[0]

    date_url = "http://mlb.mlb.com/mediacenter/index.jsp?c_id=mlb#date=" + url_date

    team1 = game_key[11:14]
    team2 = game_key[15:18]

    teams_represented.add(team1)
    teams_represented.add(team2)
    teams = team1 + "-" + team2

    condensed_url = "NO CONDENSED GAME URL"
    if game_key in condensed_url_dict:
        condensed_url = condensed_url_dict[game_key]

    game_id = "GAME_ID"
    if game_key in game_id_dict:
        game_id = game_id_dict[game_key]

        game_id, ext = os.path.splitext(game_id)
        game_url = "http://m.mlb.com/tv/e14-" + game_id + "-" + game_date


        date_column = "<td align=\"left\"><a href=\"%s\">%s</a></td>" % (date_url, game_date)
        team_column = "<td align=\"left\"><a href=\"%s\">%s</a></td>" % (date_url, teams)
        lind_score = "<td align=\"center\">%.2f</td>" % (score)
        mlb_tv = "<td align=\"center\"><a href=\"%s\"><u>Watch</u></a></td>" % (game_url)
        print "<tr>" + date_column, team_column, lind_score, mlb_tv + "</tr>"

    i += 1
		


