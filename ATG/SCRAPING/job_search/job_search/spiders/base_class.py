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


class BaseClassSpider(scrapy.Spider):
    name = 'base_class'
    allowed_domains = ['']
    start_urls = ['http:///']

    def parse(self, response):
        if response.status != 200:
            return None    # Couldn't crawl webpage #

