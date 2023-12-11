import pandas
import pandas as pd
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
    e = model.get_engine()
    players = pd.read_sql_query("""
        select t.name as ball_team_name, p.first_name, p.last_name, p.ppg
        from tbl_player p
            inner join tbl_ball_team t on p.fk_ball_team_id = t.id
        """
    , con=e).to_dict("records")
    #print(players)
    return render_template('player_search.html', players=players)


@route_blueprint.route('/bracket/')
def bracket():
    return render_template('bracket.html')


@route_blueprint.route('/leaderboard/')
def leaderboard():
    return render_template('leaderboard.html')


@route_blueprint.route('/teams/')
def teams():
    return render_template('teams.html')


@route_blueprint.route('/settings/')
def settings():
    e = model.get_engine()
    messages = pd.read_sql_query("""
        select timestamp, message from console_logs order by timestamp desc
        """
        , con=e).to_dict("records")
    return render_template('settings.html', messages=messages)


######################
##  POST Endpoints  ##
######################

@route_blueprint.route('/refresh_player_stats/', methods=['POST'])
def refresh_player_stats():
    # Add the code you want to execute on button push
    populate.refresh_players_stats(engine=model.get_engine())
    return "Model populated"


@route_blueprint.route('/refresh_users_configuration/', methods=['POST'])
def refresh_users_configuration():
    # Add the code you want to execute on button push
    populate.refresh_users_configuration(engine=model.get_engine())
    return "Model populated"