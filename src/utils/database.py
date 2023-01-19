import os
import sqlalchemy
from src.utils import logger as log_util

logger = log_util.get_logger(__name__, 'INFO')


def get_engine(database_name):
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{os.getenv('db_user')}:{os.getenv('db_password')}@{os.getenv('db_host')}/{database_name}")
    return engine


def init_database(database_name):
    engine = get_engine(database_name=database_name)

    create_tables = [
        "tbl_user",
        "tbl_ball_team",
        "tbl_fantasy_team",
        "tbl_fantasy_team_user_mtm",
        "tbl_player",
        "tbl_draft_event",
        "tbl_game",
        "tbl_box_score_line_item"
    ]

    create_views = [
        "vw_roster",
        "vw_team_ownership"
    ]

    for table in create_tables:

        with open(f"{os.getcwd()}/src/model/schema/{table}.sql", 'r') as file:
            ddl = file.read()

        logger.info(f'Creating table {table}')

        with engine.connect() as conn:
            try:
                conn.execute(ddl)
            except Exception as e:
                logger.error(e)
                logger.info(f"Failed to create table {table}")

    for view in create_views:

        with open(f"{os.getcwd()}/src/model/view/{view}.sql", 'r') as file:
            ddl = file.read()

        logger.info(f'Creating view {table}')
        with engine.connect() as conn:
            conn.execute(ddl)
