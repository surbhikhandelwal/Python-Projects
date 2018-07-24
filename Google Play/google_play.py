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

def check_exists_by_xpath(xpath):
    try:
    	driver.find_element_by_xpath("%s"%(xpath,)).send_keys("\n")
    except ElementNotVisibleException:
        print ("element not found for click")

def text_from_xpath(xpath):
	text =None
	try:
		text =driver.find_element_by_xpath("%s"%(xpath,)).text
		time.sleep(2)
		return text
	except ElementNotVisibleException:	
		print ("element not found for text")

def element_exists(xpath):
	try:
		driver.find_element_by_xpath("%s"%(xpath,))
		time.sleep(2)
		return True
	except ElementNotVisibleException:	
		print ("element not found for text")
		return False

show_href =[]
season_href =[]
serv_href =[]
service_videos ={}
launch_id =[]
release_year =0
driver.get ("https://www.justwatch.com/us/provider/google-play-movies?content_type=show")
time.sleep(5)
shows =driver.find_elements_by_xpath(".//*[@id='content']/div/div[2]/div")
scroll_from = 0
scroll_limit = 3000
while(len(shows)<1500):
	# print(len(shows))
	driver.execute_script("window.scrollTo(%d, %d);" %(scroll_from, scroll_from+scroll_limit))
	scroll_from += scroll_limit
	time.sleep(3)
	shows =driver.find_elements_by_xpath(".//*[@id='content']/div/div[2]/div")
time.sleep(15)
driver.execute_script("window.scrollTo(0, 0)")
print(len(shows))
for s in range (len(shows)):
	show_link =driver.find_element_by_xpath("(.//*[@id='content']/div/div[2]/div//div[@class='main-content__poster__image']/a)[%s]"%(s+1,))
	show_href.append(show_link.get_attribute('href'))
print(show_href)
for h in range (len(show_href)):
	driver.get(show_href[h])
	seasons =driver.find_elements_by_xpath("//div[@class='detail-infos__seasons__season']/a[1]")
	for se in range (len(seasons)):
		season_href.append(seasons[se].get_attribute('href'))
		for sh in range (len(seasons)):
			driver.get (season_href[sh])
			episodes =driver.find_elements_by_xpath("html/body/div[2]/div/div[3]/div/div/div[1]/div[3]/newest-episodes/div//div[@class='panel']")
			for e in range (len(episodes)):
				driver.find_element_by_xpath("(html/body/div[2]/div/div[3]/div/div/div[1]/div[3]/newest-episodes/div//div[@class='panel'])[%s]"%(e+1,)).click()
				services =driver.find_elements_by_xpath("//newest-episodes[@target-title ='::title.title']//div[contains(@class,'panel')]//a[@target='_blank']")
				for serv in range (len(services)):
					serv_href.append(services[serv].get_attribute('href'))
					current_url =driver.current_url
				print(serv_href)
				for serv in range (len(serv_href)):
					if("google" in serv_href[serv]):
						driver.get(serv_href[serv])
						epi_link =driver.current_url
						driver.get (current_url)
						print  (epi_link)