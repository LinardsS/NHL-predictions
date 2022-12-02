from downloadCsv import downloadTeamStats
from uploadResults import uploadResultsAndStats

downloadTeamStats(today = True, date = None, file_date = None) # downloads team stats file
uploadResultsAndStats() # updates games file with results of last night's games and adds stats for both teams at the time of game
