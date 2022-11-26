import requests
import csv
from os import path
import pandas as pd
import utils

###
# Function which will upload results into NHL 2022-23 Games.csv file
# and also append the game row with home and away team stats heading into that game.
# Stats are retrieved using the date parameter and matching it to the team stats csv file.
###
def uploadResultsAndStats(start_date = None, end_date = None):
    if start_date is None:
        start_date = utils.getYesterdaysDate("%Y-%m-%d")
    if end_date is None:
        end_date = utils.getTodaysDate("%Y-%m-%d") # if date params left null, will retrieve last night's games
    url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}".format(start_date, end_date)
    request = requests.get(url)
    requestJson = request.json()

    basepath = path.dirname(__file__)
    filename = "NHL 2022-23 Games.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)

    for date in requestJson['dates']:
        for game in date['games']:
            if game['gameType'] == "R": # process only regular season games
                if game['status']['statusCode'] == "7": # 7 - Final, otherwise don't process game as it won't contain scores 
                    game_id = game['gamePk']   # get gameId
                    row_index =  df.index[df['game_id'] == game_id] # find game by ID in csv file
                    #update game row with goals for both teams and respective result
                    home_team_goals = game['teams']['home']['score']
                    away_team_goals = game['teams']['away']['score']
                    if home_team_goals > away_team_goals:
                        result = 1
                    else:
                        result = 0
                    df.loc[row_index,"home_team_goals"] = home_team_goals
                    df.loc[row_index,"away_team_goals"] = away_team_goals
                    df.loc[row_index,"result"] = result
    
    
    #basepath = path.dirname(__file__)
    #filename = "NHL 2022-23 Games TEST2.csv"
    #filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df.to_csv(filepath)

def encoding(filepath = None):
    import chardet
    if filepath is None:
        basepath = path.dirname(__file__)
        filename = "NHL 2022-23 Games.csv"
        filepath = path.abspath(path.join(basepath, "..", "data", filename))
    with open(filepath, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))
    return result  
uploadResultsAndStats(start_date="2022-10-07") #date of season opener
