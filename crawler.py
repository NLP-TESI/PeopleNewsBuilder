import urllib, json
import scrapy
from scrapy.crawler import CrawlerProcess

class NewsSpider(scrapy.Spider):
    name = "NewsSpider"
    urlSearch = "http://g1.globo.com/politica/politico/dilma.html"

    def start_requests(self):
        self.search = getattr(self, 'search', '')
        # url = self.urlSearch+"?species=not%C3%ADcias&q="+self.search # set param: species=noticias
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news = response.xpath("//ul[@class='resultado_da_busca unstyled']/li")
        nextLink = response.xpath("//div[@id='paginador']/div/ul/li/a[@class='proximo fundo-cor-produto']/@href").extract_first()
        nextLink = self.urlSearch + nextLink
        for new in news:
            newLink = "http:"+new.xpath("div/div/a/@href").extract_first()
            jornalType = new.xpath("div/div/a/@title").extract_first()
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

class News:
    def __init__(self, created, lastPublication, modified, publication, id, summary, title, url, text=None):
        self.created = created
        self.lastPublication = lastPublication
        self.modified = modified
        self.publication = publication
        self.id = id
        self.summary = summary
        self.title = title
        self.url = url
        self.text = text

    def fetchText(self):
        # here come the scrapy stuffs to get text
        print self.url

class Sniffer:

    def __init__(self, initialUrl, newsLimit=0):
        self.newsLimit = newsLimit
        self.initialUrl = initialUrl
        self.news = []

    def _getNews(self):
        page = 0

        while len(self.news) < self.newsLimit:
            page += 1
            url = str.replace(self.initialUrl, "/page/1", "/page/"+str(page))
            response = urllib.urlopen(url)
            data = json.loads(response.read())

            for item in data['items']:
                n = News(created=item['created'],lastPublication=item['lastPublication'],modified=item['modified'],
                         publication=item['publication'],id=item['id'],summary=item['content']['summary'],
                         title=item['content']['title'],url=item['content']['url'])
                self.news.append(n)

                if len(self.news) == self.newsLimit:
                    break

    def _fetchTexts(self):
        for n in self.news:
            n.fetchText()

    def execute(self):
        self._getNews()
        self._fetchTexts()
                

if __name__ == "__main__":
    # URL for json news from Dilma Roussef
    url = "http://falkor-cda.bastian.globo.com/feeds/8351bc2f-9988-4fed-bc44-13d62a3e966f/posts/page/1/query_parameter/http://semantica.globo.com/G1/Politico_7c678a2c-2e99-4c45-b20b-76d15b9d77f8";
    sniffer = Sniffer(initialUrl=url, newsLimit=15)
    sniffer.execute()
