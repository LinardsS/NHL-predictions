from importCsv import getTeamsStats
import utils

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

a = predictGame("Toronto Maple Leafs", "Pittsburgh Penguins") # 2-4
b = predictGame("Washington Capitals", "Tampa Bay Lightning") # 5-1
c = predictGame("Dallas Stars", "San Jose Sharks")            # 4-5
d = predictGame("Seattle Kraken", "Minnesota Wild")           # 0-1

log_loss = []
predictions = []

log_loss.append(processGame(a, 0))
log_loss.append(processGame(b,1))
log_loss.append(processGame(c,0))
log_loss.append(processGame(d,0))

result = sum(log_loss) / len(log_loss)
print("Log loss for 4 games: " + str(result))