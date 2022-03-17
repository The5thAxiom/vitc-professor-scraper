clear:
	rm links.txt && rm info.txt

links:
	scrapy crawl get_professor_links

info:
	scrapy crawl get_professor_info
	python makeValidJson.py

all:
	make clear
	make links
	make info