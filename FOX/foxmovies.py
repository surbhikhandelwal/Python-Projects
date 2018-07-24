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
service_videos ={}
launch_id =[]
credit =[]
release_year =0
driver.get ("https://www.fox.com/movies/")
time.sleep(5)
shows =driver.find_elements_by_xpath("//div[contains(@class,'Tile_tile')]")
scroll_from = 0
scroll_limit = 3000
while(len(shows)<133):
	# print(len(shows))
	driver.execute_script("window.scrollTo(%d, %d);" %(scroll_from, scroll_from+scroll_limit))
	scroll_from += scroll_limit
	shows =driver.find_elements_by_xpath("//div[contains(@class,'Tile_tile')]/div/a")
time.sleep(8)
print(len(shows))
driver.execute_script("window.scrollTo(0, 0)")
time.sleep(5)
for m in range (len(shows)):
	show_href.append(shows[m].get_attribute('href'))
print(show_href)
for h in range (len(shows)):
	driver.get (show_href[h])
	print("show_num : [%s]"%(h,))
	movie_link =driver.find_element_by_xpath("//a[contains(@class,'Branding_topButton')]")
	movie_href=movie_link.get_attribute('href')
	movie_id =movie_href.split("/")[-2].encode('ascii', 'ignore')
	launch_id.append(movie_id)
	metadata =driver.find_element_by_xpath("//div[contains(@class,'Branding_metadata')]").text
	release_year =metadata.split(" ")[0].encode('ascii', 'ignore')
	movie_title =driver.find_element_by_xpath("//h1[contains(@class,'Branding_name')]").text.encode('ascii', 'ignore')
	team =driver.find_elements_by_xpath("//span[contains(@class,'Branding_starringInner')]/div/span")
	for t in range (len(team)):
		star=driver.find_element_by_xpath("(//span[contains(@class,'Branding_starringInner')]/div/span)[%s]"%(t+1,)).text.encode('ascii', 'ignore')
		credit.append(star)
	service_videos ["fox"] =launch_id
	res=[today, "FOX Movies", movie_title, release_year, credit, service_videos]
	with open(os.getcwd()+'/'+"fox_output_movies"+ '.csv', 'ab+') as mycsvfile:
		thedatawriter =csv.writer(mycsvfile)
		thedatawriter.writerow(res)
		launch_id =[]
		service_videos = {}
		credit =[]
		