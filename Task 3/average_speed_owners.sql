CREATE OR REPLACE VIEW average_speed_owners AS SELECT position_data.ship, position_data.timestamps, position_data.speed, position_data.lon, position_data.lat, ships_owners.owners FROM position_data, ships_owners WHERE ships_owners.ship_id = position_data.ship;

SELECT DISTINCT ship, owners from average_speed;

