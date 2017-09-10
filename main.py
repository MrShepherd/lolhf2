import sys
import time

import basic_data_crawler
import dbhandler
import gameid_info_crawler
from models import Team, Player, GameIDInfo, IDMapping

TIME_START = time.time()
TIME_COUNT = '0'


def get_time():
    return time.strftime("%H:%M:%S", time.localtime())


def time_count():
    global TIME_START
    global TIME_COUNT
    TIME_COUNT = time.time() - TIME_START
    TIME_START = time.time()
    return TIME_COUNT


# todo find and use a better way to log
if __name__ == '__main__':
    print('%s : crawler start' % get_time())
    print('get argument:', sys.argv)
    db_handler = dbhandler.DBHandler()
    if 'basic' in sys.argv:
        crawler = basic_data_crawler.BasicDataCrawler()
        print('%s: start to collect team and player pages' % get_time())
        crawler.collect_page()
        print('spent %s seconds to finish collect pages' % time_count())
        print('%s: start to craw team info' % get_time())
        team_info = crawler.crawl_team_info()
        print('spent %s seconds to finish craw team info' % time_count())
        print('%s: start to save team info to db' % get_time())
        db_handler.save_data(team_info, Team)
        print('spent %s seconds to save team info to db' % time_count())
        print('%s: start to craw team images' % get_time())
        crawler.crawl_team_img()
        print('spent %s seconds to finish craw team images' % time_count())
        print('%s: start to collect player data' % get_time())
        player_info = crawler.crawl_player_data()
        print('spent %s seconds to collect player data' % time_count())
        print('%s: start to save player info to db' % get_time())
        db_handler.save_data(player_info, Player)
        print('spent %s seconds to save player info to db' % time_count())
        crawler.close()
    if 'daily' in sys.argv:
        crawler = gameid_info_crawler.GameIDInfoCrawler()
        crawler.collect_page()
        gameid_data, id_mapping = crawler.crawl_gameid_info()
        db_handler.save_data(gameid_data, GameIDInfo)
        db_handler.save_data(id_mapping, IDMapping)
        db_handler.update_summary()
        crawler.close()
