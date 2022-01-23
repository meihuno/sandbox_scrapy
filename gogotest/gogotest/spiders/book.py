import scrapy
from gogotest.items import GogotestItem

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

class BookSpider(CrawlSpider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    rules = (
        # allow=[r'/catalogue/page-[\d]+.html$/', r'books.toscrape.com/$'],
        # 記事を allow=[r'/catalogue/page-[\d]+.html$/', 'books.toscrape.com/$'],
        # 記事ページから記事ページを抽出しないようにしたい。何ページにあったかを記憶するために。
        Rule(LinkExtractor(
            restrict_css='section div ol li article.product_pod h3 a'),
            callback='parse_book', follow=False),
        
        Rule(LinkExtractor(restrict_css='li.next a'), callback='parse_page', follow=True),
    )
    
    def __init__(self, *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs) #引数を受け取るための継承
        self.counter = 0
        self.close_manually = False

    #
    def parse_page(self, response):
        # print(["Gogo!", response.url])
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        pass
    
    def parse_book(self, response):
        i = {}
        refurl = response.request.headers['referer']
        url = response.url
        # print(["Ref GoGo", refurl, url])
        i['name'] = 'book'
        i['url'] = url
        i['refurl'] = str(refurl)
        i['title'] = response.css('article.product_page div.row div h1::text').get()

        self.counter += 1
        # if self.counter == 10:
        # raise CloseSpider('Page is full')

        if self.close_manually:
            raise CloseSpider('Already been scraped.')
        
        yield i
