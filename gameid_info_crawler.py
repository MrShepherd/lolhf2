import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import dbhandler


class GameIDInfoCrawler(object):
    def __init__(self):
        self.idmapping_url = 'http://www.op.gg/spectate/list/'
        self.pro_ids = set()
        self.pro_gameids = set()
        self.idmapping_data = []
        self.gameid_info_url = 'http://www.op.gg/ranking/ladder/'
        self.gameids_ladder = set()
        self.gameids_add = set()
        self.gameid_info = []

    def crawl_idmapping_info(self):
        # service_args = ['--load-images=false']
        # browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs', service_args=service_args)
        browser = webdriver.PhantomJS(executable_path='/opt/phantomjs/bin/phantomjs')
        # browser = webdriver.Chrome()
        browser.set_page_load_timeout(30)
        print('getting:', self.idmapping_url)
        try:
            browser.get(self.idmapping_url)
        except TimeoutException:
            browser.execute_script('window.stop()')
        page_source = browser.page_source
        print('length of html:', len(page_source))
        # soup = htmlparser.HtmlParser(page_source)
        all_team = browser.find_elements_by_xpath('//div[@class="RegisterSummonerBox"]')
        print('number of teams found:', len(all_team))
        for team in all_team:
            all_li = team.find_elements_by_tag_name('li')
            # print('number of gameids found:', len(all_li))
            for li in all_li:
                tmp_dict = {}
                tmp_dict['player_team'] = team.find_element_by_xpath(".//div[@class='TeamName']").text
                tmp_dict['game_id'] = li.find_element_by_xpath('.//div[@class="SummonerName"]').text
                tmp_dict['player_name'] = li.find_element_by_xpath('.//span[@class="SummonerExtra"]').text.upper()
                # print(tmp_dict)
                self.idmapping_data.append(tmp_dict)
                self.pro_gameids.add(tmp_dict['game_id'])
                self.pro_ids.add(tmp_dict['player_name'])
                # print(len(self.idmapping_data))
                # print(self.idmapping_data)
        browser.close()
        browser.quit()
        print('number of gameids found:', len(self.pro_gameids))
        print(self.pro_gameids)
        print('number of pros found:', len(self.pro_ids))
        print(self.pro_ids)
        print('number of mapping groups found:', len(self.idmapping_data))
        print(self.idmapping_data)
        return self.idmapping_data

    def crawl_gameid_info(self):
        browser = webdriver.PhantomJS(executable_path="/opt/phantomjs/bin/phantomjs")
        # browser = webdriver.Chrome()
        browser.set_page_load_timeout(30)
        print('getting:', self.gameid_info_url)
        try:
            browser.get(self.gameid_info_url)
        except TimeoutException:
            browser.execute_script("window.stop()")
        count = 1
        while count <= 5:
            js = "document.body.scrollTop=%d000" % (count * 500)
            browser.execute_script(js)
            time.sleep(1)
            count += 1
        page_source = browser.page_source
        print('length of html:', len(page_source))
        all_gameid = browser.find_elements_by_xpath("//table[@class='LadderRankingTable']//tbody[@class='Body']//tr")
        for gameid in all_gameid:
            tmp_dict = {}
            tmp_dict['rank'] = gameid.find_element_by_xpath(".//td[contains(@class,'Rank') and contains(@class,'Cell')]").text
            tmp_dict['game_id'] = gameid.find_element_by_xpath(".//td[contains(@class,'SummonerName')]/a").text
            tmp_dict['link'] = gameid.find_element_by_xpath(".//td[contains(@class,'SummonerName')]/a").get_attribute("href")
            tmp_dict['tier'] = gameid.find_element_by_xpath(".//td[contains(@class,'TierRank')]").text
            tmp_dict['lp'] = gameid.find_element_by_xpath(".//td[contains(@class,'LP')]").text.split()[0].replace(',', '')
            tmp_dict['total_win'] = gameid.find_element_by_xpath(".//td[contains(@class,'RatioGraph')]//div[contains(@class,'Text') and contains(@class,'Left')]").text
            tmp_dict['total_lose'] = gameid.find_element_by_xpath(".//td[contains(@class,'RatioGraph')]//div[contains(@class,'Text') and contains(@class,'Right')]").text
            tmp_dict['total_win_ratio'] = gameid.find_element_by_xpath(".//td[contains(@class,'RatioGraph')]//span[@class='WinRatio']").text.replace('%', '')
            self.gameid_info.append(tmp_dict)
            self.gameids_ladder.add(tmp_dict['game_id'])
            # print(tmp_dict)
        print('number of gameids crawled:', len(self.gameids_ladder))
        self.gameids_add = self.pro_ids - self.gameids_ladder
        db_handler = dbhandler.DBHandler()
        gameids_db = set(db_handler.get_idmappingmanual_gameid())
        self.gameids_add = (gameids_db - self.gameids_ladder) | self.gameids_add
        print(self.gameids_add)
        browser.close()
        browser.quit()
        print('number of gameids crawled:', len(self.gameid_info))
        print(self.gameid_info)
        return self.gameid_info

    def close(self):
        pass
