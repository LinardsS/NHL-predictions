import numpy as np
from datetime import date

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

def getTodaysDate(format = "%d-%m-%y"):
    today = date.today()
    return today.strftime(format)
