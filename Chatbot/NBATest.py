import requests
import json

players = 'https://balldontlie.io/api/v1/players'


player_response = requests.get(players)
player_response = player_response.json()

def get_team_players(team_name):
    player_list = []
    new = player_response["data"]
    for i in new:
        if i['team'] != None:
            team = i["team"]
            
            if team["full_name"] == team_name:
            
                name = "{} {}".format(i["first_name"], i["last_name"])
            
                player_list.append(name)
    
    return player_list
#returns all players at height or greater
def height_check(height):
    for i in player_response["data"]:
        if i['height_feet'] != None and i['height_feet'] >= height:
            name = "Name:{} {}".format(i["first_name"], i["last_name"])
            print(name)

#print(response)
