import subprocess
import os

from collections import *

def download_from_m3u8_url(url, output_file):
	print "aboud to dl", url, "output:", output_file
	subprocess.call(["/usr/local/bin/ffmpeg", "-i", url, output_file])


def download_games(sorted_games, teams_to_dl, games_per_team_to_dl, output_folder):
	
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
			
			if False == os.path.isdir(output_folder):
				os.mkdir(output_folder)
				
			filename = "%02d%02d%02d_%s@%s.mp4" % (int(game["year"]), int(game["month"]), int(game["day"]), away_team, home_team)
			output_file = os.path.join(output_folder, filename)
			if os.path.exists(output_file):
				print "Skipping", filename, "(found on disk)"
			else:
				print "Downloading game", filename
				download_from_m3u8_url(game["asset_url"], output_file)
			

