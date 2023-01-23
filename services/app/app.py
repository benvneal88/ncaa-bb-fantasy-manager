import os
import pandas
import time
from flask import Flask, render_template
from dotenv import load_dotenv

from src.utils import database as db_util
from src.model.settings import APP_DATABASE_NAME
from src.utils import logger as log_util

load_dotenv()

logger = log_util.get_logger(__name__, 'INFO')

#HOST = "127.0.0.1" # for local development
HOST = "0.0.0.0" # for docker deployment
app = Flask(__name__)


def get_table_data(query):
    engine = db_util.get_engine(APP_DATABASE_NAME)
    df = pandas.read_sql_query(query, con=engine)
    #count = int(df.iloc[0]['count'])
    return df
#
# @app.route("/")
# def hello_world():
#     count = 0
#     try:
#         count = get_detail()
#     except Exception as e:
#         print(e)
#
#     return f"<p>Hello, World! {count}</p>"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/roster/')
def roster():
    query = 'select * from vw_Roster where PPG > 2'
    df = get_table_data(query)
    return render_template('table_embed.html',
                           column_names=df.columns.values,
                           row_data=list(df.values.tolist()), zip=zip)


@app.route('/about/')
def about():
    return render_template('about.html')



# def create_app():
#
#     #db_util.init_database(APP_DATABASE_NAME)
#     #app.run(host='0.0.0.0', debug=True)
#     #app.run()

def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])



#
# if __name__ == '__main__':
#     # wait for database service to startup
#     time.sleep(5)
#     db_util.init_database(APP_DATABASE_NAME)
#     app.run(host='0.0.0.0', debug=True)