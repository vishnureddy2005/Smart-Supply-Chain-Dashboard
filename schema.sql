CREATE DATABASE walmart_sparkathon;
USE walmart_sparkathon;

CREATE TABLE deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    destination VARCHAR(100),
    distance_km FLOAT,
    weather_condition VARCHAR(50),
    traffic_level VARCHAR(50),
    holiday_flag BOOLEAN,
    predicted_delay_minutes FLOAT
);
 CREATE TABLE products (
     product_id INT AUTO_INCREMENT PRIMARY KEY,
     product_name VARCHAR(100),
     stock_level INT
 );
 
INSERT INTO products (product_name, stock_level) VALUES
  ('Product A', 50),
  ('Product B', 60),
  ('Product C', 70),
  ('Product D', 80),
  ('Product E', 90);
ALTER TABLE deliveries ADD COLUMN origin_address VARCHAR(255);
DESCRIBE deliveries;
SELECT * FROM deliveries;