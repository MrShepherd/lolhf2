import sys
import time

import basic_data_crawler
import dbhandler
import gameid_info_crawler
from models import Team, Player, IDMapping, GameIDInfo

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
        print('%s: start to crawl idmapping info' % get_time())
        idmapping_data = crawler.crawl_idmapping_info()
        print('spent %s seconds to crawl idmapping info' % time_count())
        print('%s: start to save idmapping info to db' % get_time())
        db_handler.save_data(idmapping_data, IDMapping)
        print('spent %s seconds to save idmapping info to db' % time_count())
        print('%s: start to crawl gameid info' % get_time())
        gameid_info = crawler.crawl_gameid_info()
        print('spent %s seconds to crawl gameid info' % time_count())
        print('%s: start to save gameid info to db' % get_time())
        db_handler.save_data(gameid_info, GameIDInfo)
        print('spent %s seconds to save gameid info to db' % time_count())
        print('%s: start to update summary data' % get_time())
        db_handler.update_summary()
        print('spent %s seconds to update summary data' % time_count())
        crawler.close()
