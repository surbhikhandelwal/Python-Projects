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
import unicodedata
import re
import hashlib
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from ConfigParser import ConfigParser
import logging
from logging.config import fileConfig


options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=options)
actions = ActionChains(driver)
today =datetime.date.today()
# fileConfig("logging.ini")
# logger = logging.getLogger()
logging.basicConfig(filename='logger.log', level =logging.DEBUG)
if __name__=="__main__":
	cfg =ConfigParser()
	cfg.read('itunes_config.ini')
	logging.debug(cfg.get('ConfigMovies', 'url'))
	def check_exists_by_xpath(xpath):
	    try:
	        while (driver.find_element_by_xpath("%s"%(xpath,))) :
	        	driver.find_element_by_xpath("%s"%(xpath,)).click()
	        	time.sleep(5)
	    except Exception as e:
			logging.debug (e)

	def text_from_xpath(xpath):
		text =None
		try:
			text =driver.find_element_by_xpath("%s"%(xpath,)).text.encode('ascii', 'ignore')
			time.sleep(2)
			return text
		except Exception as e:
			logging.debug (e)	

	def elements_exists(xpath):
		try:
			elements  =driver.find_elements_by_xpath("%s"%(xpath,))
			time.sleep(2)
			return elements
		except Exception as e:
			logging.debug (e)

	wait = ui.WebDriverWait(driver, 10)

	driver.get(cfg.get('ConfigMovies', 'url'))
	logging.debug(driver.current_url)
	time.sleep(8)
	(driver.page_source).encode('ascii','ignore')
	launch_id =[]
	service_videos = {}
	href =[]
	credit =[]

	driver.find_element_by_xpath(cfg.get('ConfigMovies', 'media')).click()
	genres =driver.find_elements_by_xpath(cfg.get('ConfigMovies', 'genre'))
	logging.debug("No. of Genres: %s"%(len(genres),))
	for g in range (len(genres)):
		driver.find_element_by_xpath("(//div[@id='genre-nav']/div/ul/li/a)[%s]"%(g+1,)).click()
		movie_links=driver.find_elements_by_xpath(cfg.get('ConfigMovies', 'movie_links'))
		for m in range (len(movie_links)):
			href.append(movie_links[m].get_attribute('href'))
			# print(href)

	logging.debug("Num. of movies: %s"%(len(href)))
	for h in range (len(href)):
		release_year=0
		driver.get(href[h])
		movie_title =text_from_xpath(cfg.get('ConfigMovies', 'movie_title'))
		logging.debug(movie_title)
		actors =text_from_xpath(cfg.get('ConfigMovies', 'actors'))
		logging.debug(actors)
		credit.append(actors)
		producers= text_from_xpath(cfg.get('ConfigMovies', 'producers'))
		logging.debug(producers)
		credit.append(producers)
		directors= text_from_xpath(cfg.get('ConfigMovies', 'directors'))
		logging.debug(directors)
		credit.append(directors)
		release_year= text_from_xpath(cfg.get('ConfigMovies', 'release_year'))
		logging.debug(release_year)
		current_url =driver.current_url
		movie_id =current_url.split("id")[-1].encode('ascii', 'ignore')
		logging.debug(movie_id)
		launch_id.append(movie_id)
		service_videos ["itunes"] =launch_id
		logging.debug(service_videos)
		res=[today, "Itunes Movies", movie_title, release_year, service_videos, credit]
		with open(os.getcwd()+'/'+"iTunes_output_movies"+ str(today)+'.csv', 'ab+') as mycsvfile:
			thedatawriter =csv.writer(mycsvfile)
			thedatawriter.writerow(res)
			launch_id =[]
			service_videos = {}
			credit =[]
