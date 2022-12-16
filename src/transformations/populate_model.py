import pandas
import os
import sys
import json
import pandas
sys.path.append(os.getcwd())
from src.utils import database as db_util
from src.config.constants import DATABASE_NAME


def tbl_ball_team(engine):
    with open('src/config/tournament_teams.json', 'r') as f:
        config = json.load(f)

    insert_df = pandas.DataFrame(columns=['name', 'region', 'seed'])

    for ball_team_name, value_dict in config.items():
        data_dict = {
            'name': [ball_team_name],
            'region': [value_dict.get('region')],
            'seed': [value_dict.get('seed')],
        }
        df = pandas.DataFrame(data=data_dict)
        # print(df)
        insert_df = pandas.concat([insert_df, df])

    print(insert_df)

    # delete target table
    with engine.connect() as connection:
        connection.execute(f"delete from tbl_ball_team where 1=1")

    insert_df.to_sql('tbl_ball_team', con=e, if_exists='append', index=False)


def populate_model(engine, table_name):
    table_name(engine=engine)







if __name__ == '__main__':
    e = db_util.get_engine(DATABASE_NAME)
    populate_model(e, tbl_ball_team)
