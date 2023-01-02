from downloadCsv import downloadTeamStats
from uploadResults import uploadResultsAndStats
from utils import getTodaysDate, getTomorrowsDate
from predictions import predictSlate, scorePredictions
import sys
from os import path
basepath = path.dirname(__file__)
todays_date = getTodaysDate()
todays_date = todays_date + '.txt'
filepath = path.abspath(path.join(basepath, "..", "data/daily logs", todays_date))
sys.stdout = open(filepath, 'w')

downloadTeamStats(today = True, date = None, file_date = None) # downloads team stats file
uploadResultsAndStats() # updates games file with results of last night's games and adds stats for both teams at the time of game
# result upload to predictions file incorporated into uploadResultsAndStats 
# so as not to send duplicate requests for game results

#score predictions from last night
scorePredictions()

#predict next night's games
tomorrows_date = getTomorrowsDate(format = "%Y-%m-%d")
predictSlate(date = tomorrows_date)

sys.stdout.close()