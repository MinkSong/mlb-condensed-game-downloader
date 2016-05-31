import xml.etree.ElementTree as ET


def parse_game_file(game_file):
	tree = ET.parse(game_file)
	root = tree.getroot()	
	
	games = []

	for media in root.iter('media'):
		if "condensed" in media.attrib.keys() and "id" in media.attrib.keys():
			game = {}
			game["id"] = media.attrib["id"]
			game["sortable_date"] = media.attrib["date"]
			for child in media:
				if child.tag == "headline":
					pieces = child.text.split(" ")
					day, month, year = pieces[0].split("/")
					away_team, home_team = pieces[2].split("@")
					
					game["day"] = day
					game["month"] = month
					
					game["year"] = year
					game["home_team"] = home_team
					game["away_team"] = away_team
					
					games.append(game)
					
	return games
				
				

game_file = 'game_data/446867.xml'
games = parse_game_file(game_file)
print games
		
		