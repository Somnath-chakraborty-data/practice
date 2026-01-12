CREATE TABLE raw_sales (
    order_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    amount DECIMAL(10,2),
    order_date DATE
);

INSERT INTO raw_sales VALUES 
(1, 'Laptop', 1200.00, CURRENT_DATE),
(2, 'Mouse', 25.00, CURRENT_DATE),
(3, 'Monitor', 300.00, CURRENT_DATE);