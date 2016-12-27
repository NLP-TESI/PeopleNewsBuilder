import scrapy
from scrapy.crawler import CrawlerProcess

class NewsSpider(scrapy.Spider):
    name = "NewsSpider"
    urlSearch = "http://www.globo.com/busca/"

    def start_requests(self):
        self.search = getattr(self, 'search', '')
        url = self.urlSearch+"?species=not%C3%ADcias&q="+self.search
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news = response.xpath("//ul[@class='resultado_da_busca unstyled']/li")
        nextLink = response.xpath("//div[@id='paginador']/div/ul/li/a[@class='proximo fundo-cor-produto']/@href").extract_first()
        nextLink = self.urlSearch + nextLink
        for new in news:
            newLink = "http:"+new.xpath("div/div/a/@href").extract_first()
            jornalType = new.xpath("div/div/p/span/text()").extract_first()
            print "---------------------------"
            print jornalType, "=====", newLink
        print "next ====", nextLink



class Crawler:

    def __init__(self, spider=NewsSpider, search=None):
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        self.process.crawl(spider, search=search)

    def crawl(self):
        self.process.start() # the script will block here until the crawling is finished


if __name__ == "__main__":
    import sys
    crawler = Crawler(search=sys.argv[1])
    crawler.crawl()
