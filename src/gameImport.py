import requests
import csv
from os import path
import utils

def createGameFile():
    basepath = path.dirname(__file__)
    filename = "NHL 2022-23 Games.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    header = ['date', 'game_id', 'home_team', 'away_team']
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def loadGames(start_date = "2022-10-07", end_date = None):
    if end_date is None:
        end_date = utils.getTodaysDate("%Y-%m-%d")
    url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}".format(start_date, end_date)
    request = requests.get(url)
    requestJson = request.json()
    #print(requestJson)
    games = []
    for date in requestJson['dates']:
        for game in date['games']:
            if game['gameType'] == "R":
                game_entry = []
                date = game['gameDate'] # first need to format date to remove timestamp
                date = date[:-10]       # remove timestamp characters
                game_entry.append(date) # add gameDate
                game_entry.append(game['gamePk'])   # add gameId
                #process exception where Montreal Canadiens written as Montréal Canadiens
                if game['teams']['home']['team']['name'] == "Montréal Canadiens":
                    game_entry.append("Montreal Canadiens")
                else:
                    game_entry.append(game['teams']['home']['team']['name']) # add home team
                if game['teams']['away']['team']['name'] == "Montréal Canadiens":
                    game_entry.append("Montreal Canadiens")
                else:
                    game_entry.append(game['teams']['away']['team']['name']) # add away team
                games.append(game_entry)
    basepath = path.dirname(__file__)
    filename = "NHL 2022-23 Games.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(games)
    return requestJson
#createGameFile()
#loadGames(end_date="2023-04-13")

