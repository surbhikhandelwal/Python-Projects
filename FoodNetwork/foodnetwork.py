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
actions = ActionChains(driver)
today =datetime.date.today()
driver.implicitly_wait(10)

def check_exists_by_xpath(xpath):
    try:
    	driver.find_element_by_xpath("%s"%(xpath,)).click()
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

def elements_exists(xpath):
	try:
		elements  =driver.find_elements_by_xpath("%s"%(xpath,))
		time.sleep(2)
		return elements
	except ElementNotVisibleException:	
		print ("element not found for text")
		

driver.get('http://www.foodnetwork.com/')
show_href =[]
epi_num=0
season_num =0
launch_id =[]
service_videos = {}
num_seasons =1
try:
	driver.find_element_by_xpath("(//a[contains(@class,'International')])[2]").click()
except Exception as ex :
		print (ex)
		pass

driver.find_element_by_xpath(".//*[contains(@class,'a-Icon--menu')]").click()
driver.execute_script("window.scrollTo(0, 200)")
driver.find_element_by_xpath(".//*[@id='mod-mobile-nav-1']/div[2]/ul/li[5]/a").click()
shows =driver.find_elements_by_xpath("//div[@class='container-site']//div[1]//section[contains(@class,'o-Capsule')]//ul/li/a")

print(len(shows))
for s in range (len(shows)):
	show_href.append(shows[s].get_attribute('href'))
print(show_href)
for h in range (len(shows)):
	try:
		print (show_href[h])
		driver.get(show_href[h])
		driver.find_element_by_xpath(".//*[@id='mod-sub-navigation-1']/li[2]/div").click()
		series_title =driver.find_element_by_xpath("//section[@class='o-ListEpisode']//h2/span").text.encode('ascii', 'ignore').split("EPISODES")[0]
		print (series_title)
		series_url =driver.current_url
		check_exists_by_xpath("//section[@class='m-ResultFilter']/div")
		seasons =elements_exists("//section[@class='m-ResultFilter']/div//ul/li")
		try:
			num_seasons =(len(seasons))
		except Exception as e:
			print (e)
			pass
		for se in range (num_seasons): 
			check_exists_by_xpath("//section[@class='m-ResultFilter']/div//ul/li[%s]"%(len(seasons)-se,))
			episodes =driver.find_elements_by_xpath("//section[@class='o-ListEpisode']//span[contains(@class,'m-EpisodeCard')]")
			print(len(episodes))
			
			for e in range (len(episodes)):
				episode_details =driver.find_element_by_xpath("(//section[@class='o-ListEpisode']//span[contains(@class,'m-EpisodeCard')])[%s]"%(e+1,)).text.encode('ascii', 'ignore')
				season_num =episode_details.split(",")[0]
				if "Season" not in season_num:
					season_num ="Special"
				else :
					season_num=season_num.split(" ")[1]
				epi_num =episode_details.split(",")[1].split(" ")[-1]
				epi_title =driver.find_element_by_xpath("(//section[@class='o-ListEpisode']//h4)[%s]"%(e+1,)).text.encode('ascii', 'ignore')
				epi_link=driver.find_element_by_xpath("(//section[@class='o-ListEpisode']//h4//a)[%s]"%(e+1,)).get_attribute('href')
				print  (season_num,epi_num, epi_title, epi_link)
				current_url =driver.current_url
				try:
					driver.get(epi_link)
					driver.find_element_by_xpath(".//*[@id='mod-video-launcher-1']/header/div/a").click()
					video_text =driver.find_elements_by_xpath(".//div[@id='video-gallery']//div[contains(@class,'MediaBlock__m-TextWrap')]//span[contains(@class,'HeadlineText')]")
					print ("video length: [%s]"%(len(video_text)))
					multiples= len(video_text)/3
					for v in range (len(video_text)):
						if v>3 :
							for m in range (multiples):
								if v==(4*(m+1)) :
									print (v)
									driver.find_element_by_xpath("(.//*[contains(@id,'mod-carousel')]//div[contains(@class,'m-CustomPagination')]//a)[2]").click()
									print(video_text[v].text.encode('ascii', 'ignore'))
									if (epi_title.lower() == video_text[v].text.encode('ascii', 'ignore').lower()):
										print("title matched")
										src_id =driver.find_element_by_xpath("(.//*[contains(@id,'mod-carousel')]//div[contains(@class,'MediaBlock__m-MediaWrap')]//a/img)[%s]"%(v+1,)).get_attribute('src')
										# src_id =src_id.get_attribute('src')
										video_id =src_id.split(".jpg")[0].split("/")[-1].encode('ascii', 'ignore')
										print(video_id)
										launch_id.append(video_id)
										service_videos ["foodnetwork"] =launch_id
									
										res=[today, "Freeform Shows", series_title, season_num, epi_num, epi_title, service_videos]
										print (res)
										with open(os.getcwd()+'/'+"foodnetwork_shows_output"+ '.csv', 'ab+') as mycsvfile:
											thedatawriter =csv.writer(mycsvfile)
											thedatawriter.writerow(res)
											launch_id =[]
											service_videos = {}
						print(video_text[v].text.encode('ascii', 'ignore'))
						if (epi_title.lower() == video_text[v].text.encode('ascii', 'ignore').lower()):
							print("title matched")
							src_id =driver.find_element_by_xpath("(.//*[contains(@id,'mod-carousel')]//div[contains(@class,'MediaBlock__m-MediaWrap')]//a/img)[%s]"%(v+1,)).get_attribute('src')
							# src_id =src_id.get_attribute('src')
							video_id =src_id.split(".jpg")[0].split("/")[-1].encode('ascii', 'ignore')
							print(video_id)
							launch_id.append(video_id)
							service_videos ["foodnetwork"] =launch_id
						
							res=[today, "Freeform Shows", series_title, season_num, epi_num, epi_title, service_videos]
							print (res)
							with open(os.getcwd()+'/'+"foodnetwork_shows_output"+ '.csv', 'ab+') as mycsvfile:
								thedatawriter =csv.writer(mycsvfile)
								thedatawriter.writerow(res)
								launch_id =[]
								service_videos = {}
					
							# if epi_title.lower() in video_text[v].text.encode('ascii', 'ignore').lower():
							# 	print("title matched")
							# 	src_id =driver.find_element_by_xpath("(.//*[contains(@id,'mod-carousel')]//div[contains(@class,'MediaBlock__m-MediaWrap')]//a/img)[%s]"%(v+1,)).get_attribute('src')
							# 	# src_id =src_id.get_attribute('src')
							# 	video_id =src_id.split(".jpg")[0].split("/")[-1].encode('ascii', 'ignore')
							# 	print(video_id)
							# 	launch_id.append(video_id)
							# 	service_videos ["foodnetwork"] =launch_id
							
							# 	res=[today, "Freeform Shows", series_title, season_num, epi_num, epi_title, service_videos]
							# 	print (res)
							# 	with open(os.getcwd()+'/'+"foodnetwork_shows_output"+ '.csv', 'ab+') as mycsvfile:
							# 		thedatawriter =csv.writer(mycsvfile)
							# 		thedatawriter.writerow(res)
							# 		launch_id =[]
							# 		service_videos = {}
				except Exception as e:
					print (e)
					pass
				driver.get(current_url)		
			driver.get(series_url)
			check_exists_by_xpath("//section[@class='m-ResultFilter']/div")
	except Exception as e:
		print (e)
		continue
	
