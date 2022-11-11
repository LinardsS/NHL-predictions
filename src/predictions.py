from importCsv import getTeamsStats

def predictGame(home_team, away_team):
    teamsCsv = getTeamsStats('11-11-22', home_team, away_team)
    home_team_xgf_percent = float(teamsCsv['home_team']['xGF%'])
    away_team_xgf_percent = float(teamsCsv['away_team']['xGF%'])
    home_team_hdcf_percent = float(teamsCsv['home_team']['HDCF%']) # High Danger Chances For %
    away_team_hdcf_percent = float(teamsCsv['away_team']['HDCF%'])

    total_percentage = home_team_xgf_percent + away_team_xgf_percent + home_team_hdcf_percent + away_team_hdcf_percent
    home_team_percentage = "{:.2f}".format(((home_team_xgf_percent + home_team_hdcf_percent) / total_percentage)*100)
    away_team_percentage = "{:.2f}".format(((away_team_xgf_percent + away_team_hdcf_percent) / total_percentage)*100)

    print(f"{home_team} {home_team_percentage}% - {away_team_percentage}% {away_team}")

predictGame("Toronto Maple Leafs", "Pittsburgh Penguins")