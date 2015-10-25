import csv


def LIND_score_for_game_dict(gameDict):
	
	
	# our formula is very simple: WPA + aLI + HR / 4.5 (every 5 home runs is insanity!)
	score = 0.0
	
	score += float(gameDict['WPA'])
	score += float(gameDict['aLI'])
	score += float(gameDict['HR']) / 4.5
	
	return score
	
def game_key_for_dict(gameDict):
	
	date = gameDict['Date']
	teams = gameDict['Tm'] + '-' + gameDict['Opp']
	game_key = date + ' ' + teams
	return game_key
	

# first, create a dictionary of the batting games, using the date and teams as the key
batting_games = {}
batting_file = 'raw_csv/bat_wpa.csv'
with open(batting_file) as csvfile: 
	reader = csv.DictReader(csvfile)
	
	for row in reader:
		key = game_key_for_dict(row)
		score = LIND_score_for_game_dict(row)
		batting_games[key] = score
		
pitching_games = {}
pitching_file = 'raw_csv/pit_wpa.csv'
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
		
	
sorted_by_score = sorted(all_games, key=all_games.get, reverse=True)
for i in range (0, 30):
	game_key = sorted_by_score[i]
	score = all_games[game_key]
	print i, "-", score, game_key

		


