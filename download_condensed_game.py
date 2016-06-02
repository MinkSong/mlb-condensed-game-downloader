import subprocess
import os

from collections import *

def download_from_m3u8_url(url, output_file):
	print "aboud to dl", url, "output:", output_file
	subprocess.call(["ffmpeg", "-i", url, output_file])


def download_games(sorted_games, teams_to_dl, games_per_team_to_dl):
	
	team_game_count = defaultdict(int)
	
	for game in sorted_games:
		download_game = False
		home_team, away_team = game["home_team"], game["away_team"]
		if home_team in teams_to_dl and team_game_count[home_team] < games_per_team_to_dl:
			team_game_count[home_team] += 1
			download_game = True
			
		if away_team in teams_to_dl and team_game_count[away_team] < games_per_team_to_dl:
			team_game_count[away_team] += 1
			download_game = True
			
		if download_game:
			
			output_folder =  os.path.abspath(os.path.join(os.path.dirname(__file__), "condensed_games"))
			if False == os.path.isdir(output_folder):
				os.mkdir(output_folder)
				
			filename = game["year"] + game["month"] + game["day"] + "_" + away_team + "@" + home_team + ".mp4"
			output_file = os.path.join(output_folder, filename)
			
			print "Downloading game", game
			download_from_m3u8_url(game["asset_url"], output_file)
			

