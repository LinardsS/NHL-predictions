import requests
import importCsv
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
#uploadResultsAndStats(start_date="2022-10-07") #date of season opener
def tempStatsUpload():
    home_team = game['teams']['home']['team']['name']
    if home_team == "Montréal Canadiens":
        home_team = "Montreal Canadiens" #encoding workaround
    away_team = game['teams']['away']['team']['name']
    if away_team == "Montréal Canadiens":
        away_team = "Montreal Canadiens" #encoding workaround
    date = game['gameDate'] # first need to format date to remove timestamp
    date = date[:-10] #trim timestamp 
    ##change date format to dd-mm-yy as API returns YYYY-MM-DD
    game_dict = importCsv.getTeamsStats(date, home_team, away_team, format = True)
    home_team_dict = game_dict['home_team']
    away_team_dict = game_dict['away_team']
    #updates csv row with home team stats
    df.loc[row_index,"h_point%"] = game_dict['home_team']['Point %']
    df.loc[row_index,"h_cf%"] = game_dict['home_team']['CF%']
    df.loc[row_index,"h_ff%"] = game_dict['home_team']['FF%']
    df.loc[row_index,"h_sf%"] = game_dict['home_team']['SF%']
    df.loc[row_index,"h_gf%"] = game_dict['home_team']['GF%']
    df.loc[row_index,"h_xgf%"] = game_dict['home_team']['xGF%']
    df.loc[row_index,"h_scf%"] = game_dict['home_team']['SCF%']
    df.loc[row_index,"h_scsf%"] = game_dict['home_team']['SCSF%']
    df.loc[row_index,"h_scgf%"] = game_dict['home_team']['SCGF%']
    df.loc[row_index,"h_scsh%"] = game_dict['home_team']['SCSH%']
    df.loc[row_index,"h_scsv%"] = game_dict['home_team']['SCSV%']
    df.loc[row_index,"h_hdsf%"] = game_dict['home_team']['HDSF%']
    df.loc[row_index,"h_hdgf%"] = game_dict['home_team']['HDGF%']
    df.loc[row_index,"h_hdsh%"] = game_dict['home_team']['HDSH%']
    df.loc[row_index,"h_hdsv%"] = game_dict['home_team']['HDSV%']
    df.loc[row_index,"h_mdsf%"] = game_dict['home_team']['MDSF%']
    df.loc[row_index,"h_mdgf%"] = game_dict['home_team']['MDGF%']
    df.loc[row_index,"h_mdsh%"] = game_dict['home_team']['MDSH%']
    df.loc[row_index,"h_mdsv%"] = game_dict['home_team']['MDSV%']
    df.loc[row_index,"h_ldsf%"] = game_dict['home_team']['LDSF%']
    df.loc[row_index,"h_ldgf%"] = game_dict['home_team']['LDGF%']
    df.loc[row_index,"h_ldsh%"] = game_dict['home_team']['LDSH%']
    df.loc[row_index,"h_ldsv%"] = game_dict['home_team']['LDSV%']
    df.loc[row_index,"h_sh%"] = game_dict['home_team']['SH%']
    df.loc[row_index,"h_sv%"] = game_dict['home_team']['SV%']
    df.loc[row_index,"h_PDO"] = game_dict['home_team']['PDO']
    #away team
    df.loc[row_index,"a_point%"] = game_dict['away_team']['Point %']
    df.loc[row_index,"a_cf%"] = game_dict['away_team']['CF%']
    df.loc[row_index,"a_ff%"] = game_dict['away_team']['FF%']
    df.loc[row_index,"a_sf%"] = game_dict['away_team']['SF%']
    df.loc[row_index,"a_gf%"] = game_dict['away_team']['GF%']
    df.loc[row_index,"a_xgf%"] = game_dict['away_team']['xGF%']
    df.loc[row_index,"a_scf%"] = game_dict['away_team']['SCF%']
    df.loc[row_index,"a_scsf%"] = game_dict['away_team']['SCSF%']
    df.loc[row_index,"a_scgf%"] = game_dict['away_team']['SCGF%']
    df.loc[row_index,"a_scsh%"] = game_dict['away_team']['SCSH%']
    df.loc[row_index,"a_scsv%"] = game_dict['away_team']['SCSV%']
    df.loc[row_index,"a_hdsf%"] = game_dict['away_team']['HDSF%']
    df.loc[row_index,"a_hdgf%"] = game_dict['away_team']['HDGF%']
    df.loc[row_index,"a_hdsh%"] = game_dict['away_team']['HDSH%']
    df.loc[row_index,"a_hdsv%"] = game_dict['away_team']['HDSV%']
    df.loc[row_index,"a_mdsf%"] = game_dict['away_team']['MDSF%']
    df.loc[row_index,"a_mdgf%"] = game_dict['away_team']['MDGF%']
    df.loc[row_index,"a_mdsh%"] = game_dict['away_team']['MDSH%']
    df.loc[row_index,"a_mdsv%"] = game_dict['away_team']['MDSV%']
    df.loc[row_index,"a_ldsf%"] = game_dict['away_team']['LDSF%']
    df.loc[row_index,"a_ldgf%"] = game_dict['away_team']['LDGF%']
    df.loc[row_index,"a_ldsh%"] = game_dict['away_team']['LDSH%']
    df.loc[row_index,"a_ldsv%"] = game_dict['away_team']['LDSV%']
    df.loc[row_index,"a_sh%"] = game_dict['away_team']['SH%']
    df.loc[row_index,"a_sv%"] = game_dict['away_team']['SV%']
    df.loc[row_index,"a_PDO"] = game_dict['away_team']['PDO']

