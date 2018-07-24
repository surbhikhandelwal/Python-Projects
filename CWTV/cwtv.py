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


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
actions = ActionChains(driver)
today =datetime.date.today()
def check_exists_by_xpath(xpath):
    try:
        while (driver.find_element_by_xpath("%s"%(xpath,))) :
        	driver.find_element_by_xpath("%s"%(xpath,)).click()
        	time.sleep(5)
    except ElementNotVisibleException:
        print ("element not found")

wait = ui.WebDriverWait(driver, 10)
driver.get('http://www.cwtv.com/shows/')
print(driver.current_url)
time.sleep(8)
(driver.page_source).encode('ascii','ignore')
shows_count =driver.find_elements_by_xpath(".//*[@id='cw-main-footer-1']/div[1]/ul/li/a")
print ("Shows count :[%s]"%(len(shows_count)),)
launch_id =[]
service_videos = {}
href =[]
release_year=0
multiples =1
for s in range (len(shows_count)):
	href.append(shows_count[s].get_attribute('href'))
print (href)
for h in range (len(href)):
	try:
		print (h)
		driver.get (href[h])
		episodes=driver.find_elements_by_xpath(".//*[@id='list_1']/div//li//a")
		multiples= len(episodes)/5
		print (multiples)
		for m in range (multiples) :
			for e in range (len(episodes)):
				print (len(episodes), e+1, m+1)
				if e+1==(5*(m+1)) :
					driver.find_element_by_xpath(".//*[contains(@id,'touchcarousel_1')]/button[2]").click()
					time.sleep  (3)
				epi_href =episodes[e].get_attribute('href')
				video_id =epi_href.split("=")[-1].encode('ascii', 'ignore')
				epi_details =driver.find_element_by_xpath("(.//*[@id='list_1']/div//li//a//div[contains(@class,'videodetails')]/p[1])[%s]"%(e+1)).text.encode('ascii', 'ignore')
				epi_title =epi_details.split("Ep.")[0].split("(")[0].strip()
				epi_sea_num =epi_details.split("Ep.")[1].split(")")[0]
				print (epi_details, epi_title, epi_sea_num)
				if (len (epi_sea_num) == 3) :
					epi_num=epi_details.split("Ep.")[1].split(")")[0][-2:]
					season_num =epi_details.split("Ep.")[1].split(")")[0][0]
				elif (len (epi_sea_num) == 4) :
					epi_num=epi_details.split("Ep.")[1].split(")")[0][-2:]
					season_num =epi_details.split("Ep.")[1].split(")")[0][0:2]
				series_title =driver.find_element_by_xpath(".//*[@id='show-logo']/a").get_attribute('title').encode('ascii', 'ignore')
				launch_id.append(video_id)
				service_videos ["cwtv"] =launch_id
			
				res=[today, "CWTV Shows", series_title, season_num, epi_num, epi_title, service_videos]
				print (res)
				with open(os.getcwd()+'/'+"cwtv_shows_output"+ '.csv', 'ab+') as mycsvfile:
					thedatawriter =csv.writer(mycsvfile)
					thedatawriter.writerow(res)
					launch_id =[]
					service_videos = {}
	except Exception as e:
		print(e)
		continue