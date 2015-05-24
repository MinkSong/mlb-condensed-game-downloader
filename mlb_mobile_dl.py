import urllib2
import re
import os
import subprocess


teams_to_dl = ['oak', 'sfn', 'tor']

# what is the number of most recent games you'd like to download per team?
games_per_team_to_dl = 1

# where to look for our xml files online
mlb_root = "http://gd2.mlb.com/components/game/mlb/year_2015/"
folder = "mobile"
mlb_path = os.path.join(mlb_root, folder)
print "mlb_path:", mlb_path


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
			

local_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), folder))
print "local_folder_path:", local_folder_path
if False == os.path.isdir(local_folder_path):
	os.mkdir(local_folder_path)

	
result = urllib2.urlopen(mlb_root + folder).read()

found_xml_files = xmlFilesInFolder(local_folder_path)
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
	local_file_path = os.path.join(local_folder_path, file)
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
found_xml_files = xmlFilesInFolder(local_folder_path)
for file in found_xml_files:
	file_path = os.path.join(local_folder_path, file)
	xml_data = open(file_path, "r").read()
	
	
	rtmp_reg_ex = "rtmp://.*.mp4"
	match = re.search(rtmp_reg_ex, xml_data)
	if match != None:
		rtmp_url = match.group(0)
		rtmp_urls.append(rtmp_url)
		
# sort by newest descending. This is super easy because the date is in yyyy/mm/dd format, 
# so all we have to do is sort the text and reverse it.
rtmp_urls.sort()
rtmp_urls.reverse()

# make an output path for downloaded games
output_folder =  os.path.abspath(os.path.join(os.path.dirname(__file__), "condensed_games"))
if False == os.path.isdir(output_folder):
	os.mkdir(output_folder)
	
game_urls_to_dl = []

for team in teams_to_dl:
	counter = 0
	for url in rtmp_urls:
		if team in url:
			found_team = True
			game_urls_to_dl.append(url)
			counter += 1
			if counter >= games_per_team_to_dl:
				break
		
for url in game_urls_to_dl:
	
	team_name = "_unknown_"
	team_match = re.search("_[a-z]*_", url)
	if team_match != None:
		team_name = team_match.group(0)
		
	date = "YYYY/MM/DD"
	date_match = re.search("[0-9]{4}/[0-9]{2}/[0-9]{2}", url)
	if date_match != None:
		date = date_match.group(0)
		date = date.replace("/", "")
		
	filename = date + team_name + "condensed" + os.path.splitext(url)[1]
	output_file = os.path.join(output_folder, filename)
	if False == os.path.exists(output_file):
		print "about to dl:", url, "to:", output_file
		download_rtmp_url(url, output_file)
	else:
		print "skipping:", url, "because it's alredy on disk."
		
	
