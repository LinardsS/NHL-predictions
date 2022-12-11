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
    # first_column = df.columns[0]
    # df = df.drop([first_column], axis=1)

    for date in requestJson['dates']:
        for game in date['games']:
            if game['gameType'] == "R": # process only regular season games
                if game['status']['statusCode'] == "7" or game['status']['statusCode'] == "6": # 7 or 6 - Final, otherwise don't process game as it won't contain scores 
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

                    game_date = df.loc[row_index,"date"].item()
                    home_team = df.loc[row_index,"home_team"].item()
                    away_team = df.loc[row_index,"away_team"].item()
                    print(game_date,home_team,away_team)
                    game_dict = importCsv.getTeamsStats(game_date, home_team, away_team, format = True, backdate = True)
                    #print(game_dict)
                    if game_dict == {}:
                        print("Team data missing for: \n")
                        print(date,home_team,away_team) # print for debugging purposes
                        continue    # if team stats file not found, don't touch csv rows
                    #2 checks if dictionary present but one team's data is missing
                    if "home_team" not in list(game_dict.keys()):
                        print(home_team + " stats missing from " + date )
                        continue
                    if "away_team" not in list(game_dict.keys()):
                        print(away_team + " stats missing from " + date )
                        continue
                    home_team_dict = game_dict['home_team']
                    away_team_dict = game_dict['away_team']
                    df.loc[row_index,"h_point%"] = home_team_dict['Point %']
                    df.loc[row_index,"h_cf%"] = home_team_dict['CF%']
                    df.loc[row_index,"h_ff%"] = home_team_dict['FF%']
                    df.loc[row_index,"h_sf%"] = home_team_dict['SF%']
                    df.loc[row_index,"h_gf%"] = home_team_dict['GF%']
                    df.loc[row_index,"h_xgf%"] = home_team_dict['xGF%']
                    df.loc[row_index,"h_scf%"] = home_team_dict['SCF%']
                    df.loc[row_index,"h_scsf%"] = home_team_dict['SCSF%']
                    df.loc[row_index,"h_scgf%"] = home_team_dict['SCGF%']
                    df.loc[row_index,"h_scsh%"] = home_team_dict['SCSH%']
                    df.loc[row_index,"h_scsv%"] = home_team_dict['SCSV%']
                    df.loc[row_index,"h_hdsf%"] = home_team_dict['HDSF%']
                    df.loc[row_index,"h_hdgf%"] = home_team_dict['HDGF%']
                    df.loc[row_index,"h_hdsh%"] = home_team_dict['HDSH%']
                    df.loc[row_index,"h_hdsv%"] = home_team_dict['HDSV%']
                    df.loc[row_index,"h_mdsf%"] = home_team_dict['MDSF%']
                    df.loc[row_index,"h_mdgf%"] = home_team_dict['MDGF%']
                    df.loc[row_index,"h_mdsh%"] = home_team_dict['MDSH%']
                    df.loc[row_index,"h_mdsv%"] = home_team_dict['MDSV%']
                    df.loc[row_index,"h_ldsf%"] = home_team_dict['LDSF%']
                    df.loc[row_index,"h_ldgf%"] = home_team_dict['LDGF%']
                    df.loc[row_index,"h_ldsh%"] = home_team_dict['LDSH%']
                    df.loc[row_index,"h_ldsv%"] = home_team_dict['LDSV%']
                    df.loc[row_index,"h_sh%"] = home_team_dict['SH%']
                    df.loc[row_index,"h_sv%"] = home_team_dict['SV%']
                    df.loc[row_index,"h_PDO"] = home_team_dict['PDO']
                    #away team
                    df.loc[row_index,"a_point%"] = away_team_dict['Point %']
                    df.loc[row_index,"a_cf%"] = away_team_dict['CF%']
                    df.loc[row_index,"a_ff%"] = away_team_dict['FF%']
                    df.loc[row_index,"a_sf%"] = away_team_dict['SF%']
                    df.loc[row_index,"a_gf%"] = away_team_dict['GF%']
                    df.loc[row_index,"a_xgf%"] = away_team_dict['xGF%']
                    df.loc[row_index,"a_scf%"] = away_team_dict['SCF%']
                    df.loc[row_index,"a_scsf%"] = away_team_dict['SCSF%']
                    df.loc[row_index,"a_scgf%"] = away_team_dict['SCGF%']
                    df.loc[row_index,"a_scsh%"] = away_team_dict['SCSH%']
                    df.loc[row_index,"a_scsv%"] = away_team_dict['SCSV%']
                    df.loc[row_index,"a_hdsf%"] = away_team_dict['HDSF%']
                    df.loc[row_index,"a_hdgf%"] = away_team_dict['HDGF%']
                    df.loc[row_index,"a_hdsh%"] = away_team_dict['HDSH%']
                    df.loc[row_index,"a_hdsv%"] = away_team_dict['HDSV%']
                    df.loc[row_index,"a_mdsf%"] = away_team_dict['MDSF%']
                    df.loc[row_index,"a_mdgf%"] = away_team_dict['MDGF%']
                    df.loc[row_index,"a_mdsh%"] = away_team_dict['MDSH%']
                    df.loc[row_index,"a_mdsv%"] = away_team_dict['MDSV%']
                    df.loc[row_index,"a_ldsf%"] = away_team_dict['LDSF%']
                    df.loc[row_index,"a_ldgf%"] = away_team_dict['LDGF%']
                    df.loc[row_index,"a_ldsh%"] = away_team_dict['LDSH%']
                    df.loc[row_index,"a_ldsv%"] = away_team_dict['LDSV%']
                    df.loc[row_index,"a_sh%"] = away_team_dict['SH%']
                    df.loc[row_index,"a_sv%"] = away_team_dict['SV%']
                    df.loc[row_index,"a_PDO"] = away_team_dict['PDO']
    
    
    #basepath = path.dirname(__file__)
    #filename = "NHL 2022-23 Games TEST2.csv"
    #filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df.to_csv(filepath, index=False)

