-- sql/postgres_init.sql
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.sales_transactions (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    price NUMERIC,
    quantity INTEGER,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO raw.sales_transactions (product_name, price, quantity)
VALUES ('MacBook Pro', 2000, 1), ('iPhone 15', 999, 2), ('AirPods', 199, 5);