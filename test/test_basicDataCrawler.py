from unittest import TestCase

from basic_data_crawler import BasicDataCrawler


class TestBasicDataCrawler(TestCase):
    def test_crawl_team_info(self):
        testcrawler = BasicDataCrawler()
        testcrawler.collect_page()
        self.assertTrue(len(testcrawler.crawl_team_info()) > 10)
