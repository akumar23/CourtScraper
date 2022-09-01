from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium import webdriver
from pymongo import MongoClient
from bs4 import BeautifulSoup
from decouple import config
from pprint import pprint
from pathlib import Path
import urllib.request
import pandas as pd
import zipfile 
import time
import os


class sfCourt:

    def __init__(self):
        api_key = config('API_KEY')
        url = 'https://antcpt.com/anticaptcha-plugin.zip'
        filehandle, _ = urllib.request.urlretrieve(url)

        with zipfile.ZipFile(filehandle, "r") as f:
            f.extractall("plugin")

        file = Path('./plugin/js/config_ac_api_key.js')
        file.write_text(file.read_text().replace("antiCapthaPredefinedApiKey = ''", "antiCapthaPredefinedApiKey = '{}'".format(api_key)))

        zip_file = zipfile.ZipFile('./plugin.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk("./plugin"):
                for file in files:
                    path = os.path.join(root, file)
                    zip_file.write(path, arcname=path.replace("./plugin/", ""))
        zip_file.close()

        options = webdriver.ChromeOptions()
        options.add_extension('./plugin.zip')

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def byPassCaptcha(self):
        try:
            pageurl = config('url')
            self.driver.get(pageurl)
            time.sleep(50)
            print("SOLVED!")
        except:
            print("NO CAPTCHA FOUND")

    linkData = {}

    def getDataAtDate(self, date):
        print("STATUS: now we input the desired date")
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "ui-id-3"))).click()

        dateText = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "FilingDate")))
        dateText.clear()

        #get yesterday's date
        dateText.send_keys(date.strftime('%Y-%m-%d'))

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
            link = " "
            for a in soup.find_all('a', href=True):
                if a['href'] != '#' and "http" in a['href']:
                    link = a['href']

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
                if link != " ":
                    self.linkData.update({number: link})

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "example_next"))).click()
        
        return d

"""
# Code below for testing mongodb before making it a function
client = MongoClient("mongodb+srv://aryan:asdf1234@cluster0.xmaa1l2.mongodb.net/?retryWrites=true&w=majority")
pprint(client.server_info())
db = client.sfData 
"""