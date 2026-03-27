import json
import scrapy 
from urllib.parse import urlencode

class IndeedJobSpider(scrapy.Spider):
    name = 'indeed_jobs'

    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters = {'q': keyword, 'l': location, "filters": 0, "start": offset}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)
    

