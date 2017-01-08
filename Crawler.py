# Execute this using Python 3

import os
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from News import News

class NewsSpider(scrapy.Spider):
    name = "NewsSpider"

    def start_requests(self):
        self.newsList = getattr(self, 'newsList', None)
        
        for i, news in enumerate(self.newsList):
            yield scrapy.Request(url=news.url, callback=self.parse, meta={'i': i})

    def parse_materia_letra(self, response):
        content = response.css('#materia-letra')
        if(len(content.xpath('.//p')) == 0):
            return None

        text = ''
        for p in content.xpath('.//p'):
            text += ''.join(p.css(' ::text').extract())

        return text

    def parse_div_content_text(self, response):
        # Todo
        return None

    def parse(self, response):
        index = response.meta['i']

        trials = [self.parse_materia_letra, self.parse_div_content_text]
        text = None

        for t in trials:
            text = t(response)
            if(text != None) : break

        if(text != None):
            self.newsList[index].text = text.replace('\t','').replace('\n', ' ').strip()

class Crawler:
    def __init__(self, newsList=None, spider=NewsSpider):
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        self.process.crawl(spider, newsList=newsList)

    def crawl(self):
        # the script will block here until the crawling is finished
        self.process.start()

class Sniffer:

    def __init__(self, initialUrl, newsLimit=0, name='person'):
        self.newsLimit = newsLimit
        self.initialUrl = initialUrl
        self.news = []
        self.name = name

    def _getNews(self):
        page = 0

        while len(self.news) < self.newsLimit:
            page += 1
            url = str.replace(self.initialUrl, "/page/1", "/page/"+str(page))
            data = requests.get(url=url).json()

            for item in data['items']:
                n = News(created=item['created'],lastPublication=item['lastPublication'],modified=item['modified'],
                         publication=item['publication'],id=item['id'],summary=item['content']['summary'],
                         title=item['content']['title'],url=item['content']['url'])
                self.news.append(n)

                if len(self.news) == self.newsLimit:
                    break

    def _fetchTexts(self):
        crawler = Crawler(newsList=self.news)
        crawler.crawl()

    def _saveNewsAsJSON(self):
        if(not os.path.exists(os.path.join('database', self.name))):
            os.makedirs(os.path.join('database', self.name))

        for n in self.news:
            n.dumpsToJSON(os.path.join('database', self.name, n.id))

    def execute(self):
        self._getNews()
        self._fetchTexts()
        self._saveNewsAsJSON()
                


if __name__ == "__main__":
    # URL for json news from Dilma Roussef
    url = "http://falkor-cda.bastian.globo.com/feeds/8351bc2f-9988-4fed-bc44-13d62a3e966f/posts/page/1/query_parameter/http://semantica.globo.com/G1/Politico_7c678a2c-2e99-4c45-b20b-76d15b9d77f8";
    sniffer = Sniffer(initialUrl=url, newsLimit=1, name='dilma')
    sniffer.execute()
