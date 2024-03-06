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
    players = pd.read_sql_query(
        """select t.name as ball_team_name, t.seed, t.region, CONCAT(p.first_name, ' ', p.last_name) as name, p.ppg
        from tbl_player p
            inner join tbl_ball_team t on p.fk_ball_team_id = t.id
        """,
        con=e
    ).to_dict("records")
    #print(players)
    return render_template('player_search.html', players=players)


@route_blueprint.route('/player_stats/')
def player_stats():
    e = model.get_engine()
    player_stats_df = pd.read_sql_query("""select tbl.seed, tbl.region, tbl.title, GROUP_CONCAT(tbl.name ORDER BY tbl.ppg desc) AS name_list, GROUP_CONCAT(tbl.ppg ORDER BY tbl.ppg desc) AS ppg_list
    from (
        select
            t.seed,
            t.region,
            CONCAT(t.seed, ' - ', t.region, ' - ', t.name) as title,
            CONCAT(p.first_name, ' ', p.last_name) as name,
            ROUND(p.ppg, 1) as ppg
        from tbl_player p
            inner join tbl_ball_team t on p.fk_ball_team_id = t.id
        where p.ppg > 3
        order by t.name desc
    ) tbl
    group by 1,2,3""",
        con=e
    )

    #
    # player_stats_df = pd.read_sql_query("""select seed, GROUP_CONCAT(title ORDER BY region desc) as titles, json_arrayagg(name_list) as name_list, json_arrayagg(ppg_list) as ppg_list
    # from (
    # 	select tbl.seed, tbl.region, tbl.title, GROUP_CONCAT(tbl.name ORDER BY tbl.ppg desc) AS name_list, GROUP_CONCAT(tbl.ppg ORDER BY tbl.ppg desc) AS ppg_list
    # 	from (
    # 		select
    # 			t.seed,
    # 			t.region,
    # 			CONCAT(t.seed, ' - ', t.region, ' - ', t.name) as title,
    # 			CONCAT(p.first_name, ' ', p.last_name) as name,
    # 			ROUND(p.ppg, 1) as ppg
    # 		from tbl_player p
    # 			inner join tbl_ball_team t on p.fk_ball_team_id = t.id
    # 		where p.ppg > 3
    # 		order by t.name desc
    # 	) tbl
    # 	group by 1,2,3
    # ) tbl2
    # group by 1""", con=e)

    import pdb;
    # def zip_lists(row):
    #     zipped_list = []
    #     for item in list(zip(row['name_list'], row['ppg_list'])):
    #         pdb.set_trace()
    #         names = item[0].split(',')
    #         ppgs = item[1].split(',')
    #         nested_list = list(zip(names, ppgs))
    #         zipped_list.append(nested_list)
    #         pdb.set_trace()
    #         #print(zipped_list)
    #     return zipped_list

    def zip_lists(row):
        names = row["name_list"].split(',')
        ppgs = row["ppg_list"].split(',')
        zipped_list = list(zip(names, ppgs))
        #print(zipped_list)
        return zipped_list

    #player_stats_df["titles"] = player_stats_df.apply(lambda x: x['titles'].split(','), axis=1)
    player_stats_df["data"] = player_stats_df.apply(zip_lists, axis=1)
    player_stats_df = player_stats_df.drop(['name_list', 'ppg_list'], axis=1)
    player_stats_list = player_stats_df.to_dict("records")
    print(player_stats_list)

    return render_template('player_stats.html', player_stats_list=player_stats_list)

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


####################
#  POST Endpoints  #
####################

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