import scrapy
import json

class CourtDataSpider(scrapy.Spider):
    name = 'court-data'
    allowed_domains = ['webapps.sftc.org']
    start_urls = ['https://webapps.sftc.org/ci/CaseInfo.dll/datasnap/rest/TServerMethods1/GetCasesWithFilings/2022-08-26/46506EA6633D5024DBAA8DA85C67E6F43339B429/']

    def parse(self, response):
        resp = json.loads(response.body)
        court_data = json.dumps(resp['result'][1])['CASE_NUMBER']

        yield {
            "Case Number" : court_data
        }
