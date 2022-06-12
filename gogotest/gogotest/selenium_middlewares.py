# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common import action_chains
import chromedriver_binary
import pprint as pp
import json

import datetime

driver = webdriver.Chrome()

class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        driver.get(request.url)
                # 必要な要素が揃うまで15秒を上限として待機
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item')))
        return HtmlResponse(driver.current_url,
                            body=driver.page_source,
                            encoding='utf-8',
                            request=request)


def close_driver():
    driver.close()
