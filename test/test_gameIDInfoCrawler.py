from unittest import TestCase
from gameid_info_crawler import GameIDInfoCrawler
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time


# from selenium.webdriver.common.keys import Keys


class TestGameIDInfoCrawler(TestCase):
    def test_crawl_idmapping_info(self):
        test_crawler = GameIDInfoCrawler()
        test_crawler.crawl_idmapping_info()
        self.assertTrue(1 == 1)

    def test_crawl_gameid_info(self):
        print(time.strftime("%H:%M:%S", time.localtime()))
        test_crawler = GameIDInfoCrawler()
        test_crawler.crawl_idmapping_info()
        test_crawler.crawl_gameid_info()
        self.assertTrue(1 == 1)

    def test_crawl_gameid(self):
        test_crawler = GameIDInfoCrawler()
        browser = webdriver.Firefox()
        browser.set_page_load_timeout(15)
        try:
            browser.get(test_crawler.gameid_info_url)
        except TimeoutException:
            browser.execute_script("window.stop()")
        print('length of html:', len(browser.page_source))
        test_gameids = {'M M M M O O O O', 'SSG 메르시', '열심히할게요오', 'SIlde', 'Nox OaO', 'Wo jo lan A', 'RPG Evi'}
        browser.set_page_load_timeout(10)
        for gameid in test_gameids:
            form = browser.find_element_by_xpath("//div[@class='PageHeaderWrap']//form[@class='FormItem']//input[@class='Input']")
            form.clear()
            form.send_keys(gameid)
            try:
                form.send_keys(Keys.RETURN)
            except TimeoutException:
                browser.execute_script("window.stop()")
            time.sleep(5)
            browser.execute_script("window.stop()")
            try:
                tmp_dict = {}
                tmp_dict['rank'] = browser.find_element_by_xpath("//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'Rank') and contains(@class,'Cell')]").text
                tmp_dict['game_id'] = browser.find_element_by_xpath("//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'SummonerName')]/a").text
                tmp_dict['link'] = browser.find_element_by_xpath("//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'SummonerName')]/a").get_attribute("href")
                tmp_dict['tier'] = browser.find_element_by_xpath("//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'TierRank')]").text
                tmp_dict['lp'] = browser.find_element_by_xpath("//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'LP')]").text.split()[0].replace(',', '')
                tmp_dict['total_win'] = browser.find_element_by_xpath(
                    "//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'RatioGraph')]//div[contains(@class,'Text') and contains(@class,'Left')]").text
                tmp_dict['total_lose'] = browser.find_element_by_xpath(
                    "//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'RatioGraph')]//div[contains(@class,'Text') and contains(@class,'Right')]").text
                tmp_dict['total_win_ratio'] = browser.find_element_by_xpath(
                    "//table[@class='LadderRankingTable']//tr[contains(@class,'Selected')]//td[contains(@class,'RatioGraph')]//span[@class='WinRatio']").text.replace('%', '')
                print(tmp_dict)
            except NoSuchElementException:
                print('bad gameid')
        # browser.close()
        browser.quit()
        self.assertTrue(1 == 1)
