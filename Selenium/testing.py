from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Import needed to tackle dropdowns
from selenium.webdriver.support.ui import Select

# Importing the By for finding elements
from selenium.webdriver.common.by import By

import time

# These 2 lines solves the problem of the ChromeDriver automatically closing itself after runtime
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# This installs the version of ChromeDriver that will work with your chrome
# options= options is very important for it to not close during runtime
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

# Pull the website we are going to automate & scrape
driver.get("https://www.adamchoi.co.uk/overs/detailed")

# Syntax to find_element by XPATH in Selenium 4 , https://selenium-python.readthedocs.io/locating-elements.html
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click() # Automate clicking on a button

# This is another to find element in Selenium 4, however the official docs tell us otherwise
# all_matches_button = driver.find_element(by="xpath", value='//label[@analytics-event="All matches"]')


dropdown = Select(driver.find_element(By.ID, 'country'))
dropdown.select_by_visible_text('Italy')


# wait for the webpage to load all the data, and then the code below will excecute
time.sleep(40)


# find_element(By.TAG_NAME, "tag name")
matches = driver.find_elements(By.TAG_NAME, "tr")
# matches = driver.find_elements(by="tag-name", value='tr') , another way to do it

# Initializing lists to prepare for data extraction
date = []
home_team = []
score = []
away_team = []


# Appending data into the dataframe
for match in matches:
    date.append(match.find_element(By.XPATH, './td[1]').text) # ./ references to the matches -> which is the parent node of td
    home = match.find_element(By.XPATH, './td[2]').text
    home_team.append(home)
    print(home)
    score.append( match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)
driver.quit()

# Printing and saving data into csv file
df = pd.DataFrame({'date': date, 'Home_Team': home_team, 'Score': score, 'Away_Team': away_team})
df.to_csv('Football_data_italyiouk.csv', index= True)
print(df)
