import pandas
import os
import sys
import json
import pandas
sys.path.append(os.getcwd())
from src.utils import database as db_util
from src.utils import logger as log_util
from src.config.constants import DATABASE_NAME

LOGGER_NAME = 'populdate_model'
LOG_LEVEL = 'INFO'

logger = log_util.get_logger(LOGGER_NAME, LOG_LEVEL)


def truncate_table(engine, table_name):
    logger.info(f'deleting all rows from table {table_name}')
    # delete target table
    with engine.connect() as connection:
        connection.execute(f"delete from {table_name} where 1=1")


def tbl_ball_team(engine):
    table_name = 'tbl_ball_team'
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
    truncate_table(engine, table_name)

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}')
    insert_df.to_sql(table_name, con=e, if_exists='append', index=False)


def tbl_player(engine):
    """
    For each team in tbl_team, fetch the roster from stg_sportsref_roster

    :param engine:
    :return:
    """

    table_name = 'tbl_ball_team'
    ball_teams_df = pandas.read_sql_query(f'select id, name from {table_name}', con=e)
    truncate_table(engine, 'tbl_player')
    for index, row in ball_teams_df.iterrows():
        insert_query = f"INSERT INTO tbl_player (first_name, last_name, ppg, fk_ball_team_id) SELECT `First Name`,`Last Name`, CAST(PPG as FLOAT), {row['id']} FROM stg_sportsref_roster where School = '{row['name']}'"
        print(insert_query)
        with engine.connect() as connection:
            connection.execute(insert_query)


def populate_model(engine, table_name):
    table_name(engine=engine)


if __name__ == '__main__':
    e = db_util.get_engine(DATABASE_NAME)
    populate_model(e, tbl_ball_team)
    populate_model(e, tbl_player)
