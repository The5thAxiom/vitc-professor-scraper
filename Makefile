clear:
	rm links.txt && rm profs.txt

links:
	scrapy crawl get_professor_links

info:
	scrapy crawl get_professor_info