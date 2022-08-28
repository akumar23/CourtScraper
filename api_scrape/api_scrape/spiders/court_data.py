import scrapy
import json

class CourtDataSpider(scrapy.Spider):
    name = 'court-data'
    allowed_domains = ['webapps.sftc.org']
    start_urls = ['https://webapps.sftc.org/ci/CaseInfo.dll/datasnap/rest/TServerMethods1/GetCasesWithFilings/2022-08-26/49F92C8A8BDE62822F30E5471C478E65CE4C0711/']

    def parse(self, response):
        resp = json.loads(response.body)
        yield {
            "Data" : resp
        }
