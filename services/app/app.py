import pandas

from ncaa_fantasy.utils import database as db_util
from ncaa_fantasy.model.settings import APP_DATABASE_NAME
from flask import Flask, render_template

from dotenv import load_dotenv
load_dotenv()

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


if __name__ == '__main__':
    app.run(host=HOST, debug=True)