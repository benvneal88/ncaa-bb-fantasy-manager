import pandas
import pandas as pd
from flask import Blueprint
from flask import Flask, Response, jsonify, request, render_template

from api import model
from api.transformations import populate_model as populate
import api.commons as commons

route_blueprint = Blueprint('route_blueprint', __name__)

# def get_table_data(query):
#     engine = db_util.get_engine()
#     df = pandas.read_sql_query(query, con=engine)
#     #count = int(df.iloc[0]['count'])
#     return df
#


def get_player_stats(region, seed):
    e = model.get_engine()
    df = pd.read_sql_query(f"""
        select
            t.name as team_name,
            CONCAT(p.first_name, ' ', p.last_name) as name,
            ROUND(p.ppg, 1) as ppg,
            CONCAT('{commons.BACKEND_API_URL}/draft_player/', p.id) as draft_player,
            CASE WHEN drafted_round IS NULL THEN FALSE ELSE TRUE END as is_drafted
        from tbl_player p
            inner join tbl_ball_team t on p.fk_ball_team_id = t.id
        where 
            t.seed = {seed}
            and LOWER(region) = '{region.lower()}'
            and p.ppg > 3
        order by t.name desc""",
        con=e
    )
    #df.loc[df['is_drafted'] == 0, 'is_drafted'] = '🪖'
    #df.loc[df['is_drafted'] == 0, 'is_drafted'] = 'google.com'
    #df.loc[df['is_drafted'] == 1, 'is_drafted'] = '💼'

    return df


def get_team(team_name):
    e = model.get_engine()
    df = pd.read_sql_query(f"""
        select
            CONCAT(p.first_name, ' ', p.last_name) as name,
            ROUND(p.ppg, 1) as ppg,
            CASE WHEN drafted_round IS NULL THEN 0 ELSE 1 END as is_drafted
        from tbl_player p
            inner join tbl_ball_team t on p.fk_ball_team_id = t.id
        where 
            LOWER(t.name) = '{team_name.lower()}'
            AND p.ppg > 3""",
        con=e
    )
    return df


def get_teams():
    e = model.get_engine()
    df = pd.read_sql_query(f"""
        select
            name as team_name
        FROM tbl_ball_team order by seed asc""",
        con=e
    )
    return df


def update_draft_player(player_id):
    e = model.get_engine()
    r = e.engine.execute(f"UPDATE tbl_player set drafted_round = 1 where id = {player_id}")


@route_blueprint.route('/api/v1/teams/')
def teams():
    df = get_teams()
    return df.to_dict("records")


@route_blueprint.route('/api/v1/team/<string:team_name>')
def team(team_name):
    df = get_team(team_name)
    return df.to_dict("records")


@route_blueprint.route('/api/v1/players')
def players():
    e = model.get_engine()
    df = pd.read_sql_query(
        """select 
            t.name as team, 
            t.seed as seed, 
            t.region as region, 
            CONCAT(p.first_name, ' ', p.last_name) as name, 
            p.ppg as ppg,
            CASE WHEN drafted_round IS NULL THEN FALSE ELSE TRUE END as is_drafted
        from tbl_player p
            inner join tbl_ball_team t on p.fk_ball_team_id = t.id
        """,
        con=e
    )
    print(df)
    df = df.to_dict("records")
    return df


@route_blueprint.route('/api/v1/player_stats_by_seed_region/<string:region>/<int:seed>')
def player_stats(region, seed):
    df = get_player_stats(region=region, seed=seed)
    return df.to_dict('records')


@route_blueprint.route('/api/v1/draft_player/<string:player_id>')
def draft_player(player_id):
    update_draft_player(player_id)
    return f"drafted player {player_id}"


@route_blueprint.route('/api/v1/logs')
def logs():
    e = model.get_engine()
    # TODO date_format to yyyy-mm-dd HH.....
    df = pd.read_sql_query("""select timestamp, message from console_logs order by timestamp desc""", con=e)
    return df.to_dict('records')


@route_blueprint.route('/draft_night/')
def draft_night():
    return render_template('draft_night.html')


# @route_blueprint.route('/player_stats/')
# def player_stats():
#     e = model.get_engine()
#     player_stats_df = pd.read_sql_query("""select tbl.seed, tbl.region, tbl.title, GROUP_CONCAT(tbl.name ORDER BY tbl.ppg desc) AS name_list, GROUP_CONCAT(tbl.ppg ORDER BY tbl.ppg desc) AS ppg_list
#     from (
#         select
#             t.seed,
#             t.region,
#             CONCAT(t.seed, ' - ', t.region, ' - ', t.name) as title,
#             CONCAT(p.first_name, ' ', p.last_name) as name,
#             ROUND(p.ppg, 1) as ppg
#         from tbl_player p
#             inner join tbl_ball_team t on p.fk_ball_team_id = t.id
#         where p.ppg > 3
#         order by t.name desc
#     ) tbl
#     group by 1,2,3""",
#         con=e
#     )
#
#     #
#     # player_stats_df = pd.read_sql_query("""select seed, GROUP_CONCAT(title ORDER BY region desc) as titles, json_arrayagg(name_list) as name_list, json_arrayagg(ppg_list) as ppg_list
#     # from (
#     # 	select tbl.seed, tbl.region, tbl.title, GROUP_CONCAT(tbl.name ORDER BY tbl.ppg desc) AS name_list, GROUP_CONCAT(tbl.ppg ORDER BY tbl.ppg desc) AS ppg_list
#     # 	from (
#     # 		select
#     # 			t.seed,
#     # 			t.region,
#     # 			CONCAT(t.seed, ' - ', t.region, ' - ', t.name) as title,
#     # 			CONCAT(p.first_name, ' ', p.last_name) as name,
#     # 			ROUND(p.ppg, 1) as ppg
#     # 		from tbl_player p
#     # 			inner join tbl_ball_team t on p.fk_ball_team_id = t.id
#     # 		where p.ppg > 3
#     # 		order by t.name desc
#     # 	) tbl
#     # 	group by 1,2,3
#     # ) tbl2
#     # group by 1""", con=e)
#
#     import pdb;
#     # def zip_lists(row):
#     #     zipped_list = []
#     #     for item in list(zip(row['name_list'], row['ppg_list'])):
#     #         pdb.set_trace()
#     #         names = item[0].split(',')
#     #         ppgs = item[1].split(',')
#     #         nested_list = list(zip(names, ppgs))
#     #         zipped_list.append(nested_list)
#     #         pdb.set_trace()
#     #         #print(zipped_list)
#     #     return zipped_list
#
#     def zip_lists(row):
#         names = row["name_list"].split(',')
#         ppgs = row["ppg_list"].split(',')
#         zipped_list = list(zip(names, ppgs))
#         #print(zipped_list)
#         return zipped_list
#
#     #player_stats_df["titles"] = player_stats_df.apply(lambda x: x['titles'].split(','), axis=1)
#     player_stats_df["data"] = player_stats_df.apply(zip_lists, axis=1)
#     player_stats_df = player_stats_df.drop(['name_list', 'ppg_list'], axis=1)
#     player_stats_list = player_stats_df.to_dict("records")
#     print(player_stats_list)
#
#     return render_template('player_stats.html', player_stats_list=player_stats_list)

@route_blueprint.route('/')
def home():
    return render_template('home.html')


@route_blueprint.route('/bracket/')
def bracket():
    return render_template('bracket.html')


@route_blueprint.route('/leaderboard/')
def leaderboard():
    return render_template('leaderboard.html')

#
# @route_blueprint.route('/teams/')
# def teams():
#     return render_template('teams.html')
#



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