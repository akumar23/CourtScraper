import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from webdriver_manager.chrome import ChromeDriverManager
from itertools import cycle
from selenium import webdriver
import traceback
import subprocess
import glob, os
import time

"""
Attempt to use wget to download html page then bypass the captcha on the page if there is one
and then scrape data after the bypass of the captcha
"""

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

#runcmd("wget https://webapps.sftc.org/ci/CaseInfo.dll?&SessionID=862EC7A358935F750140F1B7AE7E5F4F8D0D5DF1", verbose = True)

"""
os.chdir("/")
for file in glob.glob("*.html"):
    print(file)
"""

siteKey = '6Ldx5AwTAAAAAGrqJtWN13DX1U0_m-ueYEBVixBf'
pageurl = 'https://webapps.sftc.org/ci/CaseInfo.dll?&SessionID=862EC7A358935F750140F1B7AE7E5F4F8D0D5DF1'
api_key = '33888cf71b78f3a196074781246f8c12'

#driver = webdriver.Chrome(ChromeDriverManager().install())
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
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
        status = 1

"""
Need to fix this part by getting the right elements on the webpage to click on
"""
if(status == 1):
    print("STATUS: now we get the dates")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "#tabs-3"))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "FilingDate"))).click()   
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, " data-month='5'"))).click()     

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

"""
with open('Case Information.html', 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')

    captcha = soup.find_all('div', class_ = 'g-recaptcha')

    print(captcha)

    
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
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
"""
