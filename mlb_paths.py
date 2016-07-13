import os

# where to look for our xml files online
mlb_root = "http://gd2.mlb.com/components/game/mlb"
def mlb_game_path_with_year(year):
	return os.path.join(mlb_root, "year_" + str(year))
	
mlb_mobile_path = os.path.join(mlb_game_path_with_year(2016), "mobile")


# data storage folders
game_data_folder = os.path.join(os.path.dirname(__file__), "game_data")
condensed_games_folder = os.path.join(os.path.dirname(__file__), "condensed_games")

def game_dump_file_with_year(year):
	return os.path.join(game_data_folder, "game_paths_" + str(year) + ".p")
	
def game_event_files_dir():
	return os.path.join(game_data_folder, "game_events")


# Baseball-Reference storage and data gathering
game_id_dict_filepath = os.path.join(game_data_folder, "game_id_dict.p")
condensed_url_dict_filepath = os.path.join(game_data_folder, "condensed_url_dict.p")
pitching_file = os.path.join(game_data_folder, "pit_wpa.csv")
batting_file = os.path.join(game_data_folder, "bat_wpa.csv")



