// Product pairs that appear in the same order.
// CONTAINS stores quantity and unit_price on the relationship.
MATCH (o:Order)-[:CONTAINS]->(p1:Product),
      (o)-[:CONTAINS]->(p2:Product)
WHERE p1.product_id < p2.product_id
RETURN p1.name AS product_a,
       p2.name AS product_b,
       count(DISTINCT o) AS shared_orders
ORDER BY shared_orders DESC
LIMIT 20;
