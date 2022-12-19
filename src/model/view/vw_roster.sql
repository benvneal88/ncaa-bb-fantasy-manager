create or replace view vw_roster
as
select
	bt.Name as TeamName,
    bt.Region as Region,
    bt.seed as Seed,
    p.first_name as FirstName,
    p.last_name as LastName,
    p.ppg as PPG
from tbl_ball_team bt
	inner join tbl_player p on bt.id = p.fk_ball_team_id;