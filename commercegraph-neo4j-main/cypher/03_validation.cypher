// Node counts by label
MATCH (n)
RETURN labels(n) AS labels, count(*) AS total
ORDER BY total DESC;

// Relationship counts by type
MATCH ()-[r]->()
RETURN type(r) AS relationship, count(*) AS total
ORDER BY total DESC;

// Check for products without a category
MATCH (p:Product)
WHERE NOT (p)-[:IN_CATEGORY]->(:Category)
RETURN p.product_id, p.name
LIMIT 20;

// Check for orders without a customer
MATCH (o:Order)
WHERE NOT (:Customer)-[:PLACED]->(o)
RETURN o.order_id
LIMIT 20;
