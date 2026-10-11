USE mamaearth;

-- a) Order totals
-- expected: 180 orders, revenue ~99860.20, avg ~554.78
SELECT COUNT(*) AS total_orders,
       ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct,0)/100)),2) AS total_revenue,
       ROUND(AVG(o.quantity * p.price * (1 - COALESCE(o.discount_pct,0)/100)),2) AS avg_order_value
FROM orders o
JOIN products p ON o.product_id = p.product_id;

-- b) count(*) vs count(rating)
-- should be (180, 165, 15)
SELECT COUNT(*) AS total_orders,
       COUNT(rating) AS rated_orders,
       COUNT(*) - COUNT(rating) AS missing_ratings
FROM orders;

-- c) customers with zero orders
-- via LEFT JOIN
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) = 0;

-- same check using NOT IN
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM orders);

-- d) return rate by city
-- only >20% return rate shown
SELECT c.city,
       COUNT(o.order_id) AS total_orders,
       SUM(CASE WHEN o.returned=1 THEN 1 ELSE 0 END) AS returned_orders,
       ROUND(SUM(CASE WHEN o.returned=1 THEN 1 ELSE 0 END)*100.0/COUNT(o.order_id),1) AS return_rate_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
HAVING return_rate_pct > 20
ORDER BY return_rate_pct DESC;

-- e) ranking customers by spend
-- tie-break: order by customer_id ASC so result is stable
SELECT c.customer_id, c.name,
       ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct,0)/100)),2) AS total_spend
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 5;

-- ranks 3–5 only (LIMIT+OFFSET)
SELECT c.customer_id, c.name,
       ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct,0)/100)),2) AS total_spend
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 3 OFFSET 2;

-- f) revenue by category
SELECT p.category,
       COUNT(o.order_id) AS order_count,
       ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct,0)/100)),2) AS category_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- g) customers whose name starts with A
SELECT * FROM customers WHERE name LIKE 'A%';

-- h) distinct acquisition sources
SELECT DISTINCT acquisition_source FROM customers;

-- i) loyalty tier update
ALTER TABLE customers ADD COLUMN loyalty_tier VARCHAR(10);

UPDATE customers
SET loyalty_tier = CASE WHEN city_tier=1 THEN 'Gold' ELSE 'Silver' END;

SELECT loyalty_tier, COUNT(*) 
FROM customers
GROUP BY loyalty_tier;
