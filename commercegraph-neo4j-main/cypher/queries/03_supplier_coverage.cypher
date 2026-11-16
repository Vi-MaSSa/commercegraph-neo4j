// Suppliers ranked by distinct products supplied
MATCH (s:Supplier)-[:SUPPLIES]->(p:Product)
RETURN s.supplier_id, s.name, count(DISTINCT p) AS product_coverage
ORDER BY product_coverage DESC
LIMIT 10;
