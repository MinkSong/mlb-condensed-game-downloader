import os

# where to look for our xml files online
mlb_root = "http://gd2.mlb.com/components/game/mlb/year_2016/"
folder = "mobile"
mlb_path = os.path.join(mlb_root, folder)

# game data folder
game_data_folder = os.path.join(os.path.dirname(__file__), "game_data")


game_id_dict_filepath = os.path.join(game_data_folder, "game_id_dict.p")
condensed_url_dict_filepath = os.path.join(game_data_folder, "condensed_url_dict.p")


pitching_file = os.path.join(game_data_folder, "pit_wpa.csv")
batting_file = os.path.join(game_data_folder, "bat_wpa.csv")