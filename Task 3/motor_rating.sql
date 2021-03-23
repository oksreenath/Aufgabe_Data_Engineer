SELECT DISTINCT speed FROM position_data WHERE speed = (SELECT MAX(SPEED) FROM position_data) AND ship = 'Ship_733';

ALTER TABLE ship_engines ADD COLUMN MAX_SPEED INT;
ALTER TABLE ship_engines DROP COLUMN SPEED;


-- INSERT INTO ship_engines (speed) SELECT MAX(speed) FROM position_data t WHERE (SELECT ship_name FROM ship_engines WHERE ship_name = t.ship);

INSERT INTO ship_engines (max_speed) SELECT DISTINCT MAX(speed) FROM position_data t WHERE (SELECT ship_name = t.ship FROM ship_engines);

UPDATE ship_engines se SET max_speed = (SELECT MAX(speed)FROM position_data pe
WHERE  se.ship_name = pe.ship);
