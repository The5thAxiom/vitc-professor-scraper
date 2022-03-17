from xmlrpc.client import ResponseError
import scrapy
import json

class ProfSpider(scrapy.Spider):
    name = "get_professor_links"

    def start_requests(self):
        urls = [
            'https://chennai.vit.ac.in/computer-science-engineering-chennai/faculty/',
            'https://chennai.vit.ac.in/academics/schools/sense/faculty/',
            'https://chennai.vit.ac.in/mechanical-engineering-chennai/faculty/',
            'https://chennai.vit.ac.in/electrical-and-electronics-engineering-chennai/faculty/',
            'https://chennai.vit.ac.in/academics/schools/sas/mfaculty',
            'https://chennai.vit.ac.in/academics/schools/sas/pfaculty',
            'https://chennai.vit.ac.in/academics/schools/sas/pfaculty'
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

class IndividualSpider(scrapy.Spider):
    name = "get_professor_info"

    def start_requests(self):
        links = open('links.txt', "r")
        urls = [link for link in links.readlines()]
        file = open("profs.txt", "w")
        file.write("[")
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        p = response.css("div#content div.pure-content p")
        if (len(p) == 4):
            prof = {
                "name": response.css("div#content h3.item-title::text").get(),
                "img": response.css("div#content article.single-event-content img::attr(src)")[1].extract(),
                "designation": response.css("div#content h4.small-text::text").get(),
                "email": p[1].get()
                    .replace('<p><strong>Email: </strong>', '')
                    .replace('<p><strong>Email:</strong>', '')
                    .replace('</p>', ''),
                "PhD": p[2].get()
                    .replace('<p><strong>PhD: </strong>', '')
                    .replace('<p><strong>PhD:</strong>', '')
                    .replace('</p>', '')
                    .lstrip(),
                "Research Area": p[3].get()
                    .replace('<p><strong>Research Area: </strong>', '')
                    .replace('<p><strong>Research Area:</strong>', '')
                    .replace('</p>', '')
                    .lstrip()
            }
        else:
            prof = {
                "name": response.css("div#content h3.item-title::text").get(),
                "img": response.css("div#content article.single-event-content img::attr(src)")[1].extract(),
                "designation": response.css("div#content h4.small-text::text").get(),
                "email": '',
                "PhD": '',
                "Research Area": ''
            }
        print(prof)
        file = open("profs.txt", 'a')
        file.write(json.dumps(prof, indent = 4) + ",\n")