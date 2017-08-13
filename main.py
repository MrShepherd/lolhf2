import sys
import time

import basic_data_crawler
import dbhandler
from models import Team, Player

TIME_START = '0'
TIME_COUNT = '0'


def str_time():
    return str(time.time())


def time_count():
    global TIME_START
    global TIME_COUNT
    TIME_COUNT = str_time() - TIME_START
    TIME_START = str_time()
    return TIME_COUNT

# todo find and use a better way to log
if __name__ == '__main__':
    print('%s : crawler start' % str_time())
    print('get argument:', sys.argv)
    db_handler = dbhandler.DBHandler()
    if 'basic' in sys.argv:
        crawler = basic_data_crawler.BasicDataCrawler()
        print('%s: start to collect team and player pages' % str_time())
        crawler.collect_page()
        print('spent %s seconds to finish collect pages' % time_count())
        print('%s: start to craw team info' % str_time())
        team_info = crawler.craw_team_info()
        print('spent %s seconds to finish craw team info' % time_count())
        print('%s: start to save team info to db' % str_time())
        db_handler.save_data(team_info, Team)
        print('spent %s seconds to save team info to db' % time_count())
        print('%s: start to craw team images' % str_time())
        crawler.craw_team_img()
        print('spent %s seconds to finish craw team images' % time_count())
        print('%s: start to collect player data' % str_time())
        player_info = crawler.craw_player_data()
        print('spent %s seconds to collect player data' % time_count())
        print('%s: start to save player info to db' % str_time())
        db_handler.save_data(player_info, Player)
        print('spent %s seconds to save player info to db' % time_count())
        crawler.close()
