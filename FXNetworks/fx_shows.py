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
driver.get ("http://www.fxnetworks.com/shows/full-episodes")
time.sleep(5)
shows =driver.find_elements_by_xpath(".//*[@id='entertainment-listing']//ul/li/a[1]")
print(len(shows))
for s in range (len(shows)):
	show_href.append(shows[s].get_attribute('href'))
print(show_href)
for h in range (len(show_href)):
# 	# try:
	driver.get (show_href[h])
	# series_title =show_href[h].split("/")[-1].replace("-"," ").encode('ascii', 'ignore')
	episodes =driver.find_elements_by_xpath(".//*[@id='js-episodes-container']//section[contains(@class,'episode-container accordian')]")
	print(len(episodes))
	for e in range (len(episodes)):
		try:
			episode_link =driver.find_element_by_xpath("(.//*[@id='js-episodes-container']//section[contains(@class,'episode-container accordian')])[%s]/div[2]/div/a[1]"%(e+1,))
			epi_id =episode_link.get_attribute('href').split("/")[-1].encode('ascii', 'ignore')
			launch_id.append(epi_id)
			epi_details =driver.find_element_by_xpath("(.//*[@id='js-episodes-container']//section[contains(@class,'episode-container accordian')])[%s]/div[2]/div[2]/p"%(e+1,)).text
			print(epi_details)
			epi_num =epi_details.split(" ")[-1].split(".")[1].encode('ascii', 'ignore')
			sea_num =epi_details.split(" ")[-2].split(".")[1].encode('ascii', 'ignore')
			series_title =driver.find_element_by_xpath(".//*[@id='js-episodes-container']/div[3]/div[1]/div[3]").text.encode('ascii', 'ignore')
			print(launch_id,epi_num,sea_num)
			epi_title =driver.find_element_by_xpath("(.//*[@id='js-episodes-container']//section[contains(@class,'episode-container accordian')])[%s]/div[2]/div[2]/h2"%(e+1,)).text.encode('ascii', 'ignore')
			epi_date =driver.find_element_by_xpath("(.//*[@id='js-episodes-container']//section[contains(@class,'episode-container accordian')])[%s]/div[2]/div[2]/p[4]"%(e+1,)).text.encode('ascii', 'ignore')
			service_videos ["fxnetwork"] =launch_id
			res=[today, "FX Shows", series_title, release_year, sea_num, epi_num, epi_title, service_videos]
			print(res)
			with open(os.getcwd()+'/'+"fx_output_shows"+ '.csv', 'ab+') as mycsvfile:
				thedatawriter =csv.writer(mycsvfile)
				thedatawriter.writerow(res)
				launch_id =[]
				service_videos = {}
				epi_id=None
			except Exception as ex:
				print(ex)
				continue