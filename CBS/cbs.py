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
driver.get('https://www.cbs.com/shows/')
print(driver.current_url)
time.sleep(8)
(driver.page_source).encode('ascii','ignore')
shows_count =driver.find_elements_by_xpath(".//*[@id='id-shows-list']/li")
print ("Shows count :[%s]"%(len(shows_count)),)
launch_id =[]
service_videos = {}
release_year=0 
for s  in range (len(shows_count)):
	try:
		print ("count number: [%s]"%(s+14,))
		show_link =driver.find_element_by_xpath(".//*[@id='id-shows-list']/li[%s]/div//a"%(s+14,))
		show_link_href =show_link.get_attribute('href')
		driver.get (show_link_href)
		time.sleep(8)
		series_title =driver.find_element_by_xpath(".//*[@id='showName']/div").text.encode('ascii', 'ignore')

		print (series_title)
		series_url =driver.current_url
		try:
			driver.get("https://www.google.com")
			driver.find_element_by_xpath("(//input)[4]").send_keys("%s series"%(series_title,))
			driver.find_element_by_xpath("(//input)[4]").send_keys("\n")
			time.sleep(3)
			year =driver.find_element_by_xpath(".//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[4]/div/div[3]/div/div/span[2]").text
			release_year =year[-4:].encode('ascii', 'ignore')
			driver.get (series_url)
			time.sleep(5)
			print (release_year)
		except Exception as ex :
			print (ex)
			driver.get (series_url)
			time.sleep(5)
	except Exception as ex :
		print (ex)
		driver.get('https://www.cbs.com/shows/')
		time.sleep(8)
		continue
	driver.find_element_by_xpath(".//*[@id='marqueeShowHeader']/section/div/ul/li[2]/a").send_keys("\n")
	time.sleep(5)
	driver.execute_script("window.scrollTo(0, 600)")
	time.sleep(3)
	
	seasons =driver.find_elements_by_xpath("//div[@class='carousel-filter']//ul/li")
	print ("seasons")
	if (len(seasons)==0):
		print("dropdown not found")
		episodes =driver.find_elements_by_xpath(".//div[contains(@id,'id-carousel')][1]//div[@class='slick-track']/li/a")
		print(episodes)
		print (len(episodes))
		episode_links =[]
		for epi in range (len(episodes)):
			epi_links =driver.find_element_by_xpath("(.//div[contains(@id,'id-carousel')][1]//div[@class='slick-track']/li/a)[%s]"%(epi+1,))
			epi_links =epi_links.get_attribute('href').encode('ascii', 'ignore')
			print(episode_links)
			episode_links.append(epi_links)
		print(episode_links)
		for k in range (len(episode_links)):
			try:
				driver.get (episode_links[k])
				time.sleep(8)
				driver.execute_script("window.scrollTo(0, 300)")
				epi_id =episode_links[k].split("/")[-3]
				launch_id.append(epi_id)
				print (launch_id)
				video_title =driver.find_element_by_xpath(".//div[@class='title']").text
				season_num =video_title.split("S")[-1].split("(")[0].split("E")[0].strip().encode('ascii', 'ignore')
				epi_num =video_title.split("S")[-1].split("(")[0].split("E")[1].strip().encode('ascii', 'ignore')
				epi_title =video_title.split("S")[-2].encode('ascii', 'ignore')
				epi_title =epi_title.split("%s - "%(series_title,))[-1]
				try:
					if (k==0) and (epi==0):
						driver.get ("https://www.imdb.com/")
						time.sleep(3)
						driver.find_element_by_xpath(".//div[@id='nb_search']//input[@id='navbar-query']").send_keys("%s %s"%(series_title, epi_title,))
						driver.find_element_by_xpath(".//div[@id='nb_search']//input[@id='navbar-query']").send_keys("\n")
						release_year =driver.find_element_by_xpath("(//div[@class='article']//table[@class='findList']//td[2]/small[2])[1]").text.split("(")[1].split(")")[0].encode('ascii', 'ignore')
						print (release_year)
						driver.get (episode_links[k])
						time.sleep(5)
				except Exception as ex :
					print (ex)
					driver.get (episode_links[k])
					time.sleep(5)
					pass
				# try:	
				# 	if (k==0):
				# 		driver.get("https://www.google.com")
				# 		driver.find_element_by_xpath("(//input)[4]").send_keys("%s series"%(series_title,))
				# 		driver.find_element_by_xpath("(//input)[4]").send_keys("\n")
				# 		time.sleep(3)
				# 		year =driver.find_element_by_xpath(".//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[4]/div/div[3]/div/div/span[2]").text.encode('ascii', 'ignore')
				# 		release_year =year[-4:]
				# 		driver.get (episode_links[k])
				# 		time.sleep(5)
				# 		print (release_year)
				# except Exception as e :
				# 	print (e)
				# 	driver.get (episode_links[k])
				# 	time.sleep(5)
				# 	pass
				# if (season_num ==1) and (epi_num==1) :
				# 	driver.find_element_by_xpath(".//*[@id='id-video-info']").click()
				# 	release_year =driver.find_element_by_xpath(".//*[@id='info-tip']//div[@class='airdate']").text.split("/")[-1]
				print (service_videos, season_num, epi_num,epi_title,release_year)
				service_videos ["cbs"] =launch_id
				res=[today, "CBS Shows", series_title, release_year, season_num, epi_num, epi_title, service_videos]
				with open(os.getcwd()+'/'+"cbs_output"+ '.csv', 'ab+') as mycsvfile:
					thedatawriter =csv.writer(mycsvfile)
					thedatawriter.writerow(res)
					launch_id =[]
					service_videos = {}
			except Exception as ex :
				print (ex)
				continue
		driver.get('https://www.cbs.com/shows/')
		time.sleep(8)
		continue
	print (len(seasons))
	time.sleep (10)
	for e in range (len(seasons)):	
		try:
			episodes =driver.find_elements_by_xpath(".//div[contains(@id,'id-carousel')][1]//div[@class='slick-track']/li/a")
			print (len(episodes))
			for epi in range (len(episodes)):
				season_num =driver.find_element_by_xpath(".//div[contains(@id,'id-carousel')][1]/div/div[1]/div/span").text.split("Season")[1]
				time.sleep(1)
				# print (epi+1)
				if (epi+1 ==len(episodes)) :
					break
				elif ((epi+1) % 3 ==0) and (not((epi+1)== len(episodes))):
					driver.find_element_by_xpath(".//div[contains(@id,'id-carousel')][1]/div/a[2]").click()
				epi_detail=driver.find_element_by_xpath("(//div[@class='slick-track'][1]//li/a)[%s]"%(epi+1,))
				epi_title =epi_detail.get_attribute('title').encode('ascii', 'ignore')
				epi_title =epi_title.split("%s - "%(series_title,))[-1]
				ep_num_detail =driver.find_element_by_xpath("(//div[@class='slick-track'][1]//li/a//span[@class='ep-title'])[%s]"%(epi+1,)).text
				epi_num =ep_num_detail.split("|")[0].split("Ep")[1]
				epi_num =epi_num.encode('ascii', 'ignore')
				curr_url =driver.current_url

					
				# try:
				# 	if(release_year ==0) and(epi==0):
				# 		driver.get("https://www.google.com")
				# 		driver.find_element_by_xpath("(//input)[4]").send_keys("%s series"%(series_title,))
				# 		driver.find_element_by_xpath("(//input)[4]").send_keys("\n")
				# 		time.sleep(3)
				# 		year =driver.find_element_by_xpath(".//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[4]/div/div[3]/div/div/span[2]").text
				# 		release_year =year[-4:]
				# 		driver.get (curr_url)
				# 		time.sleep(5)
				# 		print (release_year)
				# except Exception as e :
				# 	print (e)
				# 	driver.get (curr_url)
				# 	time.sleep(5)
					
				epi_href=epi_detail.get_attribute('href').encode('ascii', 'ignore')
				epi_id =epi_href.split("/")[-3]
				launch_id.append(epi_id)
				service_videos ["cbs"] =launch_id
				try:
					if (epi==0) and (e==0):
						driver.get ("https://www.imdb.com/")
						time.sleep(3)
						driver.find_element_by_xpath(".//div[@id='nb_search']//input[@id='navbar-query']").send_keys("%s %s"%(series_title, epi_title,))
						driver.find_element_by_xpath(".//div[@id='nb_search']//input[@id='navbar-query']").send_keys("\n")
						release_year =driver.find_element_by_xpath("(//div[@class='article']//table[@class='findList']//td[2]/small[2])[1]").text.split("(")[1].split(")")[0].encode('ascii', 'ignore')
						driver.get (curr_url)
						time.sleep(6)
						driver.execute_script("window.scrollTo(0, 600)")
						print (release_year)
						time.sleep(3)
				except Exception as ex :
					print (ex)
					driver.get (curr_url)
					time.sleep(6)
					driver.execute_script("window.scrollTo(0, 600)")
					time.sleep(3)
				print(epi_title, epi_href, epi_num, service_videos, release_year)
				res =[today, "CBS Shows", series_title, release_year, season_num, epi_num, epi_title, service_videos]
				with open(os.getcwd()+'/'+"cbs_output"+ '.csv', 'ab+') as mycsvfile:
					thedatawriter =csv.writer(mycsvfile)
					thedatawriter.writerow(res)
					launch_id =[]
					service_videos = {}
			print("outside episode loop")
			driver.find_element_by_xpath("//div[@class='carousel-filter']").click()
			time.sleep(2)
			print ("value of s [%s]"%(e,))
			driver.find_element_by_xpath(".//div[contains(@id,'id-carousel')][1]/div/div[1]/ul/li[%s]"%(e+2,)).click()
			print ("selecting next season")
			time.sleep(3)
		except Exception as ex :
			print (ex)
			continue
	driver.get('https://www.cbs.com/shows/')
	time.sleep(8)


