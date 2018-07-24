from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
import csv
import os


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

def text_from_xpath(xpath):
	text =None
	try:
		text =driver.find_element_by_xpath("%s"%(xpath,)).text.encode('ascii', 'ignore')
		time.sleep(2)
		return text
	except ElementNotVisibleException:	
		print ("element not found for text")

def elements_exists(xpath):
	try:
		elements  =driver.find_elements_by_xpath("%s"%(xpath,))
		time.sleep(2)
		return elements
	except ElementNotVisibleException:	
		print ("element not found for text")

wait = ui.WebDriverWait(driver, 10)
driver.get('https://itunes.apple.com/us')
print(driver.current_url)
time.sleep(5)
launch_id =[]
service_videos = {}
href =[]
credit =[]

driver.find_element_by_xpath("(//div[@id='media-type-nav']/ul/li/a)[3]").click()
genres =driver.find_elements_by_xpath("//div[@id='genre-nav']/div/ul/li/a")
print("No. of Genres: %s"%(len(genres),))
for g in range (len(genres)):
	driver.find_element_by_xpath("(//div[@id='genre-nav']/div/ul/li/a)[%s]"%(g+1,)).click()
	movie_links=driver.find_elements_by_xpath("//div[@id='selectedcontent']/div[contains(@class,'column')]/ul/li/a")
	for m in range (len(movie_links)):
		href.append(movie_links[m].get_attribute('href'))
print("Num. of Series: %s"%(len(href)))
for s in range (len(href)):
	try:
		release_year=0
		driver.get(href[s])
		series_detail =text_from_xpath("//div[@id='content']//div[@id='title']//h1/span[1]")
		series_title=series_detail.split(", Season")[0]
		
		if "(" in series_title :
			series_title =series_detail.split("(")[0].strip()
		print(series_title)
		release_year =text_from_xpath("//ul[@class='list']//li[@class='release-date']/span[2]")[-4:]
		print(release_year)
		season_num=series_detail.split(", Season")[-1].strip()
		print(season_num)
		episodes =driver.find_elements_by_xpath("(//table[contains(@class, 'tracklist-table')]//tbody//td[contains(@class,'view-in-itunes')]/a)")
		for e in range (len(episodes)):
			epi_num =driver.find_element_by_xpath("(.//*[@id='content']/div/div[2]/div[2]/div/table/tbody/tr/td[1]/span/span)[%s]"%(e+1,)).text.encode('ascii', 'ignore')
			print (epi_num)
			epi_links=driver.find_element_by_xpath("(//table[contains(@class, 'tracklist-table')]//tbody//td[contains(@class,'view-in-itunes')]/a)[%s]"%(e+1,))
			video_id =epi_links.get_attribute('onclick').split("i=")[-1].encode('ascii', 'ignore')
			print(video_id)
			episode_title =driver.find_element_by_xpath("(//table[contains(@class, 'tracklist-table')]//tbody/tr)[%s]"%(e+1,)).get_attribute('preview-title').encode('ascii', 'ignore')
			try:
				if "Season" in episode_title:
					if "Episode" in episode_title:
						if ":" in episode_title:
							episode_title =episode_title.split(":")[1].strip()
						elif "," in episode_title:
							episode_title =episode_title.split(",")[2].strip()

			except Exception as e:
				print(e)
			try:
				if "(" in episode_title:
					episode_title =episode_title.split("(")[0].strip()
			except Exception as e:
				print (e)
			launch_id.append(video_id)
			service_videos ["itunes"] =launch_id
		
			res=[today, "iTunes Shows", series_title, release_year,season_num, epi_num, episode_title, service_videos]
			print (res)
			with open(os.getcwd()+'/'+"itunes_shows_output"+ str(today)+'.csv', 'ab+') as mycsvfile:
				thedatawriter =csv.writer(mycsvfile)
				thedatawriter.writerow(res)
				launch_id =[]
				service_videos = {}
	except Exception as e:
		print (e)
		continue

