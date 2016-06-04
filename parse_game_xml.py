import xml.etree.ElementTree as ET

def team_from_number(number):
    return {        
	    108: 'LAA',
        109: 'ARI',
        110: 'BAL',
        111: 'BOS',
        112: 'CHC',
        113: 'CIN',
        114: 'CLE',
        115: 'COL',
        116: 'DET',
        117: 'HOU', 
	    118: 'KC', 
	    119: 'LAD',
		120: 'WAS',
		121: 'NYM',
		133: 'OAK',
		134: 'PIT',
		135: 'SD',
		136: 'SEA',
		137: 'SF',
		138: 'STL',
		139: 'TB',
		140: 'TEX',
		141: 'TOR',
		142: 'MIN',
		143: 'PHI',
		144: 'ATL',
        145: 'CWS',
		146: 'MIA',
		147: 'NYY',
		158: 'MIL',
		
		798: 'CUBA'
    }[int(number)]


def parse_game_file(game_file):
	try:
		tree = ET.parse(game_file)
		root = tree.getroot()	
	except:
		return None

	for media in root.iter('media'):
		if "condensed" in media.attrib.keys() and media.attrib["condensed"] == "true":
			game = {}
			game["id"] = media.attrib["id"]
			game["sortable_date"] = media.attrib["date"]
			game["file"] = game_file.split("/")[-1]
			for child in media:
				if child.tag == "blurb":
					#print child.text
					pieces = child.text.split(" ")
					
					date_pieces = pieces[0].split("/")
					if len(date_pieces) >= 3:
						day, month, year = date_pieces
						game["day"] = day
						game["month"] = month
						game["year"] = year
						
					team_pieces = pieces[-1].split("@")
					if len(team_pieces) >= 2:
						away_team, home_team = team_pieces
						game["away_team"] = away_team
						game["home_team"] = home_team
						
				if child.tag == "keywords" and "away_team" not in game.keys():
					teams = []
					for keyword in child:
						if keyword.attrib["type"] == "team_id":
							teams.append(keyword.attrib["value"])
							
					if len(teams) >= 2:
						away_team, home_team = teams
						game["away_team"] = team_from_number(away_team)
						game["home_team"] = team_from_number(home_team)
						
				if child.tag == "url" and child.attrib["playback-scenario"] == "HTTP_CLOUD_WIRED":
						game["asset_url"] = child.text
					
					
			#print game
			return game
	
	return None				
				
game_file = 'game_data/446867.xml'
print parse_game_file(game_file)

		
		