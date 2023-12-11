import pandas
from flask import Blueprint
from flask import Flask, Response, jsonify, request, render_template

from api import model
from api.transformations import populate_model as populate


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


@route_blueprint.route('/draft_night/')
def draft_night():
    return render_template('draft_night.html')


@route_blueprint.route('/player_search/')
def player_search():
    return render_template('player_search.html')


@route_blueprint.route('/bracket/')
def bracket():
    return render_template('bracket.html')


@route_blueprint.route('/leaderboard/')
def leaderboard():
    return render_template('leaderboard.html')


# @route_blueprint.route('/teams/')
# def teams():
#     engine = model.get_engine()
#     df = pandas.read_sql_query(f"select name, display_name, draft_order from tbl_fantasy_team", con=engine)
#     return render_template('teams.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
@route_blueprint.route('/teams/')
def teams():
    return render_template('teams.html')


@route_blueprint.route('/settings/')
def settings():
    return render_template('settings.html')


######################
##  POST Endpoints  ##
######################

@route_blueprint.route('/populate_model/', methods=['POST'])
def populate_model():
    # Add the code you want to execute on button push
    populate.run(engine=model.get_engine())
    return "Model populated"