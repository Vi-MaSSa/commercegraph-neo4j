// Top customers by number of orders
MATCH (c:Customer)-[:PLACED]->(o:Order)
RETURN c.customer_id, c.name, count(o) AS total_orders
ORDER BY total_orders DESC
LIMIT 10;
