create or replace view vw_fantasy_team_ownership
as
select
	u.name as OwnerName,
    u.is_active as IsActive,
    ft.name as TeamName
from tbl_user u
	inner join tbl_fantasy_team_user_mtm mtm
		on u.id = mtm.fk_user_id
    inner join tbl_fantasy_team ft
		on ft.id = mtm.fk_fantasy_team_id;