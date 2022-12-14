import os
import sys
import pandas
sys.path.append(os.getcwd())

from src.utils import database as db_util
from flask import Flask, render_template

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def get_table_data(query):
    engine = db_util.get_engine('fantasy_mgr')
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


@app.route('/schools/')
def schools():
    query = 'select School,W from tbl_schools limit 20'
    df = get_table_data(query)
    return render_template('table_embed.html',
                           column_names=df.columns.values,
                           row_data=list(df.values.tolist()), zip=zip)


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)