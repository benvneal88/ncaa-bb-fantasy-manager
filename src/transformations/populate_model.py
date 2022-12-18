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

    for name, value_dict in config.items():
        data_dict = {
            'name': [name],
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


def tbl_user(engine):
    table_name = 'tbl_user'
    with open('src/config/users.json', 'r') as f:
        config = json.load(f)

    insert_df = pandas.DataFrame(columns=['name', 'email', 'is_active'])

    for name, value_dict in config.items():
        data_dict = {
            'name': [name],
            'email': [value_dict.get('email')],
            'is_active': [value_dict.get('is_active')],
        }
        df = pandas.DataFrame(data=data_dict)
        # print(df)
        insert_df = pandas.concat([insert_df, df])

    print(insert_df)
    truncate_table(engine, table_name)

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}')
    insert_df.to_sql(table_name, con=e, if_exists='append', index=False)


def tbl_fantasy_team(engine):
    table_name = 'tbl_fantasy_team'
    with open('src/config/fantasy_teams.json', 'r') as f:
        config = json.load(f)

    user_df = pandas.read_sql_query(f"select id, name from tbl_user", con=e)

    insert_df = pandas.DataFrame(columns=['name', 'display_name', 'draft_order'])

    for name, value_dict in config.items():
        owner_user_id = user_df[user_df['name'] == value_dict.get('owner')].loc[0]['id']
        if owner_user_id:
            data_dict = {
                'name': [name],
                'display_name': [value_dict.get('display_name')],
                'draft_order': [value_dict.get('draft_order')],
                'fk_user_id': [owner_user_id],
            }
            df = pandas.DataFrame(data=data_dict)
            # print(df)
            insert_df = pandas.concat([insert_df, df])
        else:
            logger.error(f"Failed to find user owner for team {name}")

    print(insert_df)
    truncate_table(engine, table_name)

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}')
    insert_df.to_sql(table_name, con=e, if_exists='append', index=False)


def populate_model(engine, table_name):
    table_name(engine=engine)


if __name__ == '__main__':
    e = db_util.get_engine(DATABASE_NAME)
    #populate_model(e, tbl_ball_team)
    #populate_model(e, tbl_player)
    #populate_model(e, tbl_user)
    populate_model(e, tbl_fantasy_team)
