import numpy as np
from datetime import date,timedelta, datetime
import pandas as pd
from os import path

def logLikelihood(actual, predicted):
    """
    Computes the log likelihood.

    This function computes the log likelihood between two numbers,
    or for element between a pair of lists or numpy arrays.

    :param actual: int, float, list of numbers, numpy array
                    The ground truth value
    :param predicted: same type as actual
                     The predicted value

    :returns: double or list of doubles
             The log likelihood error between actual and predicted
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    for i in range(0, predicted.shape[0]):
        predicted[i] = min(max(1e-15, predicted[i]), 1 - 1e-15)
    err = np.seterr(all='ignore')
    score = -(actual * np.log(predicted) + (1 - actual) * np.log(1 - predicted))
    np.seterr(
        divide=err['divide'],
        over=err['over'],
        under=err['under'],
        invalid=err['invalid'])
    if isinstance(score, np.ndarray):
        score[np.isnan(score)] = 0
    else:
        if np.isnan(score):
            score = 0
    return score

def logLoss(actual, predicted):
    """
    Computes the log loss.

    This function computes the log loss between two lists
    of numbers.

    :param actual: int, float, list of numbers, numpy array
                    The ground truth value
    :param predicted: same type as actual
                     The predicted value

    :returns: double
             The log loss between actual and predicted
    """
    return np.mean(logLikelihood(actual, predicted)) 

def getTodaysDate(format = "%d-%m-%y",backdate = None):
    today = date.today()
    if backdate is True:
        today = today - timedelta(days=1)
    return today.strftime(format)
def getYesterdaysDate(format = "%d-%m-%y"):
    yesterday = date.today() - timedelta(1)
    return yesterday.strftime(format)
def getTomorrowsDate(format = "%d-%m-%y"):
    tomorrow = date.today() + timedelta(1)
    return tomorrow.strftime(format)
def deleteCsvFirstColumn(filename):
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)
    print("Columns: " + df.columns)
    # Select first column
    first_column = df.columns[0]
    # Delete first column
    df = df.drop([first_column], axis=1)
    df.to_csv(filepath, index=False)
def createGameDataframe(home_team_dict,away_team_dict):
    home_team_dict = convertTeamDictionary(home_team_dict, home_team = True)
    away_team_dict = convertTeamDictionary(away_team_dict, home_team = False)
    res_dictionary = home_team_dict | away_team_dict #merge the two dictionaries
    df = pd.DataFrame([res_dictionary])
    return df
def convertTeamDictionary(dictionary, home_team):
    # determine the prefix for keys - h_ for home, a_ for away
    if home_team is True:
        prefix = "h_"
    else:
        prefix = "a_"
    temp_dict = {}
    temp_dict[prefix + "point%"] = dictionary['Point %']
    temp_dict[prefix + "cf%"] = dictionary['CF%']
    temp_dict[prefix + "ff%"] = dictionary['FF%']
    temp_dict[prefix + "sf%"] = dictionary['SF%']
    temp_dict[prefix + "gf%"] = dictionary['GF%']
    temp_dict[prefix + "xgf%"] = dictionary['xGF%']
    temp_dict[prefix + "scf%"] = dictionary['SCF%']
    temp_dict[prefix + "scsf%"] = dictionary['SCSF%']
    temp_dict[prefix + "scgf%"] = dictionary['SCGF%']
    temp_dict[prefix + "scsh%"] = dictionary['SCSH%']
    temp_dict[prefix + "scsv%"] = dictionary['SCSV%']
    temp_dict[prefix + "hdsf%"] = dictionary['HDSF%']
    temp_dict[prefix + "hdgf%"] = dictionary['HDGF%']
    temp_dict[prefix + "hdsh%"] = dictionary['HDSH%']
    temp_dict[prefix + "hdsv%"] = dictionary['HDSV%']
    temp_dict[prefix + "mdsf%"] = dictionary['MDSF%']
    temp_dict[prefix + "mdgf%"] = dictionary['MDGF%']
    temp_dict[prefix + "mdsh%"] = dictionary['MDSH%']
    temp_dict[prefix + "mdsv%"] = dictionary['MDSV%']
    temp_dict[prefix + "ldsf%"] = dictionary['LDSF%']
    temp_dict[prefix + "ldgf%"] = dictionary['LDGF%']
    temp_dict[prefix + "ldsh%"] = dictionary['LDSH%']
    temp_dict[prefix + "ldsv%"] = dictionary['LDSV%']
    temp_dict[prefix + "sh%"] = dictionary['SH%']
    temp_dict[prefix + "sv%"] = dictionary['SV%']
    temp_dict[prefix + "PDO"] = dictionary['PDO']
    return temp_dict

def convertDateStringFormat(date,in_format,out_format, delta = None):
    if delta is None:
        return datetime.strptime(date, in_format).strftime(out_format)
    else:
        date = datetime.strptime(date, in_format)
        date = date-timedelta(days=delta)
        return date.strftime(out_format)

def addColumnToCsv(filename):
    #enter name of column in CSV yourself and this will add commas for new column in each row
    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "data", filename))
    df = pd.read_csv(filepath)
    df.to_csv(filepath, index=False)
