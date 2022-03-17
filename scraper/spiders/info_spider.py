from xmlrpc.client import ResponseError
import scrapy
import json

class IndividualSpider(scrapy.Spider):
    name = "get_professor_info"

    def start_requests(self):
        links = open('links.txt', "r")
        urls = [link for link in links.readlines()]
        file = open("info.txt", "w")
        file.write("")
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        paras = response.css("div#content div.pure-content p")
        info = {
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
            info["email"] = response\
                .css("div#content div.pure-content div.item-content::text")\
                .get()
            info["PhD"] = paras[1].get()\
                .replace('<p><strong>PhD: </strong>', '')\
                .replace('<p><strong>PhD:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
            info["Research Area"] = paras[2].get()\
                .replace('<p><strong>Research Area: </strong>', '')\
                .replace('<p><strong>Research Area:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
        elif len(paras) == 4:
            info["email"] = paras[1].get()\
                .replace('<p><strong>Email: </strong>', '')\
                .replace('<p><strong>Email:</strong>', '')\
                .replace('</p>', '')
            info["PhD"] = paras[2].get()\
                .replace('<p><strong>PhD: </strong>', '')\
                .replace('<p><strong>PhD:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
            info["Research Area"] = paras[3].get()\
                .replace('<p><strong>Research Area: </strong>', '')\
                .replace('<p><strong>Research Area:</strong>', '')\
                .replace('</p>', '')\
                .lstrip()
        infoJson = json.dumps(info, indent = 4)
        print(infoJson + ",\n")
        file = open("info.txt", 'a')
        file.write(infoJson + "\n")