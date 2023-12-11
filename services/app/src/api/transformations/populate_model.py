import os
import sys
import json
import pandas
import sqlalchemy

from api.utils import logger as log_util
from api import model
from api.transformations import sports_reference

LOGGER_NAME = 'populate_model'
LOG_LEVEL = 'INFO'

logger = log_util.get_logger(LOGGER_NAME, LOG_LEVEL)


######
# Helper Functions
######
def truncate_table(engine, table_name):
    message = f'deleting all rows from table {table_name}'
    logger.info(message)
    # delete target table
    inspect = sqlalchemy.inspect(engine, table_name)
    if inspect.has_table(table_name, schema="ncaa_fantasy"):
        with engine.connect() as connection:
            connection.execute(f"delete from {table_name} where 1=1")


def seed_draft_events(engine):
    ## UNTESTED
    with open('api/config/seed_draft_events.json', 'r') as f:
        draft_events = json.load(f)

    fantasy_teams_df = pandas.read_sql_query(f"select id, name from tbl_fantasy_team", con=engine)
    player_df = pandas.read_sql_query(f"select id, name from tbl_player", con=engine)

    count = 1

    for draft_event in draft_events:
        fantasy_team_id = None
        player_id = None

        player_name = draft_event.get('player_name')
        fantasy_team_name = draft_event.get('fantasy_team_name')

        try:
            fantasy_team_id = fantasy_teams_df[fantasy_teams_df['name'] == fantasy_team_name].iloc[0]['id']
        except Exception as e:
            logger.error(f"Unable to find fantasy team name {fantasy_team_name}")

        try:
            player_id = player_df[player_df['name'] == player_name].iloc[0]['id']
        except Exception as e:
            logger.error(f"Unable to find player with name {player_name}")

        if player_id and fantasy_team_id:
            update_sql = f"update tbl_player set drafted_number = {count}, fk_fantasy_team_id = {fantasy_team_id} where id = {player_id}"
            with engine.connect() as connection:
                connection.execute(update_sql)

            logger.info(f"with the {count} pick, the team {fantasy_team_name} picks player {player_name}")
            count = + 1


def get_tournament_teams():
    with open('api/config/tournament_teams.json', 'r') as f:
        config = json.load(f)
    return config


######
# Table Inserting Functions
######
def tbl_ball_team(engine):
    table_name = 'tbl_ball_team'
    logger.info(f"Starting '{table_name}' population")
    config = get_tournament_teams()

    insert_df = pandas.DataFrame(columns=['name', 'region', 'seed'])

    for name, value_dict in config.items():
        data_dict = {
            'name': [name],
            'name_short': [name],
            'region': [value_dict.get('region')],
            'seed': [value_dict.get('seed')],
        }
        df = pandas.DataFrame(data=data_dict)
        insert_df = pandas.concat([insert_df, df])

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}...')
    logger.debug(insert_df)
    insert_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def tbl_player(engine):
    """
    For each team in tbl_team, fetch the roster from stg_sportsref_roster

    :param engine:
    :return:
    """
    table_name = 'tbl_player'
    logger.info(f"Starting '{table_name}' population")
    insert_df = pandas.read_sql_query(f'select id, name from tbl_ball_team', con=engine)

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}...')
    logger.debug(insert_df)

    for index, row in insert_df.iterrows():
        insert_query = f"INSERT INTO {table_name} (first_name, last_name, ppg, fk_ball_team_id) SELECT `First Name`,`Last Name`, CAST(PPG as FLOAT), {row['id']} FROM stg_sportsref_roster where School = '{row['name']}'"
        with engine.connect() as connection:
            connection.execute(insert_query)


def tbl_user(engine):
    table_name = 'tbl_user'
    logger.info(f"Starting '{table_name}' population")

    with open('api/config/users.json', 'r') as f:
        config = json.load(f)

    insert_df = pandas.DataFrame(columns=['email', 'user_name', 'first_name', 'last_name', 'is_active'])

    for name, value_dict in config.items():
        data_dict = {
            'email': [name],
            'user_name': [name],
            'first_name': [value_dict.get('first_name')],
            'last_name': [value_dict.get('last_name')],
            'is_active': [value_dict.get('is_active')],
        }
        df = pandas.DataFrame(data=data_dict)
        insert_df = pandas.concat([insert_df, df])

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}...')
    logger.debug(insert_df)
    insert_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def tbl_fantasy_team(engine):
    table_name = 'tbl_fantasy_team'
    logger.info(f"Starting '{table_name}' population")

    with open('api/config/fantasy_teams.json', 'r') as f:
        config = json.load(f)

    insert_df = pandas.DataFrame(columns=['name', 'display_name', 'draft_order'])

    for name, value_dict in config.items():
        data_dict = {
            'name': [name],
            'display_name': [value_dict.get('display_name')],
            'draft_order': [value_dict.get('draft_order')],
        }
        df = pandas.DataFrame(data=data_dict)
        # logger.info(df)
        insert_df = pandas.concat([insert_df, df])

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}...')
    logger.debug(insert_df)
    insert_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def tbl_fantasy_team_user_mtm(engine):
    """
    For each user in tbl_user fetch the team ownership config and create MTM records linking tbl_fantasy_team
    :param engine:
    :return:
    """
    table_name = 'tbl_fantasy_team_user_mtm'
    logger.info(f"Starting '{table_name}' population")

    with open('api/config/users.json', 'r') as f:
        config = json.load(f)

    insert_df = pandas.DataFrame(columns=['fk_fantasy_team_id', 'fk_user_id'])

    user_df = pandas.read_sql_query(f"select id, email from tbl_user", con=engine)
    fantasy_teams_df = pandas.read_sql_query(f"select id, name from tbl_fantasy_team", con=engine)

    # for each user in tbl_user
    for index, row in user_df.iterrows():

        user_id = row['id']
        email = row['email']

        # fetch team ownership config
        this_user_config = config.get(email, None)
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
                    # logger.info(df)
                    insert_df = pandas.concat([insert_df, df])

        else:
            logger.error(f"Failed to find player by the name of {this_user_config} in users.json")

    logger.info(f'inserting {len(insert_df)} rows into table {table_name}...')
    logger.debug(insert_df)
    insert_df.to_sql(table_name, con=engine, if_exists='append', index=False)


def populate_table(engine, table_name):
    table_name(engine=engine)


def refresh_players_stats(engine):

    refresh_schools = get_tournament_teams().keys()

    model.write_to_console_logs(engine, "Fetching and Updating player stats...")
    truncate_table(engine, "tbl_player")
    truncate_table(engine, "tbl_ball_team")
    sports_reference.insert_stg_schools(engine)
    sports_reference.insert_stg_roster(engine, refresh_schools)
    populate_table(engine, tbl_ball_team)
    populate_table(engine, tbl_player)
    model.write_to_console_logs(engine, "...completed")


def refresh_users_configuration(engine):
    model.write_to_console_logs(engine, "Refreshing Users configuration...")
    truncate_table(engine, "tbl_fantasy_team_user_mtm")
    truncate_table(engine, "tbl_user")
    truncate_table(engine, "tbl_fantasy_team")
    populate_table(engine, tbl_user)
    populate_table(engine, tbl_fantasy_team)
    populate_table(engine, tbl_fantasy_team_user_mtm)
    model.write_to_console_logs(engine, "...completed")


def run(engine):
    model.init_database()
    refresh_players_stats(engine)
    refresh_users_configuration(engine)


if __name__ == '__main__':
    e = model.get_engine()
    run(e)