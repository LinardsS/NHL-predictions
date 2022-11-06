import csv
from os import path

basepath = path.dirname(__file__)
FILE_PREFIX = 'Team Season Totals - '
DATE = '06-11-22'
filename = FILE_PREFIX + DATE + '.csv'
filepath = path.abspath(path.join(basepath, "..", "data", filename))
#'data/' + FILE_PREFIX + '06-11-22.csv'

with open(filepath) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f"\t{row['Team']} has xGFp of {row['xGF%']}")
            line_count += 1
    print(f'Processed {line_count} lines.')