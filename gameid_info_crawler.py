from selenium import webdriver
from selenium.common.exceptions import TimeoutException


class GameIDInfoCrawler(object):
    def __init__(self):
        self.idmapping_url = 'http://www.op.gg/spectate/list/'
        self.pro_ids = set()
        self.pro_gameids = set()
        self.idmapping_data = []

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
        pass

    def close(self):
        pass
