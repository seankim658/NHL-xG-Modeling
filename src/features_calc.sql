/* FOR TESTING PURPOSES: Create copy of shot_data_table for testing to not potentially corrupt 
 * production data. Only copying a subset of rows to save on some storage space and make it quicker 
 * to test statements.  */
-- create table test_shot_data_table as select * from shot_data_table limit 1000000;

-- alter table by adding columns  
alter table test_shot_data_table 
-- columns to add 
add column event_distance float,
add column event_angle float,
add column score_down_4 int,
add column score_down_3 int,
add column score_down_2 int,
add column score_down_1 int,
add column score_up_4 int,
add column score_up_3 int,
add column score_up_2 int,
add column score_up_1 int,
add column score_even int,
add column wrist_shot int,
add column deflected_shot int,
add column tip_shot int,
add column slap_shot int,
add column backhand_shot int,
add column snap_shot int,
add column wrap_shot int,
add column null_shot int,
add column state_5v5 int,
add column state_4v4 int,
add column state_3v3 int,
add column state_5v4 int,
add column state_4v3 int,
add column state_5v3 int,
add column state_6v5 int,
add column state_6v4 int,
add column state_4v5 int,
add column state_3v4 int,
add column state_3v5 int;

-- update table by setting actual calculations
update test_shot_data_table 
-- calculate the event_distance in relation to the right side net at point (89, 0)
set event_distance = sqrt(power(89 - x, 2) + power(y, 2)),
-- calculate the event_angle in relation to the right side net, the greatest function 
-- is to avoid a potential divide by zero error 
event_angle = degrees(atan(y / greatest(1e-10, 89 - abs(x)))),
-- calculate score state features
score_down_4 = case 
	when is_home = 1 and home_score - away_score <= -4 then 1
	when is_home = 0 and away_score - home_score <= -4 then 1
	else 0
end,
score_down_3 = case  
	when is_home = 1 and home_score - away_score = -3 then 1 
	when is_home = 0 and away_score - home_score = -3 then 1
	else 0
end,
score_down_2 = case
	when is_home = 1 and home_score - away_score = -2 then 1
	when is_home = 0 and away_score - home_score = -2 then 1
	else 0
end,
score_down_1 = case 
	when is_home = 1 and home_score - away_score = -1 then 1 
	when is_home = 0 and away_score - home_score = -1 then 1
	else 0
end,
score_even = case 
	when home_score - away_score = 0 then 1
	else 0
end,
score_up_1 = case
	when is_home = 1 and home_score - away_score = 1 then 1 
	when is_home = 0 and away_score - home_score = 1 then 1 
	else 0
end,
score_up_2 = case 
	when is_home = 1 and home_score - away_score = 2 then 1 
	when is_home = 0 and away_score - home_score = 2 then 1
	else 0
end,
score_up_3 = case 
	when is_home = 1 and home_score - away_score = 3 then 1 
	when is_home = 0 and away_score - home_score = 3 then 1
	else 0
end,
score_up_4 = case 
	when is_home = 1 and home_score - away_score = 4 then 1
	when is_home = 0 and away_score - home_score = 4 then 1
	else 0
end,
-- calculate shot type features 
wrist_shot = case when lower(shot_type) = 'wrist' then 1 else 0 end,
deflected_shot = case when lower(shot_type) = 'deflected' then 1 else 0 end,
tip_shot = case when lower(shot_type) = 'tip-in' then 1 else 0 end,
slap_shot = case when lower(shot_type) = 'slap' then 1 else 0 end,
backhand_shot = case when lower(shot_type) = 'backhand' then 1 else 0 end,
snap_shot = case when lower(shot_type) = 'snap' then 1 else 0 end,
wrap_shot = case when lower(shot_type) = 'wrap-around' then 1 else 0 end,
null_shot = case when shot_type is null then 1 else 0 end,
-- calculate game state features
state_5v5 = case when strength = '5x5' then 1 else 0 end,
state_4v4 = case when strength = '4x4' then 1 else 0 end,
state_3v3 = case when strength = '3x3' then 1 else 0 end,
state_5v4 = case 
	when is_home = 1 and strength = '5x4' then 1 
	when is_home = 0 and strength = '4x5' then 1 
	else 0
end,
state_4v3 = case 
	when is_home = 1 and strength = '4x3' then 1
	when is_home = 0 and strength = '3x4' then 1
	else 0 
end,
state_5v3 = case 
	when is_home = 1 and strength = '5x3' then 1
	when is_home = 0 and strength = '3x5' then 1 
	else 0
end,
state_6v5 = case 
	when is_home = 1 and strength = '6x5' then 1
	when is_home = 0 and strength = '5x6' then 1 
	else 0
end,
state_6v4 = case 
	when is_home = 1 and strength = '6x4' then 1 
	when is_home = 0 and strength = '4x6' then 1 
	else 0
end,
state_4v5 = case 
	when is_home = 1 and strength = '4x5' then 1
	when is_home = 0 and strength = '5x4' then 1
	else 0
end,
state_3v4 = case 
	when is_home = 1 and strength = '3x4' then 1
	when is_home = 0 and strength = '4x3' then 1
	else 0
end,
state_3v5 = case 
	when is_home = 1 and strength = '3x5' then 1 
	when is_home = 0 and strength = '5x3' then 1
	else 0
end;