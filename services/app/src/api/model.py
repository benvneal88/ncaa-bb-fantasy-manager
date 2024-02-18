import os
from datetime import datetime

import pandas
from sqlalchemy import MetaData, ForeignKey, Date, DateTime, Table, Column, Integer, String, Numeric, Boolean, Identity, UniqueConstraint
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database
from sqlalchemy_utils.functions import database_exists
import api.utils.logger as log_util

logger = log_util.get_logger(__name__, 'INFO')

APP_DATABASE_NAME = 'ncaa_fantasy'
db = SQLAlchemy()

def get_model_constants(data_source=None):
    vars = {
        "stg_schools_table_name": 'stg_sportsref_schools',
        "stg_roster_table_name": 'stg_sportsref_roster',
        "root_data_path": os.path.join(os.getcwd(), "api", "data", data_source),
    }
    return vars


def get_model_metadata():
    metadata_obj = MetaData()

    console_logs = Table(
        "console_logs",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("timestamp", DateTime, nullable=False),
        Column("message", String(1024), nullable=True),
    )

    tbl_ball_team = Table(
        "tbl_ball_team",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("name", String(255), nullable=False),
        Column("name_short", String(60), nullable=False),
        Column("region", String(32)),
        Column("seed", Integer),
        UniqueConstraint("name", "name_short", name="uc_name"),
    )

    tbl_game = Table(
        "tbl_game",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("fk_ball_team_id_home", Integer, ForeignKey("tbl_ball_team.id"), nullable=False),
        Column("fk_ball_team_id_away", Integer, ForeignKey("tbl_ball_team.id"), nullable=False),
        Column("name", String(255)),
        Column("event_date", Date),
        Column("event_start", DateTime),
        Column("event_end", DateTime),
        Column("tournament_round", Integer),
        Column("created_date", DateTime, default=datetime.utcnow),
        Column("updated_date", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
        UniqueConstraint("fk_ball_team_id_home", "fk_ball_team_id_away", name="uc_teams"),
    )

    tbl_fantasy_team = Table(
        "tbl_fantasy_team",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("name", String(80), unique=True),
        Column("display_name", String(80)),
        Column("draft_order", Integer),
    )

    tbl_player = Table(
        "tbl_player",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("fk_ball_team_id", Integer, ForeignKey("tbl_ball_team.id")),
        Column("fk_fantasy_team_id", Integer, ForeignKey("tbl_fantasy_team.id")),
        Column("first_name", String(80)),
        Column("last_name", String(80), nullable=False),
        Column("drafted_round", Integer),
        Column("drafted_number", Integer),
        Column("drafted_datetime", Integer),
        Column("ppg", Numeric(6, 2)),
        UniqueConstraint("first_name", "last_name", "fk_ball_team_id", name="uc_player"),
    )

    tbl_box_score_line_item = Table(
        "tbl_box_score_line_item",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("fk_game_id", Integer, ForeignKey("tbl_game.id"), nullable=False),
        Column("fk_player_id", Integer, ForeignKey("tbl_player.id"), nullable=False),
        Column("points", Integer),
        Column("created_date", DateTime, default=datetime.utcnow),
        Column("updated_date", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
        UniqueConstraint("fk_game_id", "fk_player_id", name="uc_name"),
    )

    tbl_user = Table(
        "tbl_user",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("first_name", String(80), nullable=False),
        Column("last_name", String(80), nullable=False),
        Column("user_name", String(80), nullable=False, unique=True),
        Column("email", String(80), nullable=False),
        Column("is_active", Boolean, nullable=False, default=True),
        Column("created_date", DateTime, default=datetime.utcnow),
        Column("updated_date", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    )

    tbl_fantasy_team_user_mtm = Table(
        "tbl_fantasy_team_user_mtm",
        metadata_obj,
        Column("id", Integer, Identity(start=0, cycle=True), primary_key=True),
        Column("fk_fantasy_team_id", Integer, ForeignKey("tbl_fantasy_team.id"), nullable=False),
        Column("fk_user_id", Integer, ForeignKey("tbl_user.id"), nullable=False),
    )

    return metadata_obj


def get_engine(database_name=APP_DATABASE_NAME):
    db_user = os.getenv('db_user')
    db_host = os.getenv('db_host')

    if db_host is None:
        raise Exception(f"Database host not provided from environment variable 'db_host'")

    if db_user is None:
        raise Exception(f"Database user not provided from environment variable 'db_user'")

    engine = sqlalchemy.create_engine(f"mysql+pymysql://{db_user}:{os.getenv('db_password')}@{db_host}/{database_name}")
    return engine


def init_database(engine=None):
    db_meta = get_model_metadata()
    initialize_database()
    logger.info(f"Creating tables...")
    db_meta.create_all(bind=engine)
    logger.info(f"Created tables")


def delete_table(engine, table_name):
    logger.info(f'Deleting table {table_name}')
    # delete target table
    with engine.connect() as connection:
        connection.execute(f"drop table if exists {table_name}")


def initialize_database():
    engine = get_engine()
    logger.info(f"Creating databases as needed")
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info("Database created: " + database_exists(engine.url))
    else:
        logger.info(f"Database {engine.url.database} already exists")


def write_to_console_logs(engine, logger,  message=None):
    logger.info(message)
    df = pandas.DataFrame(columns=["message"]).from_records([{"message": message, "timestamp": datetime.utcnow()}])
    df.to_sql(con=engine, name="console_logs", index=False, if_exists="append")


