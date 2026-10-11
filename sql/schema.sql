CREATE DATABASE mamaearth;
USE mamaearth;

create table customers (
customer_id VARCHAR(10) PRIMARY KEY,
name varchar(50) Not Null,
city varchar(50) Not Null,
city_tier int NOT NULL,
signup_date DATE NOT NULL,
acquisition_source varchar(20) NOT NULL
);

CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(30) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    discount_pct INT,
    payment_method VARCHAR(10) NOT NULL,
    rating INT,
    returned INT NOT NULL DEFAULT 0,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

