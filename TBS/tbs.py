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

wait = ui.WebDriverWait(driver, 10)
driver.get('http://www.tbs.com/shows')
print(driver.current_url)
time.sleep(8)
(driver.page_source).encode('ascii','ignore')
shows_count =driver.find_elements_by_xpath("//div[contains(@class,'grid-widget-container')]/div/div/div//a")
print ("Shows count :[%s]"%(len(shows_count)),)
launch_id =[]
service_videos = {}
href =[]
release_year=0
m=1
for s in range (len(shows_count)):
	href.append(shows_count[s].get_attribute('href'))
print (href)
for h in range (len(href)) :
	try:
		driver.get(href[h])
		try:
			driver.find_element_by_xpath("//button[@class='toast-close-button']").click()
		except Exception as e:
			print(e)
			pass
		episodes =driver.find_elements_by_xpath("//section[contains(@class,'carousel-widget-init')]/div[2]//div[@class='slick-track']//div[@class='content-tile-progress']")
		print (len(episodes))
		driver.execute_script("window.scrollTo(0,500)")
		for e in range (len(episodes)):
			if (e+1 >=4):
				time.sleep  (2)
				driver.find_element_by_xpath("//div[contains(@class,'carousel-widget-action')][2]").click()
				time.sleep  (2)
			video_id =driver.find_element_by_xpath("(//section[contains(@class,'carousel-widget-init')]/div[2]//div[@class='slick-track']//div[@class='content-tile-progress'])[%s]"%(e+1,))
			video_id =video_id.get_attribute('id').encode('ascii', 'ignore')
			print (video_id)
			epi_detail =driver.find_element_by_xpath("(//section[contains(@class,'carousel-widget-init')]/div[2]//div[@class='slick-track']//span[@class='content-tile-epinfo '])[%s]"%(e+1,)).text.encode('ascii', 'ignore')
			epi_num =epi_detail.split("|")[-1].split("E")[-1]
			season_num =epi_detail.split("|")[0].split("S")[-1]
			epi_title =driver.find_element_by_xpath("(//section[contains(@class,'carousel-widget-init')]/div[2]//div[@class='slick-track']//div[contains(@class,'content-tile-caption-container')]//span[@class='content-tile-eptitle'])[%s]"%(e+1,)).text.encode('ascii', 'ignore')
			series_title=driver.current_url
			if "-" in series_title:
				series_title =series_title.split("shows/")[-1].replace("-", " ").title()
			else :
				series_title =series_title.split("shows/")[-1].title()
			launch_id.append(video_id)
			service_videos ["tbs"] =launch_id
		
			res=[today, "TBS Shows", series_title, season_num, epi_num, epi_title, service_videos]
			print (res)
			with open(os.getcwd()+'/'+"tbs_shows_output"+ '.csv', 'ab+') as mycsvfile:
				thedatawriter =csv.writer(mycsvfile)
				thedatawriter.writerow(res)
				launch_id =[]
				service_videos = {}
	except Exception as e:
		print(e)
		continue

