-- isolate relevant records for even strength modeling 
create table even_shot_data_table
as select *
from shot_data_table
where 
	lower(shot_event) != 'block' and 
	strength in ('5x5', '4x4', '3x3') and 
	lower(shot_type) in ('wrap-around', 'deflected', 'tip-in', 'backhand', 'snap', 'slap', 'wrist') and 
	position is not null and 
	shoots is not null; 

-- isolate relevant data for man advantage modeling
create table man_adv_shot_data_table 
as select * 
from shot_data_table
where 
	lower(shot_event) != 'block' and 
	(state_5v4 = 1 or state_4v3 = 1 or state_5v3 = 1 or state_6v5 = 1 or state_6v4 = 1) and 
	lower(shot_type) in ('wrap-around', 'deflected', 'tip-in', 'backhand', 'snap', 'slap', 'wrist') and 
	position is not null and 
	shoots is not null;

-- isolate relevant data for short handed modeling
create table short_shot_data_table 
as select * 
from shot_data_table
where 
	lower(shot_event) != 'block' and 
	(state_4v5 = 1 or state_3v4 = 1 or state_3v5 = 1) and 
	lower(shot_type) in ('wrap-around', 'deflected', 'tip-in', 'backhand', 'snap', 'slap', 'wrist') and 
	position is not null and 
	shoots is not null;