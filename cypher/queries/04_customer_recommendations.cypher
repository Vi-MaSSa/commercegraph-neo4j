// Simple co-purchase recommendation for a customer.
// Parameter: $customer_id
MATCH (target:Customer {customer_id: $customer_id})-[:PLACED]->(:Order)-[:CONTAINS]->(seen:Product)
MATCH (other_order:Order)-[:CONTAINS]->(seen)
MATCH (other_order)-[:CONTAINS]->(candidate:Product)
WHERE candidate <> seen
  AND NOT EXISTS {
    MATCH (target)-[:PLACED]->(:Order)-[:CONTAINS]->(candidate)
  }
RETURN candidate.product_id AS product_id,
       candidate.name AS recommended_product,
       count(DISTINCT other_order) AS score
ORDER BY score DESC
LIMIT 10;
