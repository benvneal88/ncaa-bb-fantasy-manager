import pandas
from flask import Blueprint
from flask import Flask, Response, jsonify, request, render_template

from api.utils import database as db_util
from api.model.settings import APP_DATABASE_NAME

route_blueprint = Blueprint('route_blueprint', __name__)

def get_table_data(query):
    engine = db_util.get_engine(APP_DATABASE_NAME)
    df = pandas.read_sql_query(query, con=engine)
    #count = int(df.iloc[0]['count'])
    return df


@route_blueprint.route('/')
def home():
    return render_template('home.html')


@route_blueprint.route("/custom", methods=["POST"])
def custom():
    payload = request.get_json()

    if payload.get("say_hello") is True:
        output = jsonify({"message": "Hello!"})
    else:
        output = jsonify({"message": "..."})

    return output


@route_blueprint.route("/health")
def health():
    return Response("OK", status=200)



@route_blueprint.route('/roster/')
def roster():
    query = 'select * from vw_Roster where PPG > 2'
    df = get_table_data(query)
    return render_template('table_embed.html',
                           column_names=df.columns.values,
                           row_data=list(df.values.tolist()), zip=zip)


@route_blueprint.route('/about/')
def about():
    return render_template('about.html')
