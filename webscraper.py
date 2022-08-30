import time, requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import column, false 
from webdriver_manager.chrome import ChromeDriverManager
from itertools import cycle
from selenium import webdriver
import time
from decouple import config
import pandas as pd
import sqlite3
from anticaptchaofficial.recaptchav2proxyon import *

"""
Program that uses the 2captcha API to bypass the captcha if there is one
and then scrape the information of court cases that happened on a given date
"""

class sfCourtData:

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def byPassCaptcha(self):
        
        #create a file named .env with the values inside config()
        api_key = config('API_KEY')

        pageurl = config('url')
        siteKey = config('site_key')  

        #code to automate finding the captcha key in the site

        self.driver.get(pageurl)

        form = {"method": "userrecaptcha",
                "googlekey": siteKey,
                "key": api_key,
                "pageurl": pageurl, 
                "json": 1 }

        response = requests.post('http://2captcha.com/in.php', data=form)
        request_id = response.json()['request']

        url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"

        try:
            status = 0
            while not status:
                res = requests.get(url)
                if res.json()['status']==0:
                    time.sleep(3)
                else:
                    requ = res.json()['request']
                    js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
                    self.driver.execute_script(js)
                    WebDriverWait(self.driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
                    status = 1
        except:
            print('no CAPTCHA')
    
    links = []

    def getDataAtDate(self):
        print("STATUS: now we input the desired date")
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "ui-id-3"))).click()

        dateText = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "FilingDate")))
        dateText.clear()
        dateText.send_keys('2022-07-01')

        #click search button to get court data
        time.sleep(5)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "FilingsSearchBtn"))).click()

        #gets page source and loops through the court cases on that page and prints the case number and title
        page = 0
        time.sleep(5)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all('div')

        time.sleep(5)

        list = []

        for i in table:
            word = i.text
            txt = word.split(" ")

            for w in txt:
                if w.isnumeric():            
                    list.append(w)

        pageCount = int(list[len(list)-1])//10

        d = {}

        while page <= pageCount:
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            tags = soup.find_all('td')      
            
            page += 1
            print(f'STATUS: Getting the case information from page {page}')
            time.sleep(5)
            
            i = 0
            for a in soup.find_all('a', href=True):
                if a['href'] != '#' and "http" in a['href']:
                    self.links.append(a['href'])

            for case in tags:
                caseInfo = case.text               
                if(not caseInfo.isnumeric()):
                    if(i%2 == 0):
                        number = caseInfo
                        title = " "
                    else:
                        title = caseInfo
                    i+=1
                d.update({number: title})

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "example_next"))).click()
        
        return d

    
"""
conn = sqlite3.connect('courtDB')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS case_info (CaseNumber text, CaseTitle text)')
c.execute('CREATE TABLE IF NOT EXISTS case_links (CaseLink text)')
conn.commit()
"""

sf = sfCourtData()
sf.byPassCaptcha()
data = sf.getDataAtDate()

d = data

dfData = pd.DataFrame(d.items(), columns=['CaseNumber', 'CaseTitle'])
dfLinks = pd.DataFrame(sf.links, columns=['CaseLink'])

dfData.to_csv('caseData.csv', index=False) 
dfLinks.to_csv('links.csv', index=False)

"""
dfData.to_sql('case_info', conn, if_exists='replace', index=False)
dfLinks.to_sql('case_links', conn, if_exists='replace', index=False)

c.execute('''
SELECT * FROM case_info
SELECT * FROM case_links
''')
"""
