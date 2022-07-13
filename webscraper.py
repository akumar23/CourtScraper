import time, requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import false 
from webdriver_manager.chrome import ChromeDriverManager
from itertools import cycle
from selenium import webdriver
import time
from decouple import config

"""
Program that uses the 2captcha API to bypass the captcha if there is one
and then scrape the information of court cases that happened on a given date
"""

api_key = config('API_KEY')

#run = true
#while(run):
#   userUrl = input("Enter a link to the site: ")

#   validUrl = validators.url(userUrl)

#   if(validUrl):
#       run = false

pageurl = config('url')
siteKey = config('site_key')

#code to automate finding the captcha key in the site
"""
with open('CaseInfo.dll?', 'r') as dll_file:
content = dll_file.read()
soup = BeautifulSoup(content, 'lxml')

captcha = soup.find_all('div', class_ = 'g-recaptcha')

if(not captcha == []):
    for key in captcha:
         #currKey = key.text
        print(key.text)

    keys = soup.find_all('data-callback')
    for id in keys:
        print(id.text)
"""

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(pageurl)

form = {"method": "userrecaptcha",
        "googlekey": siteKey,
        "key": api_key,
        "pageurl": pageurl, 
        "json": 1 }

response = requests.post('http://2captcha.com/in.php', data=form)
request_id = response.json()['request']

url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1"

status = 0
while not status:
    res = requests.get(url)
    if res.json()['status']==0:
        time.sleep(3)
    else:
        requ = res.json()['request']
        js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
        driver.execute_script(js)
        WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
        status = 1


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
table = soup.find_all('dataTables_info')

list = []
for i in table:
    word = i.text
    if word.isnumeric():
        list.append(word)

maxCount = list[len(list)-1]

while page <= maxCount/10:
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('td')      
    page += 1
    print("STATUS: Getting the case information for page {page}")
    time.sleep(5)
    i = 0

    for case in tags:
        caseInfo = case.text
        
        if(not caseInfo.isnumeric()):
            if(i%2 == 0):
                print(f' Case Number: {caseInfo}')
            else:
                print(f' Case Title: {caseInfo}\n')
            i+=1

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "example_next"))).click()

#else:
#    print("NOT A VALID URL")
