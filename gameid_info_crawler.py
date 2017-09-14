import time
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from multiprocessing.dummy import Pool
import dbhandler
import htmlparser


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
        self.invalid_gameids = set()

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
        page_html = browser.page_source
        print('length of html:', len(page_html))
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

    def crawl_gameid_info_by_search(self, gameid):
        browser = webdriver.PhantomJS(executable_path="/opt/phantomjs/bin/phantomjs")
        # browser = webdriver.Firefox()
        browser.set_page_load_timeout(30)
        # time.sleep(random.randint(1, 8))
        try:
            browser.get(self.gameid_info_url)
        except TimeoutException:
            browser.execute_script("window.stop()")
        form = browser.find_element_by_xpath("//div[@class='PageHeaderWrap']//form[@class='FormItem']//input[@class='Input']")
        form.clear()
        form.send_keys(gameid)
        try:
            form.send_keys(Keys.RETURN)
        except TimeoutException:
            browser.execute_script("window.stop()")
        time.sleep(3)
        browser.execute_script("window.stop()")
        page_html = browser.page_source
        soup = htmlparser.HtmlParser(page_html).get_soup()
        selected_row = soup.find("table", class_="LadderRankingTable").find("tr", class_="Selected")
        try:
            tmp_dict = {}
            tmp_dict['rank'] = selected_row.find("td", class_="Rank").get_text()
            tmp_dict['game_id'] = selected_row.find("td", class_="SummonerName").find("a").get_text()
            tmp_dict['link'] = 'http:' + selected_row.find("td", class_="SummonerName").find("a").get("href")
            tmp_dict['tier'] = selected_row.find("td", class_="TierRank").get_text()
            tmp_dict['lp'] = selected_row.find("td", class_="LP").get_text().split()[0].replace(',', '')
            tmp_dict['total_win'] = selected_row.find("td", class_="RatioGraph").find("div", {"class": "Text Left"}).get_text()
            tmp_dict['total_lose'] = selected_row.find("td", class_="RatioGraph").find("div", {"class": "Text Right"}).get_text()
            tmp_dict['total_win_ratio'] = selected_row.find("td", class_="RatioGraph").find("span", class_="WinRatio").get_text().replace('%', '')
            print(tmp_dict)
            self.gameid_info.append(tmp_dict)
        except Exception as e:
            print('invalid gameid:', gameid, ':', e)
            self.invalid_gameids.add(gameid)
        self.gameids_add.remove(gameid)
        print('gameids left:', len(self.gameids_add))
        browser.quit()
        # browser.close()
        return 'ok'

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
        while count <= 20:
            js = "document.body.scrollTop=%d000" % (count * 500)
            browser.execute_script(js)
            time.sleep(1)
            count += 1
            # print('length of html:', len(browser.page_source))
        page_html = browser.page_source
        print('length of html:', len(page_html))
        soup = htmlparser.HtmlParser(page_html).get_soup()
        all_gameid = soup.find("table", class_="LadderRankingTable").find_all("tr")
        for gameid in all_gameid[1:-1]:
            tmp_dict = {}
            tmp_dict['rank'] = gameid.find("td", class_="Rank").get_text()
            tmp_dict['game_id'] = gameid.find("td", class_="SummonerName").find("a").get_text()
            tmp_dict['link'] = 'http:' + gameid.find("td", class_="SummonerName").find("a").get("href")
            tmp_dict['tier'] = gameid.find("td", class_="TierRank").get_text()
            tmp_dict['lp'] = gameid.find("td", class_="LP").get_text().split()[0].replace(',', '')
            tmp_dict['total_win'] = gameid.find("td", class_="RatioGraph").find("div", {"class": "Text Left"}).get_text()
            tmp_dict['total_lose'] = gameid.find("td", class_="RatioGraph").find("div", {"class": "Text Right"}).get_text()
            tmp_dict['total_win_ratio'] = gameid.find("td", class_="RatioGraph").find("span", class_="WinRatio").get_text().replace('%', '')
            self.gameid_info.append(tmp_dict)
            self.gameids_ladder.add(tmp_dict['game_id'])
            # print(tmp_dict)
        print('number of gameids crawled:', len(self.gameids_ladder))
        self.gameids_add = self.pro_gameids - self.gameids_ladder
        db_handler = dbhandler.DBHandler()
        gameids_db = set(db_handler.get_idmappingmanual_gameid())
        self.gameids_add = (gameids_db - self.gameids_ladder) | self.gameids_add
        print('number of gameids still need to be crawled:', len(self.gameids_add))
        print(self.gameids_add)
        browser.close()
        browser.quit()
        while len(self.gameids_add) != 0:
            pool = Pool(8)
            pool.map(self.crawl_gameid_info_by_search, self.gameids_add)
            pool.close()
            pool.join()
        print('invalid gameids found:', len(self.invalid_gameids))
        print(self.invalid_gameids)
        print('number of gameids crawled:', len(self.gameid_info))
        print(self.gameid_info)
        return self.gameid_info

    def close(self):
        pass
