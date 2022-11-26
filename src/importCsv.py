import csv
from os import path
from datetime import date, datetime

def getTeamsStats(date, home_team, away_team, format = None):
    basepath = path.dirname(__file__)
    FILE_PREFIX = 'Team Season Totals - '
    if date is None:
        today = date.today()
        date = today.strftime("%d-%m-%y")
    if format is True:
        datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%y')
    filename = FILE_PREFIX + date + '.csv'
    filepath = path.abspath(path.join(basepath, "..", "data", filename))

    with open(filepath) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        return_dict = {}
        for row in csv_reader:
            if row['Team'] == home_team:
                return_dict['home_team'] = row
            if row['Team'] == away_team:
                return_dict['away_team'] = row
        return return_dict