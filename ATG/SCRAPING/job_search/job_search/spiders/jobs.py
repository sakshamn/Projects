# -*- coding: utf-8 -*-

# Imports Begin #
#import scrapy
#import BaseClassSpider
# Imports End #

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


#class JobsSpider(BaseClassSpider):
class JobsSpider(scrapy.Spider):
    name = 'jobs'
    #allowed_domains = [
    #    'www.careerguide.com/career-options',
    #     "https://in.linkedin.com/jobs/search?keywords=&location=New%20Delhi%2C%20Delhi%2C%20India&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"
    #    'www.linkedin.com/jobs/search?keywords=&location=New%20Delhi%2C%20Delhi%2C%20India&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0'
    #]
    start_urls = [
        'https://www.careerguide.com/career-options/',
        "https://in.linkedin.com/jobs/search?keywords=&location=New%20Delhi%2C%20Delhi%2C%20India&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"
    ]

    def parse(self, response):
        if response.status != 200:
            self.logger.error("Couldn't Crawl Website!")
            return None    # Couldn't crawl webpage #

        #super().parse(response)

        jobs = response.css("div.col-md-4")
        links = []
        for job in jobs:
            category = job.css("h2.c-font-bold a::attr(title)").extract()
            subcategories = job.css("ul.c-content-list-1.c-theme.c-separator-dot li a::attr(title)").extract()

            if category != [] and category[0] in ["Exams and Syllabus", "Institutes in India", "Study Abroad"]:
                print("Skipping the category:", category)
                continue    # These are not job categories, skip them #

            print(category, subcategories)

            for subcategory in subcategories:
                links += [f"https://in.linkedin.com/jobs/search?keywords={subcategory}&location=New%20Delhi%2C%20Delhi%2C%20India&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"]

        for link in links:
            print("Parsing the link:", link)
            yield scrapy.Request(link, callback=self.parse_link)


    def parse_link(self, response):
        if response.status != 200:
            self.logger.error("Couldn't Crawl Website!")
            return None    # Couldn't crawl webpage #

        print("NSAK0")
        title = response.css("title::text").get()
        body = response.body

        #table = response.css("table").extract()

        print(body)
        #print(table)

# class JobsSpider # 


