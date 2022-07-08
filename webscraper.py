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
import traceback
import subprocess
import glob, os
import time
import validators 
import pickle


"""
Attempt to use wget to download html page then bypass the captcha on the page if there is one
and then scrape data after the bypass of the captcha
"""

def existsElement(id):
    try:
        driver.findElement(By.ID, id)
    except:
        return False
    
    return True


api_key = '33888cf71b78f3a196074781246f8c12'

#run = true
#while(run):
#   userUrl = input("Enter a link to the site: ")

#   validUrl = validators.url(userUrl)

#   if(validUrl):
#       run = false

pageurl = 'https://webapps.sftc.org/ci/CaseInfo.dll?&SessionID=862EC7A358935F750140F1B7AE7E5F4F8D0D5DF1'
siteKey = '6Ldx5AwTAAAAAGrqJtWN13DX1U0_m-ueYEBVixBf'

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

#requests.get(pageurl)

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
        #driver.implicitly_wait(20)
        requ = res.json()['request']
        js = f'document.getElementById("g-recaptcha-response").innerHTML="{requ}";'
        driver.execute_script(js)
        #driver.find_element("name", "reCAPTCHA").submit() 
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
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
print("STATUS: Getting the case information")

while existsElement("pageinate_button next"):
    time.sleep(20)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('td')

    i = 0

    for case in tags:
        caseInfo = case.text
        
        if(not caseInfo.isnumeric()):
            if(i%2 == 0):
                print(f' Case Number: {caseInfo}')
            else:
                print(f' Case Title: {caseInfo}\n')
            i+=1

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pageinate_button next"))).click()

#else:
#    print("NOT A VALID URL")
