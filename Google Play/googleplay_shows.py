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
series_href =[]
service_videos ={}
launch_id =[]
release_year =0
driver.get ("https://play.google.com/store/movies/category/TV?hl=en")
time.sleep(7)
# driver.execute_script("window.scrollTo(0, 600)")
category =driver.find_elements_by_xpath("//div[contains(@class,'outer-container')]//div[contains(@class,'id-cluster-container')]//a[contains(@class,'see-more play-button')]")
current_url =driver.current_url
print("Num of categories : %s"%(len(category)))
for c in range (len(category)):
	driver.find_element_by_xpath("(//div[contains(@class,'outer-container')]//div[contains(@class,'id-cluster-container')]//a[contains(@class,'see-more play-button')])[%s]"%(c+1,)).click()
	time.sleep(7)
	print ("Category %s checking"%(c+1,))
	driver.execute_script("window.scrollTo(0, 5000)")
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, 0)")
	series_links =driver.find_elements_by_xpath("//div[contains(@class,'id-card-list')]/div/div/a")
	series_href =[]
	for s in range(len(series_links)):
		series_href.append(series_links[s].get_attribute('href'))
	print("Number of series: %s"%(len(series_links)))
	for l in range (len(series_href)):
		try:
			driver.get(series_href[l])
			time.sleep(5)
			driver.execute_script("window.scrollTo(0, 400)")
			driver.find_element_by_xpath(".//*[@id='season-selector']").click()
			number_of_season = driver.find_elements_by_xpath(".//*[@class='season-selector-dropdown']/div")
			for n in range (len(number_of_season)):
				driver.find_element_by_xpath("(.//*[@class='season-selector-dropdown']/div)[%s]"%(len(number_of_season)-n,)).click()
				season_num =driver.find_element_by_xpath(".//*[@id='season-selector']/span").text.encode('ascii', 'ignore')
				season_num =season_num.title()
				sea_num =season_num.split(" ")[1]
				num_of_epi =driver.find_elements_by_xpath("//div[@data-season-title='%s']//div[contains(@class,'id-card-list card-list')]/div"%(season_num,))
				print ("Num of episodes %s in season %s"%(num_of_epi,n+1,))
				for e in range (len(num_of_epi)):
					series_title =driver.find_element_by_xpath("//h1[@class='document-title']").text.encode('ascii', 'ignore')
					print(series_title)
					epi_link =driver.find_element_by_xpath("(//div[@data-season-title='%s']//div[contains(@class,'id-card-list card-list')]//div[@class='details']/a[1])[%s]"%(season_num,e+1,))
					epi_id =(epi_link.get_attribute('href')).split("tvepisode-")[-1].encode('ascii', 'ignore')
					print(epi_id)
					launch_id.append(epi_id)
					try:
						epi_detail =driver.find_element_by_xpath("(//div[@data-season-title='%s']//div[contains(@class,'id-card-list card-list')]//div[@class='details']/a/span/span[1])[%s]"%(season_num,e+1,)).text.encode('ascii', 'ignore')
						print(epi_detail)
						epi_title =epi_detail.split(".")[-1].strip()
						episode_num =epi_detail.split(".")[0].strip()
						print(epi_title, sea_num, episode_num)
						if (int(sea_num) ==1 and int(episode_num)==1):
							release_date =driver.find_element_by_xpath("//div[@data-season-title='%s']//div[contains(@class,'id-card-list card-list')]//div[@class='details']//span[contains(@class,'releasedate')]"%(season_num,)).text.encode('ascii', 'ignore')
							release_year =release_date[-4:]
							print(release_year)
					except Exception as ex:
						print(ex)
					service_videos ["googleplay"] =launch_id
					res=[today, "GooglePlay Shows", series_title, release_year, sea_num, episode_num, epi_title, service_videos]
					print(res)
					with open(os.getcwd()+'/'+"Google_output_shows_16Mar"+ '.csv', 'ab+') as mycsvfile:
						thedatawriter =csv.writer(mycsvfile)
						thedatawriter.writerow(res)
						launch_id =[]
						service_videos = {}
						epi_id=None
				
				driver.find_element_by_xpath(".//*[@id='season-selector']").click()
		except Exception as ex:
			print(ex)
			continue
	driver.get(current_url)


