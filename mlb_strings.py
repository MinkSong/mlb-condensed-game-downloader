import os
import re


# extract the date from a rtmp xml
def extractDateFromUrl(url):
	date_match = re.search("[0-9]{4}/[0-9]{2}/[0-9]{2}", url)
	if date_match != None:
		date = date_match.group(0)
		return date

	return None
	
def extractTeamFromUrl(url):
	team_name = "_unknown_"
	team_match = re.search("_[a-z]*_", url)
	if team_match != None:
		team_name = team_match.group(0)
		
	return team_name
		
	
def team_key(team):
	key = team.upper()
	
	if team == "NYN":
		key = "NYM"
	elif team == "NYA":
		key = "NYY"
	elif team == "SFN":
		key = "SFG"
	elif team == "LAN":
		key = "LAD"
	elif team == "SLN":
		key = "STL"
	elif team == "TBA":
		key = "TBR"
	elif team == "KCA":
		key = "KCR"
	elif team == "CHN":
		key = "CHC"
	elif team == "CHA":
		key = "CHW"
	elif team == "SDN":
		key = "SDP"
	elif team == "WSN":
		key = "WAS"
	
	
	return key
		
def team_string_with_teams(team1, team2):
	teams = sorted([team_key(team1), team_key(team2)])
	return teams[0] + "-" + teams[1]
		
		
def game_key_from_rtmp_url(url):
	date = extractDateFromUrl(url)
	date = date.replace("/", "-")
	
	teams = extractTeamFromUrl(url)
	teamL = teams[1:4].upper()
	teamR = teams[4:7].upper()
	
	team_string = team_string_with_teams(teamL, teamR)
	
	return date + " " + team_string
	
	
def game_key_for_dict(gameDict):
	
	date = gameDict['Date']
	date = date[0:10]
	
	team1 = gameDict['Tm']
	team2 = gameDict['Opp']
	teams = team_string_with_teams(team1, team2)
	game_key = date + ' ' + teams
	return game_key