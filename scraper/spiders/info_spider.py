from xmlrpc.client import ResponseError
import scrapy
import json

class IndividualSpider(scrapy.Spider):
    name = "get_professor_info"

    def start_requests(self):
        links = open('links.txt', "r")
        urls = [link for link in links.readlines()]
        file = open("info.txt", "w")
        file.write("[")
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        p = response.css("div#content div.pure-content p")
        if (len(p) == 2):
            print(
                    response
                    .css("div#content h3.item-title::text")
                    .get()
            )
        if len(p) == 3:
            prof = {
                "name": response
                    .css("div#content h3.item-title::text")
                    .get(),
                "link": response.url,
                "img": response
                    .css("div#content article.single-event-content img::attr(src)")[1]
                    .extract(),
                "designation": response
                    .css("div#content h4.small-text::text")
                    .get(),
                "email": response
                    .css("div#content div.pure-content div.item-content::text")
                    .get(),
                "PhD": p[1].get()
                    .replace('<p><strong>PhD: </strong>', '')
                    .replace('<p><strong>PhD:</strong>', '')
                    .replace('</p>', '')
                    .lstrip(),
                "Research Area": p[2].get()
                    .replace('<p><strong>Research Area: </strong>', '')
                    .replace('<p><strong>Research Area:</strong>', '')
                    .replace('</p>', '')
                    .lstrip()
            }
        elif len(p) == 4:
            prof = {
                "name": response.css("div#content h3.item-title::text").get(),
                "link": response.url,
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
                "link": response.url,
                "img": response.css("div#content article.single-event-content img::attr(src)")[1].extract(),
                "designation": response.css("div#content h4.small-text::text").get(),
                "email": None,
                "PhD": None,
                "Research Area": None
            }
        # print(json.dumps(prof, indent = 4) + ",\n")
        file = open("info.txt", 'a')
        file.write(json.dumps(prof, indent = 4) + ",\n")