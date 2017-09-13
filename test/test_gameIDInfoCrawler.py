from unittest import TestCase
from gameid_info_crawler import GameIDInfoCrawler


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
