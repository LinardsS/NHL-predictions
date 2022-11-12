from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import utils

directory = r"C:\Users\lats4\Desktop\Kursa darbs\git\NHL-predictions\data"
chromeOptions = Options()
chromeOptions.add_experimental_option("prefs",{"download.default_directory": directory})

date_stamp = utils.getTodaysDate("%Y-%m-%d")
file_datestamp = utils.getTodaysDate()
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