from datetime import date
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
        date_stamp = utils.getTodaysDate("%Y-%m-%d")
        file_datestamp = utils.getTodaysDate()
    else:
        date_stamp = date
        file_datestamp = file_date
    download_url = "https://www.naturalstattrick.com/teamtable.php?fromseason=20222023&thruseason=20222023&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td=";
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
downloadTeamStats(today = True) # this will get auto-executed daily, don't touch

#will go through dates from beginning of season until  25-10-22 to download missing team stats files
# downloadTeamStats(today = False, date = "2022-10-07", file_date="07-10-22")
# downloadTeamStats(today = False, date = "2022-10-08", file_date="08-10-22")
# downloadTeamStats(today = False, date = "2022-10-09", file_date="09-10-22")
# downloadTeamStats(today = False, date = "2022-10-10", file_date="10-10-22")
# downloadTeamStats(today = False, date = "2022-10-11", file_date="11-10-22")
# downloadTeamStats(today = False, date = "2022-10-12", file_date="12-10-22")
# downloadTeamStats(today = False, date = "2022-10-13", file_date="13-10-22")
# downloadTeamStats(today = False, date = "2022-10-14", file_date="14-10-22")
# downloadTeamStats(today = False, date = "2022-10-15", file_date="15-10-22")
# downloadTeamStats(today = False, date = "2022-10-16", file_date="16-10-22")
# downloadTeamStats(today = False, date = "2022-10-17", file_date="17-10-22")
# downloadTeamStats(today = False, date = "2022-10-18", file_date="18-10-22")
# downloadTeamStats(today = False, date = "2022-10-19", file_date="19-10-22")
# downloadTeamStats(today = False, date = "2022-10-20", file_date="20-10-22")
# downloadTeamStats(today = False, date = "2022-10-21", file_date="21-10-22")
# downloadTeamStats(today = False, date = "2022-10-22", file_date="22-10-22")
# downloadTeamStats(today = False, date = "2022-10-23", file_date="23-10-22")
# downloadTeamStats(today = False, date = "2022-10-24", file_date="24-10-22")
#downloadTeamStats(today = False, date = "2022-10-30", file_date="30-10-22")