def encoding(filepath = None):
    import chardet
    if filepath is None:
        basepath = path.dirname(__file__)
        filename = "NHL 2022-23 Games.csv"
        filepath = path.abspath(path.join(basepath, "..", "data", filename))
    with open(filepath, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))
    return result  

def tempStatsUpload(end_date = None):
    # home_team = game['teams']['home']['team']['name']
    # if home_team == "Montréal Canadiens":
    #     home_team = "Montreal Canadiens" #encoding workaround
    # away_team = game['teams']['away']['team']['name']
    # if away_team == "Montréal Canadiens":
    #     away_team = "Montreal Canadiens" #encoding workaround
    # date = game['gameDate'] # first need to format date to remove timestamp
    # date = date[:-10] #trim timestamp 
    ##change date format to dd-mm-yy as API returns YYYY-MM-DD
    #updates csv row with home team stats
    if end_date is None:
        end_date = utils.getTodaysDate("%Y-%m-%d")
    basepath = path.dirname(__file__)
    filename = "NHL 2022-23 Games.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)
    #game_id=2022020326
    for row_index, row in df.iterrows():
        date = row["date"]
        if date == "2022-10-07" or date == "2022-10-08" or date == "2021-10-12" or date == "2021-10-13":
            continue #skip first games
        if date == end_date:
            break    #stop reading csv file as team stats file won't exist for tomorrow
        home_team = row["home_team"]
        away_team = row["away_team"]
        print(date,home_team,away_team)
        game_dict = importCsv.getTeamsStats(date, home_team, away_team, format = True, backdate = True)
        #print(game_dict)
        if game_dict == {}:
            print("Team data missing for: \n")
            print(date,home_team,away_team) # print for debugging purposes
            continue    # if team stats file not found, don't touch csv rows
        #2 checks if dictionary present but one team's data is missing
        if "home_team" not in list(game_dict.keys()):
            print(home_team + " stats missing from " + date )
            continue
        if "away_team" not in list(game_dict.keys()):
            print(away_team + " stats missing from " + date )
            continue
        home_team_dict = game_dict['home_team']
        away_team_dict = game_dict['away_team']
        df.loc[row_index,"h_point%"] = home_team_dict['Point %']
        df.loc[row_index,"h_cf%"] = home_team_dict['CF%']
        df.loc[row_index,"h_ff%"] = home_team_dict['FF%']
        df.loc[row_index,"h_sf%"] = home_team_dict['SF%']
        df.loc[row_index,"h_gf%"] = home_team_dict['GF%']
        df.loc[row_index,"h_xgf%"] = home_team_dict['xGF%']
        df.loc[row_index,"h_scf%"] = home_team_dict['SCF%']
        df.loc[row_index,"h_scsf%"] = home_team_dict['SCSF%']
        df.loc[row_index,"h_scgf%"] = home_team_dict['SCGF%']
        df.loc[row_index,"h_scsh%"] = home_team_dict['SCSH%']
        df.loc[row_index,"h_scsv%"] = home_team_dict['SCSV%']
        df.loc[row_index,"h_hdsf%"] = home_team_dict['HDSF%']
        df.loc[row_index,"h_hdgf%"] = home_team_dict['HDGF%']
        df.loc[row_index,"h_hdsh%"] = home_team_dict['HDSH%']
        df.loc[row_index,"h_hdsv%"] = home_team_dict['HDSV%']
        df.loc[row_index,"h_mdsf%"] = home_team_dict['MDSF%']
        df.loc[row_index,"h_mdgf%"] = home_team_dict['MDGF%']
        df.loc[row_index,"h_mdsh%"] = home_team_dict['MDSH%']
        df.loc[row_index,"h_mdsv%"] = home_team_dict['MDSV%']
        df.loc[row_index,"h_ldsf%"] = home_team_dict['LDSF%']
        df.loc[row_index,"h_ldgf%"] = home_team_dict['LDGF%']
        df.loc[row_index,"h_ldsh%"] = home_team_dict['LDSH%']
        df.loc[row_index,"h_ldsv%"] = home_team_dict['LDSV%']
        df.loc[row_index,"h_sh%"] = home_team_dict['SH%']
        df.loc[row_index,"h_sv%"] = home_team_dict['SV%']
        df.loc[row_index,"h_PDO"] = home_team_dict['PDO']
        #away team
        df.loc[row_index,"a_point%"] = away_team_dict['Point %']
        df.loc[row_index,"a_cf%"] = away_team_dict['CF%']
        df.loc[row_index,"a_ff%"] = away_team_dict['FF%']
        df.loc[row_index,"a_sf%"] = away_team_dict['SF%']
        df.loc[row_index,"a_gf%"] = away_team_dict['GF%']
        df.loc[row_index,"a_xgf%"] = away_team_dict['xGF%']
        df.loc[row_index,"a_scf%"] = away_team_dict['SCF%']
        df.loc[row_index,"a_scsf%"] = away_team_dict['SCSF%']
        df.loc[row_index,"a_scgf%"] = away_team_dict['SCGF%']
        df.loc[row_index,"a_scsh%"] = away_team_dict['SCSH%']
        df.loc[row_index,"a_scsv%"] = away_team_dict['SCSV%']
        df.loc[row_index,"a_hdsf%"] = away_team_dict['HDSF%']
        df.loc[row_index,"a_hdgf%"] = away_team_dict['HDGF%']
        df.loc[row_index,"a_hdsh%"] = away_team_dict['HDSH%']
        df.loc[row_index,"a_hdsv%"] = away_team_dict['HDSV%']
        df.loc[row_index,"a_mdsf%"] = away_team_dict['MDSF%']
        df.loc[row_index,"a_mdgf%"] = away_team_dict['MDGF%']
        df.loc[row_index,"a_mdsh%"] = away_team_dict['MDSH%']
        df.loc[row_index,"a_mdsv%"] = away_team_dict['MDSV%']
        df.loc[row_index,"a_ldsf%"] = away_team_dict['LDSF%']
        df.loc[row_index,"a_ldgf%"] = away_team_dict['LDGF%']
        df.loc[row_index,"a_ldsh%"] = away_team_dict['LDSH%']
        df.loc[row_index,"a_ldsv%"] = away_team_dict['LDSV%']
        df.loc[row_index,"a_sh%"] = away_team_dict['SH%']
        df.loc[row_index,"a_sv%"] = away_team_dict['SV%']
        df.loc[row_index,"a_PDO"] = away_team_dict['PDO']
    filename = "NHL 2021-22 Games Stat Upload Test.csv"
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df.to_csv(filepath, index=False)

#tempStatsUpload(date="2022-11-26",home_team = "Columbus Blue Jackets",away_team= "New York Islanders")
# basepath = path.dirname(__file__)
# filename = "NHL 2022-23 Games.csv"
# filepath = path.abspath(path.join(basepath, "..", "data", filename))
# df = pd.read_csv(filepath)

# game_id = 2022020365
# row_index =  df.index[df['game_id'] == game_id]
# game_date = df.loc[row_index,"date"].item()
# home_team = df.loc[row_index,"home_team"].item()
# away_team = df.loc[row_index,"away_team"].item()
# print(game_date,home_team,away_team)

# game_id=2022020326
# row_index =  df.index[df['game_id'] == game_id]
# for index,row in df.iterrows():
#     print(row["date"])
#     if index > 2:
#         break
#tempStatsUpload(end_date = "2022-11-30")
#uploadResultsAndStats()
#tempStatsUpload(end_date = "2022-04-30")
