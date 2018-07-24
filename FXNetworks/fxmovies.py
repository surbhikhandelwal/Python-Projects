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


show_href =[]
service_videos ={}
launch_id =[]
credit =[]
release_year =0
driver.get ("http://www.fxnetworks.com/movies")
time.sleep(5)
shows =driver.find_elements_by_xpath(".//*[@id='entertainment-listing']/div[2]/ul/li/a")
# scroll_from = 0
# scroll_limit = 3000
# while(len(shows)<134):
# 	# print(len(shows))
# 	driver.execute_script("window.scrollTo(%d, %d);" %(scroll_from, scroll_from+scroll_limit))
# 	scroll_from += scroll_limit
# 	shows =driver.find_elements_by_xpath(".//*[@id='entertainment-listing']/div[2]/ul/li/a")
# time.sleep(5)
driver.execute_script("window.scrollTo(0, 0)")
print(len(shows))
for s in range (len(shows)):
	show_href.append(shows[s].get_attribute('href'))
print(show_href)
for m in range (len(shows)):
	try:
		print("show number:  [%s]"%(m,))
		driver.get(show_href[m])
		movie_link=driver.find_element_by_xpath(".//*[@id='movie-detail']/div[2]/section[1]/a")
		movie_href =movie_link.get_attribute('href')
		movie_id =movie_href.split("/")[-1].encode('ascii', 'ignore')
		launch_id.append(movie_id)
		print(launch_id)
		movie_title =driver.find_element_by_xpath(".//*[@id='movie-detail']/div[2]/section[2]/div/h2").text.encode('ascii', 'ignore')
		print(movie_title)
		movie_team =driver.find_element_by_xpath(".//*[@id='movie-detail']/div[2]/section[2]/div/p[2]").text.encode('ascii', 'ignore')
		team =movie_team.split(",")
		for te in range (len(team)):
			credit.append(team[te])
		print(credit)
		try:
			driver.get("https://www.google.com")
			time.sleep(6)
			driver.find_element_by_xpath("(//input)[4]").send_keys("%s movie"%(movie_title,))
			driver.find_element_by_xpath("(//input)[4]").send_keys("\n")
			time.sleep(3)
			year =driver.find_element_by_xpath(".//*[@id='rhs_block']/div[1]/div[1]/div/div[1]/div[2]/div[5]/div/div[3]/div/div/span[2]").text
			release_year =year.split(" ")[2].encode('ascii', 'ignore')
			driver.get (series_url)
			time.sleep(5)
			print (release_year)
		except Exception as ex :
			print (ex)
			# driver.get (series_url)
			time.sleep(5)
		service_videos ["fxnetwork"] =launch_id
		res=[today, "FX Movies", movie_title, release_year, credit, service_videos]
		# 	print(res)
		with open(os.getcwd()+'/'+"fx_output_movies"+ '.csv', 'ab+') as mycsvfile:
			thedatawriter =csv.writer(mycsvfile)
			thedatawriter.writerow(res)
			launch_id =[]
			service_videos = {}
			credit =[]
	except Exception as ex:
		print(ex)
		continue

