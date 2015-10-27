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

print game_id_dict

sorted_by_score = sorted(all_games, key=all_games.get, reverse=True)
for i in range (0, 50):
	game_key = sorted_by_score[i]
	score = all_games[game_key]

	condensed_url = "NO CONDENSED GAME URL"
	if game_key in condensed_url_dict:
		condensed_url = condensed_url_dict[game_key]
		
	game_id = "GAME_ID"
	if game_key in game_id_dict:
		game_id = game_id_dict[game_key]
		
		
	print i, "-", score, game_key, condensed_url, game_id

		


