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
	elif team == "LAA":
		key = "ANA"
	
	
	return key
		
def team_string_with_teams(team1, team2):
	teams = sorted([team_key(team1), team_key(team2)])
	return teams[0] + "-" + teams[1]
		
		
	
def game_key_for_dict(gameDict):
	
	date = gameDict['Date']
	date = date[0:10]
	
	team1 = gameDict['Tm']
	team2 = gameDict['Opp']
	teams = team_string_with_teams(team1, team2)
	game_key = date + ' ' + teams
	return game_key
	
def find_game_date_from_xml_string(xml_string):
	date = None
	
	date_regexp = "[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{1,2}"
	match = re.search(date_regexp, xml_string)
	
	if match != None:
		date = match.group(0)
		
	return date
	
def find_rtmp_url_in_xml_string(xml_string):
	
	url = None
	
	rtmp_reg_ex = "rtmp://.*.mp4"
	match = re.search(rtmp_reg_ex, xml_string)
	
	if match != None:
		url = match.group(0)
	
	return url
	
def find_any_media_url_in_xml_string(xml_string):
	
	url = None
	
	exp = "http://.*_[a-z]{6}_.*.mp4"
	match = re.search(exp, xml_string)
	
	if match != None:
		url = match.group(0)
	
	return url
	
def game_key_from_xml_data(xml_data):
	
	date = find_game_date_from_xml_string(xml_data)
	date_components = date.split("/")
	
	month = int(date_components[0])
	day = int(date_components[1])
	year = 2000 + int(date_components[2])
	
	key_date = "%02d-%02d-%02d" % (year, month, day)
	
	url = find_any_media_url_in_xml_string(xml_data)
	print url
	teams = extractTeamFromUrl(url)
	teamL = teams[1:4].upper()
	teamR = teams[4:7].upper()
	
	team_string = team_string_with_teams(teamL, teamR)
	
	return key_date + " " + team_string