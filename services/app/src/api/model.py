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
STAGING_DATABASE_NAME = 'staging'


db = SQLAlchemy()

metadata_obj = MetaData()


def get_engine(database_name=APP_DATABASE_NAME):
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{os.getenv('db_user')}:{os.getenv('db_password')}@{os.getenv('db_host')}/{database_name}")
    return engine


def init_database(engine=get_engine(), db: SQLAlchemy() = metadata_obj):
    validate_database()
    db.create_all(bind=engine)


def validate_database():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info("New Database Created: " + database_exists(engine.url))
    else:
        logger.info("Database Already Exists")


def write_to_console_logs(engine, message):
    df = pandas.DataFrame(columns=["message"]).from_records([{"message": message, "timestamp": datetime.utcnow()}])
    df.to_sql(con=engine, name="console_logs", index=False, if_exists="append")


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
    Column("ppg", Numeric(6,2)),
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

