from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
import time
import datetime
import csv
import unicodedata
import re
import hashlib
import os
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
today =datetime.date.today()
driver.implicitly_wait(10)
movies_href =[]
service_videos ={}
launch_id =[]
credit =[]
release_year =0
driver.get ("https://play.google.com/store/movies/category/MOVIE")
time.sleep(7)
# driver.execute_script("window.scrollTo(0, 600)")
category =driver.find_elements_by_xpath("//div[contains(@class,'outer-container')]//div[contains(@class,'id-cluster-container')]//a[contains(@class,'see-more play-button')]")
current_url =driver.current_url
print("Num of categories : %s"%(len(category)))
for c in range (len(category)):
	driver.find_element_by_xpath("(//div[contains(@class,'outer-container')]//div[contains(@class,'id-cluster-container')]//a[contains(@class,'see-more play-button')])[%s]"%(c+1,)).click()
	time.sleep(7)
	driver.execute_script("window.scrollTo(0, 5000)")
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, 0)")
	movies_links =driver.find_elements_by_xpath("//div[contains(@class,'id-card-list')]/div/div/a")
	movies_href =[]
	for s in range(len(movies_links)):
		movies_href.append(movies_links[s].get_attribute('href'))
	print(movies_href)
	print("Number of series: %s"%(len(movies_href)))
	for m in range (len(movies_href)):
		driver.get(movies_href[m])
		time.sleep(4)
		movie_id =movies_href[m].split("id=")[-1].encode('ascii', 'ignore')
		launch_id.append(movie_id)
		movie_title= driver.find_element_by_xpath(".//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/div[1]/div[2]/div/div[1]/h1/span").text.encode('ascii', 'ignore')
		air_date =driver.find_element_by_xpath(".//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/div[1]/div[2]/div/div[1]/div/div[1]/span[1]").text.encode('ascii', 'ignore')
		release_year =air_date[-4:]
		team =driver.find_elements_by_xpath(".//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[3]/div/div[2]/div/div/span/a")
		for c in range (len(team)):
			credit.append(team[c].text.encode('ascii', 'ignore'))
		print(launch_id,movie_title,release_year, credit)
		service_videos ["googleplay"] =launch_id
		res=[today, "Google Play Movies", movie_title, release_year, service_videos, credit]
		with open(os.getcwd()+'/'+"GooglePlay_output_movies"+ '.csv', 'ab+') as mycsvfile:
			thedatawriter =csv.writer(mycsvfile)
			thedatawriter.writerow(res)
			launch_id =[]
			service_videos = {}
			credit =[]







	driver.get(current_url)