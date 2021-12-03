import os
import time
import random
import logging
from typing import List
from urllib.parse import urlparse, parse_qs

import typer
import joblib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

logging.basicConfig(filename="std.log",format='%(asctime)s %(message)s',filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)
rent = 0
if rent ==1 :
    X591URL="https://rent.591.com.tw/?kind=1&order=money&orderType=asc&region=17&rentprice=10000,18000&other=lift"
else:
    X591URL="https://sale.591.com.tw/?shType=list&kind=9&regionid=1&price=500$_2000$"
URL = os.environ.get('X591URL',X591URL)

def main(output_path: str = "cache/listings.jbl", max_pages: int = 5, quiet: bool = False):
    try:
        if rent==0 :
	#For sell
            region = parse_qs(urlparse(URL).query)['regionid'][0]
        else:
	#For rent
            region = parse_qs(urlparse(URL).query)['region'][0]
    except AttributeError as e:
        print("The URL must have a 'region' query argument!")
        raise e
    options = webdriver.ChromeOptions()
    if quiet:
        options.add_argument('headless')
    browser = webdriver.Chrome(options=options, executable_path='./chromedriver')
    browser.get(URL)
    #browser.find_element_by_xpath("//div[@class=\"house-switch-item pull-left\"]//div[@class=\"undis tips-popbox vrhouse-popbox\"]//div[@class=\"tips-popbox-shadow\"]").click()
    #For sell 
    if rent ==0 : 	
        WebDriverWait(browser,1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[4]/div[2]/div[1]/div[3]/div/div[2]'))).click()    

    try:
        browser.find_element_by_css_selector(
            f"dd[data-id=\"{region}\"]").click()
    except NoSuchElementException:
        pass
    time.sleep(2)
    listings: List[str] = []
    for i in range(max_pages):

        soup = BeautifulSoup(browser.page_source, "lxml")
        #a = soup.find_all("ul")
        logger.error(soup)

	#For rent
        if rent == 1:
           for item in soup.find_all("ul", attrs={"class": "item active"}):
                #print(f"--Terence---item {item}")
                logger.error(item)
                link = item.find("a")
                logger.error("Terence")
                #logger.error(link.attrs["href"].split("-")[-1].split(".")[0])
                listings.append(link.attrs["href"].split("-")[-1].split(".")[0])
                #listings.append(link.attrs["href"])	
                #logger.error(listings.append(link.attrs["href"].split("-")[-1].split(".")[0]))	
        else:
            for item in soup.find_all("ul", attrs={"class": "listinfo"}):
                logger.error(item)
                link = item.find("a")
                logger.error("Terence")
                listings.append(link.attrs["href"].split("-")[-1].split(".")[0])
        browser.find_element_by_class_name('pageNext').click()
        time.sleep(random.random() * 5)
        try:
            browser.find_element_by_css_selector('a.last')
            break
        except NoSuchElementException:
            pass
    print(f"-------------------Terence-------------------")
    print(f'dylan : {listings}')
    print(len(set(listings)))
    joblib.dump(listings, output_path)
    print(f"Done! Collected {len(listings)} entries.")


if __name__ == "__main__":
    typer.run(main)
