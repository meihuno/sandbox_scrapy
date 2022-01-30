# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exceptions import CloseSpider
from gogotest.consqlite import DBConnection
import scrapy

class GogotestPipeline:

    def open_spider(self, spider: scrapy.Spider):
        # コネクションの開始
        self.conn = DBConnection()
        self.book_dict = self.conn.ret_find_book("book")
        self.exist_book_dict = {}
        self.page_check_dict = {}
        
    def close_spider(self, spider: scrapy.Spider):
        # コネクションの終了
        self.conn.close()

    def process_item(self, item, spider):
        url = item['url']
        refurl = item['refurl']

        if not refurl in self.exist_book_dict:
            self.exist_book_dict[refurl] = {}
            self.page_check_dict[refurl] = {'total': 0, 'exist': 0}

            
            for ref, freq_dict in self.page_check_dict.items():
                total = freq_dict['total']
                if not total == 0:
                    ct = freq_dict['exist'] / total
                    if ct == 1.0:
                        print(["IN", refurl, ref,  ct])
                        spider.close_manually = True
        
        self.page_check_dict[refurl]['total'] += 1
        
        if url in self.book_dict:
            self.exist_book_dict[refurl][url] = True
            self.page_check_dict[refurl]['exist'] += 1
            raise DropItem(f"Dropping exisiting {url}")
        else:
            self.exist_book_dict[refurl][url] = False
            self.conn.save_book(item)
            return item
