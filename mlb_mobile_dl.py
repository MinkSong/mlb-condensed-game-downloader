import urllib2
import re
import os
import subprocess, pickle

from mlb_paths import *
from mlb_strings import *
from parse_game_xml import *

teams_to_dl = []

teams_to_dl.append('sfn')
teams_to_dl.append('oak')

dates_to_dl = []

# what is the number of most recent games you'd like to download per team?
games_per_team_to_dl = 2


print "mlb_path:", mlb_path

game_id_dict = {}
condensed_game_dict = {}


# we are looking for xml files that look like 123456.xml
xml_reg_exp = "[0-9]*.xml"

# look in a local folder for already downloaded xml files e.g. "412345.xml"
def xmlFilesInFolder(folder_path):
	found_xml_files = set()
	files = [f for f in os.listdir(folder_path)]
	
	for f in files:
		match = re.search(xml_reg_exp, f)
		if match != None:
			xml_file = match.group(0)
			found_xml_files.add(xml_file)
			#print "found xml file:", xml_file
			
	return found_xml_files
	
# download a file via rtmp
def download_rtmp_url(rtmp_url, output_file):
	subprocess.call(["rtmpdump", "-r", rtmp_url, "-o", output_file])
	

	return team_name
			

print "game_data_folder:", game_data_folder
if False == os.path.isdir(game_data_folder):
	os.mkdir(game_data_folder)

	
result = urllib2.urlopen(mlb_root + folder).read()

found_xml_files = xmlFilesInFolder(game_data_folder)
all_xml_files = set()
for line in result.split('\n'):
	match = re.search(xml_reg_exp, line)
	if match != None:
		xml_file = match.group(0)
		all_xml_files.add(xml_file)
		
		
xml_files_to_dl = all_xml_files - found_xml_files
num_files_to_dl = len(xml_files_to_dl)
num_files_downloaded = 0


print "Found", len(found_xml_files), "out of", len(all_xml_files), "xml files on disk"
	
for file in xml_files_to_dl:
	file_url = os.path.join(mlb_path + "/" + file)
	print "file url:", file_url
	xml_data = urllib2.urlopen(file_url).read()
    
	# Open our local file for writing
	local_file_path = os.path.join(game_data_folder, file)
	print "local file:", local_file_path
	
	local_file = open(local_file_path, "wb")
    
	#Write to our local file
	local_file.write(xml_data)
	local_file.close()
	
	num_files_downloaded += 1
	print "downloading", num_files_downloaded, "of", num_files_to_dl
	
print "xml files up to date"

rtmp_urls = []

# go through the xml files and find the rtmp:// link to the condensed game
found_xml_files = xmlFilesInFolder(game_data_folder)

games_file = "game_data/game_dict.p"

games = {}

local_file = open(games_file, "rb")
if os.fstat(local_file.fileno()).st_size > 0:
	games = pickle.load(local_file)
local_file.close()

for file in found_xml_files:
	if file not in games:
		
		game = parse_game_file(game_data_folder + '/' + file)
		if game != None:
			games[game["file"]] = game
			local_file = open(games_file, "wb")
			pickle.dump(games, local_file)
			local_file.close()
	
#	file_path = os.path.join(game_data_folder, file)
#	xml_data = open(file_path, "r").read()
#	
#	game_date = find_game_date_from_xml_string(xml_data)
#	media_url = find_any_media_url_in_xml_string(xml_data)
#	
#	if game_date != None and media_url != None:
#
#		game_key = game_key_from_xml_data(xml_data)
#		game_id_dict[game_key] = file
#		
#		rtmp_url = find_rtmp_url_in_xml_string(xml_data)
#		if rtmp_url != None:
#			condensed_game_dict[game_key] = rtmp_url
#			rtmp_urls.append(rtmp_url)
		

local_file = open(games_file, "wb")
pickle.dump(games, local_file)
local_file.close()

from operator import itemgetter
sorted_games = sorted(games.values(), key=itemgetter('sortable_date'), reverse=True)

please_dl = set("SF", "OAK")
for game in sorted_games:
	should_dl = False
	home_team, away_team = game["home_team"], game["away_team"]
	if home_team in please_dl:
		please_dl.remove(home_team)
		should_dl = True		
	

# sort by newest descending. This is super easy because the date is in yyyy/mm/dd format, 
# so all we have to do is sort the text and reverse it.
rtmp_urls.sort()
rtmp_urls.reverse()


game_urls_correct_date = []

# remove game dates that aren't correct
if len(dates_to_dl) > 0:
	for url in rtmp_urls:
		thisDate = extractDateFromUrl(url)
		if thisDate in dates_to_dl:
			game_urls_correct_date.append(url)
else:
	game_urls_correct_date = rtmp_urls


# make an output path for downloaded games
output_folder =  os.path.abspath(os.path.join(os.path.dirname(__file__), "condensed_games"))
if False == os.path.isdir(output_folder):
	os.mkdir(output_folder)
	
game_urls_to_dl = []

for team in teams_to_dl:
	counter = 0
	for url in game_urls_correct_date:
		if team in url:
			found_team = True
			game_urls_to_dl.append(url)
			counter += 1
			if counter >= games_per_team_to_dl:
				break
		
for url in game_urls_to_dl:
	#print url
	team_name = extractTeamFromUrl(url)
	date = extractDateFromUrl(url)
	if date != None:
		date = date.replace("/", "")
		
	filename = date + team_name + "condensed" + os.path.splitext(url)[1]
	output_file = os.path.join(output_folder, filename)
	if False == os.path.exists(output_file):
		print "about to dl:", url, "to:", output_file
		download_rtmp_url(url, output_file)
	else:
		print "skipping:", url, "because it's alredy on disk."
		
print "Done"





import pickle
local_file = open(game_id_dict_filepath, "wb")
pickle.dump(game_id_dict, local_file)
local_file.close()

local_file = open(condensed_url_dict_filepath, "wb")
pickle.dump(condensed_game_dict, local_file)
local_file.close()
		
	
