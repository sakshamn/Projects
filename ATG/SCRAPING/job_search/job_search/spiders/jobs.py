# -*- coding: utf-8 -*-

# Imports Begin #
import scrapy, sys
# Imports End #


# Globals Begin #
OUTPUT_FILE = open("output.log", "w")

# Preserve the standard output to a variable original_stdout. #
# Change the standard output to a file so that all prints are redirected. #
original_stdout = sys.stdout
sys.stdout = OUTPUT_FILE
# Globals End #

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://www.careerguide.com/career-options']
    start_urls = ['https://www.careerguide.com/career-options/']

    def parse(self, response):
        if response.status != 200:
            return None    # Couldn't crawl webpage #

        jobs = response.css("div.col-md-4")
        for job in jobs:
            category = job.css("h2.c-font-bold a::attr(title)").extract()
            subcategory = job.css("ul.c-content-list-1.c-theme.c-separator-dot li a::attr(title)").extract()
            print(category, subcategory)

# class JobsSpider # 

