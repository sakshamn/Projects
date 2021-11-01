# -*- coding: utf-8 -*-

# Imports Begin #
import scrapy
#import BaseClassSpider
# Imports End #


#class LinkedinJobsSpider(BaseClassSpider):
class LinkedinJobsSpider(scrapy.Spider):
    name = 'linkedin_jobs'
    allowed_domains = ['https://www.linkedin.com/jobs/search?keywords=&location=New%20Delhi%2C%20Delhi%2C%20India&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0']
    start_urls = ['https://www.linkedin.com/jobs/search?keywords=&location=New%20Delhi%2C%20Delhi%2C%20India&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0/']

    def parse(self, response):
        super().parse(response)

        jobs = response.css("")

