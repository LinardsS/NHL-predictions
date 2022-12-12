from downloadCsv import downloadTeamStats
from uploadResults import uploadResultsAndStats
from utils import getTodaysDate
from predictions import logRegPredictSlate

downloadTeamStats(today = True, date = None, file_date = None) # downloads team stats file
uploadResultsAndStats() # updates games file with results of last night's games and adds stats for both teams at the time of game
#score last night's predictions
## CODE WILL GO HERE LATER

#predict next night's games
todays_date = getTodaysDate(format = "%Y-%m-%d")
logRegPredictSlate(date = todays_date)
