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

        #items = JobSearchItem()
        #body = response.body

        #categories = response.css("h2.c-font-bold a::attr(title)").extract()
        ## Replace the spaces in the class name by "." #
        #subcategories = response.css("ul.c-content-list-1.c-theme.c-separator-dot li a::attr(title)").extract()
        #print(categories, "\n", subcategories)

        output = response.css("div.col-md-4").getall()
        print(output)

        #for category in categories:
        #    print(category)
            #links = ultrabooks.css("div.archive-text2 a::attr(href)").extract()
            #images = ultrabooks.css("div.archive-image img::attr(src)").extract()
            #print("Link:\n", links)
            #print("Image:\n", images)

            #for link in links:
            #    yield scrapy.Request(link, callback=self.parse_link)

            #items["images"] = images
            #yield items # send images to item class - JobSearchItem #

