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
driver.get('http://www.tntdrama.com/movies')
print(driver.current_url)
time.sleep(8)
(driver.page_source).encode('ascii','ignore')
shows_count =driver.find_elements_by_xpath("//div[contains(@class,'content-tile-caption-container')]//span[@class='content-tile-eptitle']//a")
print ("Movies count :[%s]"%(len(shows_count)),)
launch_id =[]
service_videos = {}
href =[]
credit =[]
release_year=0
m=1
for s in range (len(shows_count)):
	movie_title=driver.find_element_by_xpath("(//div[contains(@class,'content-tile-caption-container')]//span[@class='content-tile-eptitle']//a)[%s]"%(s+1,)).text.encode('ascii', 'ignore')
	# movie_title =title.get_attribute('title')
	print(movie_title)
	video_id =driver.find_element_by_xpath("(//div[contains(@class,'grid-content-wrapper')]//div[@class='content-tile']//div[@class='content-tile-progress'])[%s]"%(s+1,))
	movie_id=video_id.get_attribute('id').encode('ascii', 'ignore')
	launch_id.append(movie_id)
	service_videos ["tbs"] =launch_id
	print(service_videos)
	try:
		driver.get("https://www.google.com")
		driver.find_element_by_xpath("(//input)[4]").send_keys("%s movie"%(movie_title,))
		driver.find_element_by_xpath("(//input)[4]").send_keys("\n")
		time.sleep(3)
		driver.execute_script("window.scrollTo(0,500)")
		time.sleep(1)
		year =driver.find_element_by_xpath(".//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[5]/div/div[3]/div/div/span[2]").text
		if "(" in year :
			year=year.split("(")[0].strip()
		release_year =year[-4:].encode('ascii', 'ignore')
		# driver.get (series_url)
		time.sleep(5)
		print (release_year)
	except Exception as ex :
		print (ex)
		# driver.get (series_url)
		time.sleep(5)
	try:
		driver.get("https://www.google.com")
		driver.find_element_by_xpath("(//input)[4]").send_keys("%s cast"%(movie_title, ))
		driver.find_element_by_xpath("(//input)[4]").send_keys("\n")
		time.sleep(3)
		for i in range (5):
			cast =driver.find_element_by_xpath("(.//*[contains(@id,'uid_')]/div/div/div/a/div[2]/div[1])[%s]"%(i+1,)).text.encode('ascii', 'ignore')
			credit.append(cast)
		print (credit)
	except Exception as e:
		print (e)
		pass
	res=[today, "TNT Movies", movie_title, release_year, service_videos, credit]
	with open(os.getcwd()+'/'+"Tnt_output_movies"+ '.csv', 'ab+') as mycsvfile:
		thedatawriter =csv.writer(mycsvfile)
		thedatawriter.writerow(res)
		launch_id =[]
		service_videos = {}
		credit =[]
	driver.get('http://www.tntdrama.com/movies')