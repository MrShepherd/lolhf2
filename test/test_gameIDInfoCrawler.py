from unittest import TestCase
from gameid_info_crawler import GameIDInfoCrawler
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


# from selenium.webdriver.common.keys import Keys


class TestGameIDInfoCrawler(TestCase):
    def test_crawl_idmapping_info(self):
        test_crawler = GameIDInfoCrawler()
        test_crawler.crawl_idmapping_info()
        self.assertTrue(1 == 1)

    def test_crawl_gameid_info(self):
        test_crawler = GameIDInfoCrawler()
        test_crawler.crawl_idmapping_info()
        test_crawler.crawl_gameid_info()
        self.assertTrue(1 == 1)

    def test_crawl_gameid(self):
        test_crawler = GameIDInfoCrawler()
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(30)
        try:
            browser.get(test_crawler.gameid_info_url)
        except TimeoutException:
            browser.execute_script("window.stop()")
        print('length of html:', len(browser.page_source))
        # browser.close()
        browser.quit()
        self.assertTrue(1 == 1)
