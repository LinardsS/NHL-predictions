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
def logRegPredictGame(home_team, away_team, date = None, no_point = False):
    if date is None:
        date = utils.getTodaysDate()
    game_dict = getTeamsStats(date, home_team, away_team)
    home_team_dict = game_dict['home_team']
    away_team_dict = game_dict['away_team']
    df = utils.createGameDataframe(home_team_dict,away_team_dict)
    if no_point is True:
        #load model that doesn't include point%
        model_name = "log_reg_NO_POINT_PERCENTAGE_13-12-22"
        model = loadModel(model_name)
        #remove point% from df
        df = df.drop(columns=['h_point%', 'a_point%'])
        prediction = model.predict(df)
    else:
        #load model that includes point%
        model_name = "log_reg_12-12-22_2"
        model = loadModel(model_name)
        prediction = model.predict(df)
    return prediction[0]
#will use all created models on all games of a given slate
def predictSlate(date):
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
        #predict using logreg model that contains point%
        predicted_result = logRegPredictGame(home_team = h_team, away_team = a_team, date = datum, no_point=False)
        print("Logreg: " + h_team + " - " + a_team + " will result as: " + str(predicted_result))
        savePrediction(game_id,type='logreg', prediction = predicted_result)

        #predict using logreg model that doesn't contain point%
        predicted_result_np = logRegPredictGame(home_team = h_team, away_team = a_team, date = datum, no_point=True)
        print("No point%: " + h_team + " - " + a_team + " will result as: " + str(predicted_result_np))
        savePrediction(game_id,type='logreg_np', prediction = predicted_result_np)

        #predict using decision tree model
        predicted_result_dt = dtPredictGame(home_team = h_team, away_team = a_team, date = datum)
        print("Dt: " + h_team + " - " + a_team + " will result as: " + str(predicted_result_dt))
        savePrediction(game_id,type='dt', prediction = predicted_result_dt)

        #predict using random forest(20 estimators) model
        predicted_result_rf = rfPredictGame(home_team = h_team, away_team = a_team, date = datum)
        print("Rf: " + h_team + " - " + a_team + " will result as: " + str(predicted_result_dt))
        savePrediction(game_id,type='rf', prediction = predicted_result_rf)
        

def savePrediction(game_id, type, prediction):
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", "Predictions.csv"))
    df = pd.read_csv(filepath)
    #find given game by id
    row_index = df.index[df['game_id'] == game_id]
    type_prediction = type + "_prediction"
    df.loc[row_index,type_prediction] = prediction
    df.to_csv(filepath, index=False)

def scorePredictions():
    # open predictions file
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", "Predictions.csv"))
    df = pd.read_csv(filepath)
    logreg_score = scorePrediction(df, "logreg_prediction")
    logreg_prediction_count = logreg_score["prediction_count"]
    logreg_correct_prediction_count = logreg_score["correct_prediction_count"]
    logreg_success_rate = logreg_score["success_rate"]
        
    print("Logreg prediction count: ", logreg_prediction_count)
    print("Correct logreg prediction count: ", logreg_correct_prediction_count)

    logreg_np_score = scorePrediction(df, "logreg_np_prediction")
    logreg_np_prediction_count = logreg_np_score["prediction_count"]
    logreg_np_correct_prediction_count = logreg_np_score["correct_prediction_count"]
    logreg_np_success_rate = logreg_np_score["success_rate"]
    print("Logreg_np prediction count: ", logreg_np_prediction_count)
    print("Correct logreg_np prediction count: ", logreg_np_correct_prediction_count)

    dt_score = scorePrediction(df, "dt_prediction")
    dt_prediction_count = dt_score["prediction_count"]
    dt_correct_prediction_count = dt_score["correct_prediction_count"]
    dt_success_rate = dt_score["success_rate"]
    print("Decision tree prediction count: ", dt_prediction_count)
    print("Correct decision tree prediction count: ", dt_correct_prediction_count)

    rf_score = scorePrediction(df, "rf_prediction")
    rf_prediction_count = rf_score["prediction_count"]
    rf_correct_prediction_count = rf_score["correct_prediction_count"]
    rf_success_rate = rf_score["success_rate"]
    print("Random forest prediction count: ", rf_prediction_count)
    print("Correct random forest prediction count: ", rf_correct_prediction_count)

    #write prediction score statistics into scoring file
    writePredictionScore("logreg", logreg_prediction_count, logreg_correct_prediction_count, logreg_success_rate)
    writePredictionScore("logreg_np", logreg_np_prediction_count, logreg_np_correct_prediction_count, logreg_np_success_rate)  
    writePredictionScore("dt", dt_prediction_count, dt_correct_prediction_count, dt_success_rate) 
    writePredictionScore("rf", rf_prediction_count, rf_correct_prediction_count, rf_success_rate) 
    
def scorePrediction(df, prediction_type):
    prediction_count = len(df.loc[
    (df['result'].eq(1) | df['result'].eq(0)) & (df[prediction_type].eq(1) | df[prediction_type].eq(0))
])
    correct_prediction_count = 0
    for row_index, row in df.iterrows():
        if not pd.isna(row["result"]) and not pd.isna(row[prediction_type]): # ja abi netuksi - apstrada
             if int(row["result"]) == int(row[prediction_type]): # ja rezultats sakrit ar prognozi, prognoze pareiza
                correct_prediction_count += 1
        else:
            if pd.isna(row["result"]) and pd.isna(row[prediction_type]): #ja abi tuksi, neapstradat talak
                break
            if pd.isna(row["result"]): # rezultats tukss bet prognoze ir - beidz
                break
            if pd.isna(row[prediction_type]): #rezultats ir, bet prognoze tuksa - nenem vera so rindu
                continue
    success_rate = correct_prediction_count / prediction_count
    return_dict = {}
    return_dict["correct_prediction_count"] = correct_prediction_count
    return_dict["prediction_count"] = prediction_count
    return_dict["success_rate"] = success_rate
    return return_dict

def writePredictionScore(prediction_type, pred_count, correct_pred_count, success_rate):
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", "Predictions Scoring.csv"))
    df = pd.read_csv(filepath)
    index = df.index[df['model'] == prediction_type]
    df.loc[index,"games_predicted"] = pred_count
    df.loc[index,"correct_predictions"] = correct_pred_count
    df.loc[index,"correct_percentage"]= success_rate
    df.to_csv(filepath, index=False)

#decision tree
def dtPredictGame(home_team, away_team, date = None):
    if date is None:
        date = utils.getTodaysDate()
    game_dict = getTeamsStats(date, home_team, away_team)
    home_team_dict = game_dict['home_team']
    away_team_dict = game_dict['away_team']
    df = utils.createGameDataframe(home_team_dict,away_team_dict)
    #load decision tree model 
    model_name = "dt_30-12-22"
    model = loadModel(model_name)
    #remove point% from df
    df = df.drop(columns=['h_point%', 'a_point%'])
    prediction = model.predict(df)
    return prediction[0]

#random forest
def rfPredictGame(home_team, away_team, date = None):
    if date is None:
        date = utils.getTodaysDate()
    game_dict = getTeamsStats(date, home_team, away_team)
    home_team_dict = game_dict['home_team']
    away_team_dict = game_dict['away_team']
    df = utils.createGameDataframe(home_team_dict,away_team_dict)
    #load random forest with 20 estimators model 
    model_name = "rf_estimators20_01-01-23"
    model = loadModel(model_name)
    #remove point% from df
    df = df.drop(columns=['h_point%', 'a_point%'])
    prediction = model.predict(df)
    return prediction[0]