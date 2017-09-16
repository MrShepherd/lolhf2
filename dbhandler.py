import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Summary, IDMappingManual
from collections import namedtuple


class DBHandler(object):
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://lolhfdev2:lolhfdev2@localhost:3306/lolhfdev2')
        self.DBSession = sessionmaker(bind=self.engine)

    def initial_table(self, table_model):
        session = self.DBSession()
        session.query(table_model).delete()
        session.commit()
        session.close()

    def save_data(self, data_list, table_model):
        self.initial_table(table_model)
        all_data = [table_model(**data) for data in data_list]
        # for item in all_data:
        #     print(item.player_name, '=>', item.game_id)
        try:
            session = self.DBSession()
            session.add_all(all_data)
            # session.bulk_save_objects(all_data)
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            # for item in all_data:
            #     try:
            #         session = self.DBSession()
            #         session.add(item)
            #         session.commit()
            #         session.close()
            #     except Exception as e:
            #         print(e)

    def get_idmappingmanual_gameid(self):
        session = self.DBSession()
        gameids = session.query(IDMappingManual.game_id).filter(IDMappingManual.enable == 1).all()
        tmplist = []
        for gameid in gameids:
            tmplist.append(gameid[0])
        session.close()
        return tmplist

    def update_summary(self):
        self.initial_table(Summary)
        time.sleep(10)
        session = self.DBSession()
        sql = '''
        insert into summary
        select distinct
        COALESCE(c.player_name,'路人') as 'player_name'
        ,COALESCE(c.player_country,'unknown') as 'player_country'
        ,COALESCE(c.player_team_short_name,'路人') as 'player_team_short_name'
        ,COALESCE(c.player_team_league,'路人') as 'player_team_league'
        ,COALESCE(c.player_place,'路人') as 'player_place'
        ,a.*
        from gameidinfo a
        left JOIN
        (
        select game_id,player_name
        from idmapping
        where game_id not in
        (select game_id from idmappingmanual)
        UNION
        select game_id,player_name
        from idmappingmanual
        ) b
        on a.game_id=b.game_id
        left join
        (
        select *
        from player
        where player_name not in (select player_name from player group by player_name having count(*)>1)
        UNION
        select * from playermanual
        ) c
        ON b.player_name=c.player_name
        '''
        session.execute(sql)
        session.commit()
        sql = '''update summary set player_team_short_name='' WHERE player_team_short_name='路人';'''
        session.execute(sql)
        session.commit()
        sql = '''update summary set player_country='' where player_country='unknown';'''
        session.execute(sql)
        session.commit()
        print('update summary')
        session.close()
