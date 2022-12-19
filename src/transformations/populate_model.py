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

######
# Helper Function
######
def truncate_table(engine, table_name):
    logger.info(f'deleting all rows from table {table_name}')
    # delete target table
    with engine.connect() as connection:
        connection.execute(f"delete from {table_name} where 1=1")


def create_table(engine, table_name):
    # UNTESTED
    with open(f'src/model/schema/{table_name}.sql', 'r') as file:
        create_table_ddl = file.read()

    with engine.connect() as connection:
        connection.execute(create_table_ddl)


######
# Table Inserting Functions
######
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
    insert_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def tbl_fantasy_team(engine):
    table_name = 'tbl_fantasy_team'
    with open('src/config/fantasy_teams.json', 'r') as f:
        config = json.load(f)

    insert_df = pandas.DataFrame(columns=['name', 'display_name', 'draft_order'])

    for name, value_dict in config.items():
        data_dict = {
            'name': [name],
            'display_name': [value_dict.get('display_name')],
            'draft_order': [value_dict.get('draft_order')],
        }
        df = pandas.DataFrame(data=data_dict)
        # print(df)
        insert_df = pandas.concat([insert_df, df])

    print(insert_df)
    truncate_table(engine, table_name)

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}')
    insert_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def tbl_fantasy_team_user_mtm(engine):
    """
    For each user in tbl_user fetch the team ownership config and create MTM records linking tbl_fantasy_team
    :param engine:
    :return:
    """
    table_name = 'tbl_fantasy_team_user_mtm'

    with open('src/config/users.json', 'r') as f:
        config = json.load(f)

    insert_df = pandas.DataFrame(columns=['fk_fantasy_team_id', 'fk_user_id'])

    user_df = pandas.read_sql_query(f"select id, name from tbl_user", con=engine)
    fantasy_teams_df = pandas.read_sql_query(f"select id, name from tbl_fantasy_team", con=engine)

    # for each user in tbl_user
    for index, row in user_df.iterrows():

        user_id = row['id']
        user_name = row['name']

        # fetch team ownership config
        this_user_config = config.get(user_name, None)
        if this_user_config:
            fantasy_team_ownership = this_user_config.get("team_ownership")
            for fantasy_team_name in fantasy_team_ownership:
                fantasy_team_id = None;
                try:
                   # import pdb; pdb.set_trace()
                    fantasy_team_id = fantasy_teams_df[fantasy_teams_df['name'] == fantasy_team_name].iloc[0]['id']
                except Exception as e:
                    logger.exception(e)
                    logger.error(f"Failed to find fantasy team by name of {fantasy_team_name}")

                if fantasy_team_id:
                    data_dict = {
                        'fk_fantasy_team_id': [fantasy_team_id],
                        'fk_user_id': [user_id],
                    }
                    df = pandas.DataFrame(data=data_dict)
                    # print(df)
                    insert_df = pandas.concat([insert_df, df])

        else:
            logger.error(f"Failed to find player by the name of {this_user_config} in users.json")

    print(insert_df)
    truncate_table(engine, table_name)

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}')
    insert_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def populate_model(engine, table_name):
    table_name(engine=engine)


def create_schema(engine):
    # UNTESTED
    create_tables = [
        'tbl_user',
        'tbl_ball_team',
        'tbl_fantasy_team',
        'tbl_fantasy_team_user_mtm',
    ]

    for table_name in create_tables:
        create_table(engine, table_name)


if __name__ == '__main__':
    e = db_util.get_engine(DATABASE_NAME)
    #populate_model(e, tbl_ball_team)
    #populate_model(e, tbl_player)
    #populate_model(e, tbl_user)
    #populate_model(e, tbl_fantasy_team)
    #populate_model(e, tbl_fantasy_team_user_mtm)