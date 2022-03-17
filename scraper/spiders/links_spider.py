from xmlrpc.client import ResponseError
import scrapy
import json

class ProfSpider(scrapy.Spider):
    name = "get_professor_links"

    def start_requests(self):
        file = open('links.txt', "w")
        file.write("")
        urls = [
            'https://chennai.vit.ac.in/computer-science-engineering-chennai/faculty/',
            'https://chennai.vit.ac.in/academics/schools/sense/faculty/',
            'https://chennai.vit.ac.in/mechanical-engineering-chennai/faculty/',
            'https://chennai.vit.ac.in/electrical-and-electronics-engineering-chennai/faculty/',
            'https://chennai.vit.ac.in/academics/schools/sas/mfaculty',
            'https://chennai.vit.ac.in/academics/schools/sas/pfaculty',
            'https://chennai.vit.ac.in/academics/schools/sas/pfaculty',
            'https://chennai.vit.ac.in/academics/schools/ssl/faculty/'
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        file = open('links.txt', "a")
        profs = []
        for text in response.css("h3.item-title a.main-color-1-hover::attr(href)"):
            profs.append(text.get())
        for prof in profs:
            print(prof)
            file.write(prof)
            file.write("\n")
