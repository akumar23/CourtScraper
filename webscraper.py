import time
import urllib.request
import zipfile
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# download the plugin
url = 'https://antcpt.com/anticaptcha-plugin.zip'
filehandle, _ = urllib.request.urlretrieve(url)
# unzip it
with zipfile.ZipFile(filehandle, "r") as f:
    f.extractall("plugin")

# set API key in configuration file
api_key = "34a9934eaeb3bdee8e6c7f89d32c962e"
file = Path('./plugin/js/config_ac_api_key.js')
file.write_text(file.read_text().replace("antiCapthaPredefinedApiKey = ''", "antiCapthaPredefinedApiKey = '{}'".format(api_key)))

# zip plugin directory back to plugin.zip
zip_file = zipfile.ZipFile('./plugin.zip', 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk("./plugin"):
        for file in files:
            path = os.path.join(root, file)
            zip_file.write(path, arcname=path.replace("./plugin/", ""))
zip_file.close()

# set browser launch options
options = webdriver.ChromeOptions()
options.add_extension('./plugin.zip')

# set browser launch options
browser = webdriver.Chrome('./chromedriver', options=options)

# navigate to the target page
browser.get('https://webapps.sftc.org/captcha/captcha.dll?referrer=https://webapps.sftc.org/ci/CaseInfo.dll?%22%22%22%22%22%22')

# wait for "solved" selector to come up
time.sleep(120)
#browser.find_element(By.CSS_SELECTOR, '.antigate_solver.solved')

# press submit button
#browser.find_element(By.CSS_SELECTOR , '#submitButton').click()

print("SOLVED!")

print("STATUS: now we input the desired date")
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.ID, "ui-id-3"))).click()

dateText = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "FilingDate")))
dateText.clear()
dateText.send_keys('2022-07-01')
