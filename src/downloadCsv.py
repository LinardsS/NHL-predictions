from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import utils

def downloadTeamStats(today, date, file_date):
    directory = r"C:\Users\lats4\Desktop\Kursa darbs\git\NHL-predictions\data"
    chromeOptions = Options()
    chromeOptions.add_experimental_option("prefs",{"download.default_directory": directory})

    if today is True:
        date_stamp = utils.getTodaysDate("%Y-%m-%d",backdate = True) # need to backdate due to NSS storing yesterday's file when accessing it in the morning
        file_datestamp = utils.getTodaysDate(backdate=True)
    else:
        date_stamp = date
        file_datestamp = file_date
    download_url = "https://www.naturalstattrick.com/teamtable.php?fromseason=20222023&thruseason=20222023&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td=";
    #uncomment below if need to download 2021-22 team data
    #download_url = "https://www.naturalstattrick.com/teamtable.php?fromseason=20212022&thruseason=20212022&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td=";
    download_url = download_url + date_stamp

    driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver\chromedriver.exe", chrome_options = chromeOptions)

    driver.get(download_url)

    driver.maximize_window()
    download_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@value, 'CSV (All)')]")))
    #click the download button
    download_button.click()
    time.sleep(3)
    driver.close()

    old_file = os.path.join(directory, "games.csv")
    new_file = os.path.join(directory, "Team Season Totals - " + file_datestamp + ".csv")
    os.rename(old_file, new_file)

# downloadTeamStats(today = False, date = "2022-10-07", file_date="07-10-22")
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
def downloadSeasonTeamStats():
    start_date = date(2021, 10, 12)
    end_date = date(2022, 4, 29)
    for single_date in daterange(start_date, end_date):
        downloadTeamStats(today = False, date = single_date.strftime("%Y-%m-%d"), file_date=single_date.strftime("%d-%m-%y"))
        print(single_date.strftime("%Y-%m-%d") + " processed")
#downloadSeasonTeamStats()