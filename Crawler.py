# Execute this using Python 2.7

import os
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from News import News

# This spider collect text from the News in the g1.globo.com
class NewsSpider(scrapy.Spider):
    name = "NewsSpider"

    # Start to get requests from news.url
    def start_requests(self):
        self.newsList = getattr(self, 'newsList', [])
        for i, news in enumerate(self.newsList):
            yield scrapy.Request(url=news.url, callback=self.parse, meta={'i': i})

    # A page contain many section of text. This method concat all these sections
    # at one string
    def concat_text_list(self, text_list_selector):
        text = ''
        for t in text_list_selector:
            text += t.extract()

        if text == '':
            return None
        return text

    # parser for pages with div id="materia-letra"
    def parse_materia_letra(self, response):
        text_list = response.xpath("//*[@id='materia-letra']/descendant::p/descendant-or-self::text()")
        return self.concat_text_list(text_list)

    # parser for pages with div class="content-text"
    def parse_div_content_text(self, response):
        text_list = response.xpath("//div[contains(@class, 'content-text')]/descendant-or-self::text()")
        return self.concat_text_list(text_list)

    # parse a page result in response. Try to use any parser at trials list to get text of the news
    def parse(self, response):
        index = response.meta['i']

        trials = [self.parse_materia_letra, self.parse_div_content_text]
        text = None

        for t in trials:
            text = t(response)
            if text is not None: break

        if text is not None:
            self.newsList[index].text = text.replace('\t',' ').replace('\n', '.').strip()

# It is just to handle the crawler
class Crawler:
    def __init__(self, spider, **kwargs):
        self.process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        self.process.crawl(spider, **kwargs)

    def crawl(self):
        # the script will block here until the crawling is finished
        self.process.start()

# This collect the data of all News about one person
class Sniffer:

    def __init__(self, initialUrl, newsLimit=0, name='person'):
        self.newsLimit = newsLimit
        self.initialUrl = initialUrl
        self.news = []
        self.name = name

    # get the first x news url from a json. This json is provided to a ajax in the G1 site.
    def _getNews(self):
        page = 0

        while len(self.news) < self.newsLimit:
            page += 1
            url = self.initialUrl.replace("/page/1", "/page/"+str(page))
            response = requests.get(url=url)
            if response.status_code == 200:
                data = response.json()

                for item in data['items']:
                    item.update(item['content'])
                    n = News(**item)
                    self.news.append(n)

                    if len(self.news) == self.newsLimit:
                        break
            else:
                page -= 1

    # Init the crawler proccess for the URL list
    def _fetchTexts(self):
        crawler = Crawler(NewsSpider, newsList=self.news)
        crawler.crawl()

    # Save news infos at a JSON
    def _saveNewsAsJSON(self):
        if(not os.path.exists(os.path.join('database', self.name))):
            os.makedirs(os.path.join('database', self.name))

        for n in self.news:
            n.dumpsToJSON(os.path.join('database', self.name, n.id))

    # Execute the Sniffer
    def execute(self):
        self._getNews()
        self._fetchTexts()
        self._saveNewsAsJSON()


# This is just to test the Sniffer class
if __name__ == "__main__":
    # URL for json news from Dilma Roussef
    url = "http://falkor-cda.bastian.globo.com/feeds/8351bc2f-9988-4fed-bc44-13d62a3e966f/posts/page/1/query_parameter/http://semantica.globo.com/G1/Politico_7c678a2c-2e99-4c45-b20b-76d15b9d77f8";
    sniffer = Sniffer(initialUrl=url, newsLimit=1, name='dilma')
    sniffer.execute()
