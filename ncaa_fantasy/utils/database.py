import os
import sqlalchemy


def get_engine(database_name):
    engine = sqlalchemy.create_engine(f"mysql+pymysql://{os.getenv('db_user')}:{os.getenv('db_password')}@{os.getenv('db_host')}/{database_name}")
    return engine


def init_database(database_name):
    engine = get_engine(database_name=database_name)
    crate_ddl = "CREATE SCHEMA `fantasy_mgr` DEFAULT CHARACTER SET utf8 ;"
