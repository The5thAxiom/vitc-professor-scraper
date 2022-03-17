from xmlrpc.client import ResponseError
import scrapy
import json

class IndividualSpider(scrapy.Spider):
    name = "get_professor_info"

    def start_requests(self):
        links = open('links.txt', "r")
        urls = [link for link in links.readlines()]
        file = open("info.txt", "w")
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        paras = response.css("div#content div.pure-content p")
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
            "email": None,
            "PhD": None,
            "Research Area": None
        }
        if len(paras) == 3:
            prof["email"] = response\
                .css("div#content div.pure-content div.item-content::text")\
                .get()
            prof["PhD"] = paras[1].get()\
                .replace('<p><strong>PhD: </strong>', '')\
                .replace('<p><strong>PhD:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
            prof["Research Area"] = paras[2].get()\
                .replace('<p><strong>Research Area: </strong>', '')\
                .replace('<p><strong>Research Area:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
        elif len(paras) == 4:
            prof["email"] = paras[1].get()\
                .replace('<p><strong>Email: </strong>', '')\
                .replace('<p><strong>Email:</strong>', '')\
                .replace('</p>', '')
            prof["PhD"] = paras[2].get()\
                .replace('<p><strong>PhD: </strong>', '')\
                .replace('<p><strong>PhD:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
            prof["Research Area"] = paras[3].get()\
                .replace('<p><strong>Research Area: </strong>', '')\
                .replace('<p><strong>Research Area:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
        print(json.dumps(prof, indent = 4) + ",\n")
        file = open("info.txt", 'a')
        file.write(json.dumps(prof, indent = 4) + ",\n")