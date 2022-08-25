from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from decouple import config
from pathlib import Path
import urllib.request
import pandas as pd
import zipfile
import time
import os

class sfCourtData:

    def byPassCaptcha(self):
        url = 'https://antcpt.com/anticaptcha-plugin.zip'
        # download the plugin
        filehandle, _ = urllib.request.urlretrieve(url)
        # unzip it
        with zipfile.ZipFile(filehandle, "r") as f:
            f.extractall("plugin")

        api_key = config('API_KEY')
        file = Path('./plugin/js/config_ac_api_key.js')
        file.write_text(file.read_text().replace("antiCapthaPredefinedApiKey = ''", "antiCapthaPredefinedApiKey = '{}'".format(api_key)))

        # zip plugin directory back to plugin.zip
        zip_file = zipfile.ZipFile('./plugin.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk("./plugin"):
                for file in files:
                    path = os.path.join(root, file)
                    zip_file.write(path, arcname=path.replace("./plugin/", ""))
        zip_file.close()

        options = webdriver.ChromeOptions()
        options.add_extension('./plugin.zip')

        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        pageurl = config('url')
        browser.get(pageurl)

        # wait for "solved" selector to come up
        WebDriverWait(browser, 120).until(lambda x: x.find_element_by_css_selector('.antigate_solver.solved'))
        # press submit button
        browser.find_element_by_css_selector('#submitButton').click()
        print("BYPASSED CAPTCHA!!")


    def getDataAtDate(self):

        driver = webdriver.Chrome(ChromeDriverManager().install())

        print("STATUS: now we input the desired date")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ui-id-3"))).click()

        dateText = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "FilingDate")))
        dateText.clear()
        dateText.send_keys('2022-07-01')

        #click search button to get court data
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "FilingsSearchBtn"))).click()

        #gets page source and loops through the court cases on that page and prints the case number and title
        page = 0
        time.sleep(5)

        html = driver.page_source
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
            html = driver.page_source
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

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "example_next"))).click()
        
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

print(dfData)

#dfData.to_csv('caseData.csv', index=False) 
#dfLinks.to_csv('links.csv', index=False)

"""
dfData.to_sql('case_info', conn, if_exists='replace', index=False)
dfLinks.to_sql('case_links', conn, if_exists='replace', index=False)

c.execute('''
SELECT * FROM case_info
SELECT * FROM case_links
''')
"""
