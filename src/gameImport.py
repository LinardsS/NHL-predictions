import requests
import csv
from os import path
import utils

def createGameFile(season = None):
    basepath = path.dirname(__file__)
    if season is None:
        season = "2022-23"
    filename = "NHL " + season + " Games.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    header = ['date','game_id','home_team','away_team','home_team_goals','away_team_goals','result','h_point%','h_cf%','h_ff%','h_sf%','h_gf%','h_xgf%','h_scf%','h_scsf%','h_scgf%','h_scsh%','h_scsv%','h_hdsf%','h_hdgf%','h_hdsh%','h_hdsv%','h_mdsf%','h_mdgf%','h_mdsh%','h_mdsv%','h_ldsf%','h_ldgf%','h_ldsh%','h_ldsv%','h_sh%','h_sv%','h_PDO','a_point%','a_cf%','a_ff%','a_sf%','a_gf%','a_xgf%','a_scf%','a_scsf%','a_scgf%','a_scsh%','a_scsv%','a_hdsf%','a_hdgf%','a_hdsh%','a_hdsv%','a_mdsf%','a_mdgf%','a_mdsh%','a_mdsv%','a_ldsf%','a_ldgf%','a_ldsh%','a_ldsv%','a_sh%','a_sv%','a_PDO']
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def loadGames(start_date = "2022-10-07", end_date = None, season = "2022-23", results = False):
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
                if results is True: # if results flag set, load result for game as well
                    home_team_goals = game['teams']['home']['score']
                    away_team_goals = game['teams']['away']['score']
                    if home_team_goals > away_team_goals:
                        result = 1
                    else:
                        result = 0
                    game_entry.append(home_team_goals) # add home team goals
                    game_entry.append(away_team_goals) # add away team goals
                    game_entry.append(result)          # add game result
                games.append(game_entry)
    basepath = path.dirname(__file__)
    filename = "NHL " + season + " Games.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(games)
#createGameFile(season="2021-22")
#loadGames(start_date="2021-10-12", end_date="2022-04-29", season = "2021-22", results = True) #October 12, 2021 – June 26, 2022