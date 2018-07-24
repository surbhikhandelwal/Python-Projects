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


    

driver.get('https://www.nbc.com/shows/all')
show_href =[]
epi_nm=0
season_num =0
release_year = 0
launch_id =[]
service_videos = {}
shows =driver.find_elements_by_xpath("//div[contains(@class,'all tabs')]//section[@class='show-list']//a")
for s in range (len(shows)):
	show_href.append(shows[s].get_attribute('href'))
print(len(show_href))
print(show_href)
for h in range (len(show_href)):
	release_year = 0
	print ("show number: %s"%(h,))
	try:
		driver.get (show_href[h]+"/episodes")
		time.sleep(2)
		series_title=driver.find_element_by_xpath("//header[@class='responsive-app__header']//h1[contains(@class,'show-header__title')]").text.encode('ascii', 'ignore')
		try:
			driver.get("https://www.google.com")
			driver.find_element_by_xpath("(//input)[3]").send_keys("%s Series"%(series_title,))
			driver.find_element_by_xpath("(//input)[3]").send_keys("\n")
			time.sleep(3)
			driver.execute_script("window.scrollTo(0,500)")
			time.sleep(1)
			year =driver.find_element_by_xpath(".//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[4]/div/div[6]/div/div/span[2]").text
			release_year =year[-4:].encode('ascii', 'ignore')
			time.sleep(5)
			print (release_year)
		except Exception as ex :
			print (ex)
		driver.get (show_href[h]+"/episodes")
		number_of_epi =text_from_xpath("//div[@class='section-heading']/h1")
		print(number_of_epi)
		if '0' not in str(number_of_epi):
			total_epi =int(number_of_epi.split("(")[1].split(")")[0])
			print ("Episodes are there")
			
			try:
				driver.find_element_by_xpath("//div[@class='filter-select__inner']").click()
				dropdown =True
			except NoSuchElementException:	
				print ("element not found for text")
				dropdown =False
			if(dropdown == True):
				print (dropdown)
				print  ("dropdown value")
				seasons =driver.find_elements_by_xpath("//div[@class='filter-select__inner']/ul/li")
				print(len(seasons))
				for se in range (len(seasons)):
					time.sleep(5)
					current_season =driver.find_element_by_xpath("//div[@class='filter-select__inner']/ul/li[1]").text
					# while (driver.find_element_by_xpath("//div[contains(@class,'load-button')]")):
					# 	driver.execute_script("window.scrollTo(0,2000)")
					# 	more_episodes = driver.find_element_by_xpath("//div[contains(@class,'load-button')]").click()
					epi_in_seas =driver.find_elements_by_xpath("//div[contains(@class,'episodes-page__episodes-module')]/div")
					print("Episodes in Season %s : %s"%(current_season, (len(epi_in_seas)-1),))
					try:
						while (int(len(epi_in_seas)-1) <= (total_epi)):
							
							print(len(epi_in_seas))
							print(total_epi)
							print ("its less")
							time.sleep(3)
							driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div)[%s]"%(len(epi_in_seas),)).click()
							time.sleep(3)
							epi_in_seas =driver.find_elements_by_xpath("//div[contains(@class,'episodes-page__episodes-module')]/div")							
					except Exception as ex:
						print(ex)
					for epi in range (len(epi_in_seas)-1):
						epi_link =driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//h2[@class='card__title']/a)[%s]"%(epi+1,))
						epi_href =epi_link.get_attribute('href')
						epi_id =epi_href.split("/")[-1].encode('ascii', 'ignore')
						launch_id.append(epi_id)
						epi_detail =driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//h2[@class='card__title']/a/span[1])[%s]"%(epi+1,)).text
						try: 
							season_num =epi_detail.split(" ")[0].split("S")[1].encode('ascii', 'ignore')
							print(season_num)
							epi_nm =epi_detail.split(" ")[1].split("E")[1].encode('ascii', 'ignore')
							print(epi_nm)
						except Exception as ex:
							print(ex)
						epi_date =driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//h2[@class='card__title']/a/span[2])[%s]"%(epi+1,)).text.encode('ascii', 'ignore')
						epi_title=driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//div[@class='card__description']/span)[%s]"%(epi+1,)).text.encode('ascii', 'ignore')
						service_videos ["nbc"] =launch_id
						res=[today, "NBC Shows", series_title, release_year, season_num, epi_nm, epi_title, service_videos]
						with open(os.getcwd()+'/'+"nbc_output"+ '.csv', 'ab+') as mycsvfile:
							thedatawriter =csv.writer(mycsvfile)
							thedatawriter.writerow(res)
							launch_id =[]
							service_videos = {}
					driver.execute_script("window.scrollTo(0, 0)")
					driver.find_element_by_xpath("//div[@class='filter-select__inner']").click()
					driver.find_element_by_xpath("//div[@class='filter-select__inner']/ul/li[%s]"%(se+3,)).click()
				
			else :
				print("dropdown not present")
				epi_in_seas =driver.find_elements_by_xpath("//div[contains(@class,'episodes-page__episodes-module')]/div")
				try:
					while (int(len(epi_in_seas)-1) <= (total_epi)):
						
						print(len(epi_in_seas))
						print(total_epi)
						print ("its less")
						driver.execute_script("window.scrollTo(0, 2200)")
						time.sleep(3)
						driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div)[%s]"%(len(epi_in_seas),)).click()
						time.sleep(3)
						epi_in_seas =driver.find_elements_by_xpath("//div[contains(@class,'episodes-page__episodes-module')]/div")
						
				except Exception as ex:
					print(ex)
					print("moving forward")
				for epi in range (len(epi_in_seas)-1):
					epi_link =driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//h2[@class='card__title']/a)[%s]"%(epi+1,))
					epi_href =epi_link.get_attribute('href')
					epi_id =epi_href.split("/")[-1].encode('ascii', 'ignore')
					print(epi_id)
					launch_id.append(epi_id)
					epi_detail =driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//h2[@class='card__title']/a/span[1])[%s]"%(epi+1,)).text
					print(epi_detail)
					epi_date =driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//h2[@class='card__title']/a/span[2])[%s]"%(epi+1,)).text.encode('ascii', 'ignore')
					epi_title=driver.find_element_by_xpath("(//div[contains(@class,'episodes-page__episodes-module')]/div//div[@class='card__description']/span)[%s]"%(epi+1,)).text.encode('ascii', 'ignore')
					
					try: 
						season_num =epi_detail.split(" ")[0].split("S")[1].encode('ascii', 'ignore')
						print(season_num)
						epi_nm =epi_detail.split(" ")[1].split("E")[1].encode('ascii', 'ignore')
						print(epi_nm)
					except Exception as ex:
						print(ex)
					service_videos ["nbc"] =launch_id
					res=[today, "NBC Shows", series_title, release_year, season_num, epi_nm, epi_title, service_videos]
					with open(os.getcwd()+'/'+"nbc_output"+ '.csv', 'ab+') as mycsvfile:
						thedatawriter =csv.writer(mycsvfile)
						thedatawriter.writerow(res)
						launch_id =[]
						service_videos = {}

	except Exception as ex :
		print (ex)


