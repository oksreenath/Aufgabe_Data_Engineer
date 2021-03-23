SELECT DISTINCT speed FROM position_data WHERE speed = (SELECT MAX(SPEED) FROM position_data) AND ship = 'Ship_733';

ALTER TABLE ship_engines ADD COLUMN MAX_SPEED INT;

ALTER TABLE ship_engines ALTER COLUMN engine1_power type VARCHAR;
ALTER TABLE ship_engines ALTER COLUMN engine2_power type VARCHAR;
ALTER TABLE ship_engines ALTER COLUMN engine3_power type VARCHAR;

-- ALTER TABLE ship_engines DROP COLUMN SPEED;


-- INSERT INTO ship_engines (speed) SELECT MAX(speed) FROM position_data t WHERE (SELECT ship_name FROM ship_engines WHERE ship_name = t.ship);

-- INSERT INTO ship_engines (max_speed) SELECT DISTINCT MAX(speed) FROM position_data t WHERE (SELECT ship_name = t.ship FROM ship_engines);

UPDATE ship_engines se SET max_speed = (SELECT MAX(speed)FROM position_data pe
WHERE  se.ship_name = pe.ship);

UPDATE ship_engines se SET engine1_power = (SELECT DISTINCT max_rating FROM motors mo WHERE LOWER(se.engine1_name) = LOWER(mo.product_id));

UPDATE ship_engines se SET engine2_power = (SELECT DISTINCT max_rating FROM motors mo WHERE LOWER(se.engine2_name) = LOWER(mo.product_id));

UPDATE ship_engines se SET engine3_power = (SELECT DISTINCT max_rating FROM motors mo WHERE LOWER(se.engine3_name) = LOWER(mo.product_id));


