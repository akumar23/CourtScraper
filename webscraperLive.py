import subprocess
import glob, os
import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring 
from itertools import cycle
import traceback

"""
Prints all the case information from one page of case details.
This code will be copied and looped for every page of cases per day
"""

with open('Case Information.html', 'r') as html_file:
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
