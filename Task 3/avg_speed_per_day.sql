--Create View for each Ship

-- CREATE OR REPLACE VIEW speed_per_day_463 AS SELECT * FROM position_data WHERE ship='Ship_463';
-- CREATE OR REPLACE VIEW speed_per_day_733 AS SELECT * FROM position_data WHERE ship='Ship_733';
-- CREATE OR REPLACE VIEW speed_per_day_642 AS SELECT * FROM position_data WHERE ship='Ship_642';
-- CREATE OR REPLACE VIEW speed_per_day_417 AS SELECT * FROM position_data WHERE ship='Ship_417';
-- CREATE OR REPLACE VIEW speed_per_day_584 AS SELECT * FROM position_data WHERE ship='Ship_584';
-- CREATE OR REPLACE VIEW speed_per_day_454 AS SELECT * FROM position_data WHERE ship='Ship_454';
-- CREATE OR REPLACE VIEW speed_per_day_495 AS SELECT * FROM position_data WHERE ship='Ship_495';
-- CREATE OR REPLACE VIEW speed_per_day_322 AS SELECT * FROM position_data WHERE ship='Ship_322';
-- CREATE OR REPLACE VIEW speed_per_day_337 AS SELECT * FROM position_data WHERE ship='Ship_337';
-- CREATE OR REPLACE VIEW speed_per_day_707 AS SELECT * FROM position_data WHERE ship='Ship_707';


-- SELECT DISTINCT ship from position_data;
-- SELECT cast(timestamps as date) as days, AVG(speed) from speed_per_day_337
-- GROUP BY cast(timestamps as date) order by days;



--Calculate average speed of each vessel for each day
SELECT * FROM (SELECT ship, AVG(speed) as avg_speed, cast(timestamps as date) as days from position_data GROUP BY cast(timestamps as date), ship) ship_speed where ship='Ship_463';

