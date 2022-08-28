import scrapy
import json

class CourtDataSpider(scrapy.Spider):
    name = 'court-data'
    allowed_domains = ['webapps.sftc.org']
    start_urls = ['https://webapps.sftc.org/ci/CaseInfo.dll/datasnap/rest/TServerMethods1/GetCasesWithFilings/2022-08-26/30307C63056FAB05FC6E750B80A9B8DDA3A55D87/']

    def parse(self, response):
        resp = json.loads(response.body)
        yield {
            "Data" : resp['result']['CASE_NUMBER']
        }
