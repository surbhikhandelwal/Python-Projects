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
release_year =0
driver.get ("https://www.fox.com/shows/collection/all%20shows")
time.sleep(5)
shows =driver.find_elements_by_xpath("//div[contains(@class,'TileGrid_grid_')]/div")
scroll_from = 0
scroll_limit = 3000
while(len(shows)<104):
	# print(len(shows))
	driver.execute_script("window.scrollTo(%d, %d);" %(scroll_from, scroll_from+scroll_limit))
	scroll_from += scroll_limit
	shows =driver.find_elements_by_xpath("//div[contains(@class,'TileGrid_grid_')]/div/div/a")
time.sleep(5)
driver.execute_script("window.scrollTo(0, 0)")
print(len(shows))
for s in range (len(shows)):
	show_href.append(shows[s].get_attribute('href'))
print(show_href)
print(len(show_href))
for h in range (len(show_href)):
	print("Show number: [%s]"%(h,))
	driver.get(show_href[h])
	time.sleep(5)
	episodes =driver.find_elements_by_xpath("//div[@name='SERIES_SCROLL_ELEMENT']//div[contains(@class,'SeriesDetail_tabContent')]/div//div[contains(@class,'Tile_tile')]")
	for e in range (len(episodes)):
		launch_id =[]
		service_videos = {}
		epi_id=None
		try:
			epi_link =driver.find_element_by_xpath("(//div[@name='SERIES_SCROLL_ELEMENT']//div[contains(@class,'SeriesDetail_tabContent')]/div//div[contains(@class,'Tile_imageContainer')]//a)[%s]"%(e+1,))
			epi_href =epi_link.get_attribute('href')
			epi_id=epi_href.split("/")[-2].encode('ascii', 'ignore')
			launch_id.append(epi_id)
			epi_details =driver.find_element_by_xpath("(//div[@name='SERIES_SCROLL_ELEMENT']//div[contains(@class,'SeriesDetail_tabContent')]/div//div[contains(@class,'Tile_details')]//div[contains(@class,'Tile_titleWrapper')])[%s]"%(e+1,)).text
			epi_title =epi_details.split(" ",2)[2].encode('ascii', 'ignore')
			season_num =epi_details.split(" ")[0].split("S")[1].encode('ascii', 'ignore')
			epi_num =epi_details.split(" ")[1].split("E")[1].encode('ascii', 'ignore')
			epi_air_date =driver.find_element_by_xpath("(//div[@name='SERIES_SCROLL_ELEMENT']//div[contains(@class,'SeriesDetail_tabContent')]/div//div[contains(@class,'Tile_details')]//p[contains(@class,'Tile_metadata')])[%s]"%(e+1,)).text
			epi_date =epi_air_date.split(" ")[1].encode('ascii', 'ignore')
			title_img =driver.find_element_by_xpath("//img[contains(@class,'Branding_titleImage')]")
			series_title =title_img.get_attribute('alt')
			print(series_title)
			print (epi_id, epi_title, season_num, epi_num, epi_date)
			if (int(season_num) ==1 and int(epi_num) ==1) :
				print("S! E! found")
				release_year =epi_date.split("-")[-1].encode('ascii', 'ignore')
				print(release_year)
			service_videos ["fox"] =launch_id
			res=[today, "FOX Shows", series_title, release_year, epi_date, season_num, epi_num, epi_title, service_videos]
			with open(os.getcwd()+'/'+"fox_output_shows"+ '.csv', 'ab+') as mycsvfile:
				thedatawriter =csv.writer(mycsvfile)
				thedatawriter.writerow(res)
				launch_id =[]
				service_videos = {}
				epi_id=None
		except Exception as ex:
			print(ex)
			print("erorororororor")
			continue