import urllib, urllib2
import re
import os
import pickle

# mlb gameday api urls
from mlb_paths import *

def month_links_in_xml(xml):
	'''
	Given html from a mlb year_xxxx link, return the list of months
	for that year (that are available on this link)
	'''
	month_paths = []
	for line in xml.split("\n"):
		match = re.search("month_[0-9]{2}", line)
		if match != None:
			month_path = match.group(0)
			month_paths.append(month_path)
			
	return month_paths
	
def day_links_in_xml(xml):
	'''
	Given html from a mlb month_xx link, return the list of days
	for that month (that are available on this link)
	'''
	day_paths = []
	for line in xml.split("\n"):
		match = re.search("day_[0-9]{2}", line)
		if match != None:
			day = match.group(0)
			day_paths.append(day)
			
	return day_paths
	
def gameID_links_in_xml(xml):
	'''
	Given html from a mlb day_xx link, return the list of game ids
	for that day (that are available on this link)
	'''
	gameIDs = []
	for line in xml.split("\n"):
		match = re.search("gid_[0-9]{4}_[0-9]{2}_[0-9]{2}_[a-z]{6}_[a-z]{6}_[0-9]", line)
		if match != None:
			game = match.group(0)
			gameIDs.append(game)
			
	return gameIDs
	
def cache_game_events_file(game_path):
	if False == os.path.isdir(game_event_files_dir()):
		os.mkdir(game_event_files_dir())
		
	game_events_url = os.path.join(game_path, "game_events.json")
	game_filename = os.path.basename(game_path) + ".json"
	dump_file_path = os.path.join(game_event_files_dir(), game_filename)
	urllib.urlretrieve(game_events_url, dump_file_path)
	

def cached_game_event_ids():
	game_ids = set()
	files = [f for f in os.listdir(game_event_files_dir())]
	for file in files:
		if file.endswith(".json"):
			game_id = os.path.splitext(file)[0]
			game_ids.add(game_id)
						
	return game_ids

def find_all_games_in_year(year):
	'''
	Given a year, put it all together and list every game path for that year.
	'''
	
	# start with the months 
	starting_path = mlb_game_path_with_year(year)
	resultXML = urllib2.urlopen(starting_path).read()
	months = month_links_in_xml(resultXML)

	# create full paths with the months
	month_paths = []
	for month in months:
		new_path = os.path.join(starting_path, month)
		month_paths.append(new_path)
		
	# now add the days
	day_paths = []
	for month_path in month_paths:
		this_month_xml = urllib2.urlopen(month_path).read()
		days = day_links_in_xml(this_month_xml)
		for day in days:
			new_path = os.path.join(month_path, day)
			day_paths.append(new_path)
			
	# now find all of the games for these days
	game_paths = []
	for day_path in day_paths:
		this_day_xml = urllib2.urlopen(day_path).read()
		gameIDs = gameID_links_in_xml(this_day_xml)
		for gameID in gameIDs:
			game_path = os.path.join(day_path, gameID)
			game_paths.append(game_path)
			print game_path
		
	return game_paths
	
def cache_event_files_for_year(year):
	game_paths = load_cached_game_paths(2016)
	cached_games = cached_game_event_ids()
	for game in game_paths:
		game_id = os.path.basename(game)
		if game_id not in cached_games:
			cache_game_events_file(game)
	
def dump_game_paths(game_paths, year):
	'''
	Given a list of game paths and a year, dump these to a cache file
	'''
	path_dump_file = open(game_dump_file_with_year(year), "wr+")
	pickle.dump(game_paths, path_dump_file)
	path_dump_file.close()
	
def load_cached_game_paths(year):
	'''
	Given a year, either load the cache file or find all of the games and return them
	'''
	try:
		path_dump_file = open(game_dump_file_with_year(year), "r")
		game_paths = pickle.load(path_dump_file)
		path_dump_file.close()
		return game_paths
	except:
		all_games = find_all_games_in_year(year)
		dump_game_paths(all_games, year)
		return all_games
		


#files = [f for f in os.listdir(game_event_files_dir())]
#for file in files:
#	print file
cache_event_files_for_year(2016)



	