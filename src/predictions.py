from importCsv import getTeamsStats
import utils
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import seaborn as sb
sb.set()
import datetime as dt
import pickle
from os import path
from logisticRegression import loadModel

def predictGame(home_team, away_team, date = None):
    if date is None:
        date = utils.getTodaysDate()
    teamsCsv = getTeamsStats(date, home_team, away_team)
    home_team_xgf_percent = float(teamsCsv['home_team']['xGF%'])
    away_team_xgf_percent = float(teamsCsv['away_team']['xGF%'])
    home_team_hdcf_percent = float(teamsCsv['home_team']['HDCF%']) # High Danger Chances For %
    away_team_hdcf_percent = float(teamsCsv['away_team']['HDCF%'])

    total_percentage = home_team_xgf_percent + away_team_xgf_percent + home_team_hdcf_percent + away_team_hdcf_percent
    home_team_percentage = float("{:.2f}".format(((home_team_xgf_percent + home_team_hdcf_percent) / total_percentage)))
    away_team_percentage = float("{:.2f}".format(((away_team_xgf_percent + away_team_hdcf_percent) / total_percentage)))
    result = [home_team_percentage, away_team_percentage]
    #print(f"{home_team} {home_team_percentage*100}% - {away_team_percentage*100}% {away_team}")
    return result

def processGame(prediction, result):
    home_team_prob = []
    home_team_prob.append(prediction[0])
    log_loss = utils.logLoss([result], home_team_prob)
    return log_loss
def logRegPredictGame(home_team, away_team, date = None):
    if date is None:
        date = utils.getTodaysDate()
    game_dict = getTeamsStats(date, home_team, away_team)
    home_team_dict = game_dict['home_team']
    away_team_dict = game_dict['away_team']
    df = utils.createGameDataframe(home_team_dict,away_team_dict)
    #load model
    model_name = "log_reg_12-12-22_2"
    model = loadModel(model_name)
    prediction = model.predict(df)
    return prediction[0]
#will use logistic regression model on all games of a given slate
def logRegPredictSlate(date):
    #get games for given date
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", "Predictions.csv"))
    df = pd.read_csv(filepath)
    games = df.loc[df['date'] == date]
    print(games)
    for game_index, game in games.iterrows():
        h_team  = game['home_team']
        a_team  = game['away_team']
        datum   = game['date'] # need to convert from YYYY-MM-DD to DD-MM-YYYY for stats file retrieval
        datum   = utils.convertDateStringFormat(datum,in_format="%Y-%m-%d",out_format = "%d-%m-%y", delta = 2)
        game_id = game['game_id']
        predicted_result = logRegPredictGame(home_team = h_team, away_team = a_team, date = datum)
        print(h_team + " - " + a_team + " will result as: " + str(predicted_result))
        savePrediction(game_id,type='logreg', prediction = predicted_result)

def savePrediction(game_id, type, prediction):
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", "Predictions.csv"))
    df = pd.read_csv(filepath)
    #find given game by id
    row_index = df.index[df['game_id'] == game_id]
    if type == 'logreg':
        df.loc[row_index,'logreg_prediction'] = prediction
    df.to_csv(filepath, index=False)

def scorePredictions():
    # open predictions file
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", "Predictions.csv"))
    df = pd.read_csv(filepath)
    logreg_prediction_count = df.count().loc["logreg_prediction"]
    logreg_correct_prediction_count = 0
    counter = 0
    for row_index, row in df.iterrows():
        if not pd.isna(row["result"]) and not pd.isna(row["logreg_prediction"]):
             if int(row["result"]) == int(row["logreg_prediction"]):
                logreg_correct_prediction_count += 1
        else:
            counter += 1
            if counter == logreg_prediction_count:
                break
            continue
        counter += 1
        if counter == logreg_prediction_count:
            break
    logreg_success_rate = logreg_correct_prediction_count / logreg_prediction_count
        
    
    print("Logreg prediction count: ", logreg_prediction_count)
    print("Correct logreg prediction count: ", logreg_correct_prediction_count)

    #write prediction score statistics into scoring file  
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", "Predictions Scoring.csv"))
    df2 = pd.read_csv(filepath)
    logreg_index = df2.index[df2['model'] == "logreg"]
    df2.loc[logreg_index,"games_predicted"] = logreg_prediction_count
    df2.loc[logreg_index,"correct_predictions"] = logreg_correct_prediction_count
    df2.loc[logreg_index,"correct_percentage"]= logreg_success_rate
    df2.to_csv(filepath, index=False)

scorePredictions()
