
# -*- coding: utf-8 -*-
import scrapy
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from selenium_middlewares import close_driver

class AdventarSpider(scrapy.Spider):
    name = 'adventar_spider'
    allowed_domain = 'adventar.org'
    base_url = 'https://adventar.org'
    start_urls = [
        'https://adventar.org/calendars?year=2019'
        ]
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "selenium_middlewares.SeleniumMiddleware": 0
        },
        "DOWNLOAD_DELAY": 1
    }

    def parse(self, response):
        ads = response.xpath('//*[@id="__layout"]/div/div/main/div/div/ul/li')
        for ad in ads:
            title = ad.xpath('a/text()').extract_first()
            url = ad.xpath('a/@href').extract_first()
            value = ad.xpath('div/span[@class="indicator"]/span/@data-value').extract_first()
            yield {
                'title': title,
                'url': self.base_url + url,
                'value': value
            }

    def closed(self, reason):
        close_driver()
