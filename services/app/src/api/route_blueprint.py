import pandas
from flask import Blueprint
from flask import Flask, Response, jsonify, request, render_template

route_blueprint = Blueprint('route_blueprint', __name__)

# def get_table_data(query):
#     engine = db_util.get_engine()
#     df = pandas.read_sql_query(query, con=engine)
#     #count = int(df.iloc[0]['count'])
#     return df
#

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



# @route_blueprint.route('/roster/')
# def roster():
#     query = 'select * from vw_Roster where PPG > 2'
#     df = get_table_data(query)
#     return render_template('table_embed.html',
#                            column_names=df.columns.values,
#                            row_data=list(df.values.tolist()), zip=zip)


@route_blueprint.route('/bracket/')
def bracket():
    return render_template('bracket.html')


@route_blueprint.route('/scoreboard/')
def scoreboard():
    return render_template('scoreboard.html')


@route_blueprint.route('/teams/')
def teams():
    return render_template('teams.html')
