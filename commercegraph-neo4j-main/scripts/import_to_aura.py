"""Import generated CSV files into Neo4j Aura using batched UNWIND queries."""
from pathlib import Path
import csv
import os
from datetime import date
from dotenv import load_dotenv
from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "generated"
BATCH_SIZE = 500

NODE_FILES = {
    "customers": ("Customer", "customer_id"),
    "orders": ("Order", "order_id"),
    "products": ("Product", "product_id"),
    "categories": ("Category", "category_id"),
    "brands": ("Brand", "brand_id"),
    "suppliers": ("Supplier", "supplier_id"),
    "payments": ("Payment", "payment_id"),
    "shipments": ("Shipment", "shipment_id"),
    "reviews": ("Review", "review_id"),
}

CSV_FIELD_CONVERTERS = {
    "orders": {"order_date": date.fromisoformat},
    "products": {"price": float},
    "order_items": {"quantity": int, "unit_price": float},
    "reviews": {"rating": int},
}

def read_batches(path):
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        converters = CSV_FIELD_CONVERTERS.get(path.stem, {})
        batch = []
        for row_number, row in enumerate(reader, start=2):
            for field, converter in converters.items():
                try:
                    row[field] = converter(row[field])
                except (KeyError, TypeError, ValueError) as error:
                    raise ValueError(
                        f"Invalid {field} value {row.get(field)!r} "
                        f"in {path.name} at row {row_number}"
                    ) from error
            batch.append(row)
            if len(batch) >= BATCH_SIZE:
                yield batch
                batch = []
        if batch:
            yield batch

def run_batches(session, query, path):
    total = 0
    for batch in read_batches(path):
        result = session.run(query, rows=batch)
        result.consume()
        total += len(batch)
    print(f"{path.name}: processed {total} rows")

def create_constraints(session):
    for label, key in NODE_FILES.values():
        session.run(
            f"CREATE CONSTRAINT {label.lower()}_{key} IF NOT EXISTS "
            f"FOR (n:{label}) REQUIRE n.{key} IS UNIQUE"
        ).consume()

def import_nodes(session):
    for filename, (label, key) in NODE_FILES.items():
        query = (
            f"UNWIND $rows AS row "
            f"MERGE (n:{label} {{{key}: row.{key}}}) "
            f"SET n += row"
        )
        run_batches(session, query, DATA / f"{filename}.csv")

def import_relationships(session):
    jobs = [
        ("MATCH (c:Customer {customer_id: row.customer_id}), (o:Order {order_id: row.order_id}) MERGE (c)-[:PLACED]->(o)", "orders.csv"),
        ("MATCH (o:Order {order_id: row.order_id}), (p:Payment {payment_id: row.payment_id}) MERGE (o)-[:HAS_PAYMENT]->(p)", "payments.csv"),
        ("MATCH (o:Order {order_id: row.order_id}), (s:Shipment {shipment_id: row.shipment_id}) MERGE (o)-[:HAS_SHIPMENT]->(s)", "shipments.csv"),
        ("MATCH (p:Product {product_id: row.product_id}), (c:Category {category_id: row.category_id}) MERGE (p)-[:IN_CATEGORY]->(c)", "products.csv"),
        ("MATCH (p:Product {product_id: row.product_id}), (b:Brand {brand_id: row.brand_id}) MERGE (p)-[:BELONGS_TO]->(b)", "products.csv"),
        ("MATCH (s:Supplier {supplier_id: row.supplier_id}), (p:Product {product_id: row.product_id}) MERGE (s)-[:SUPPLIES]->(p)", "products.csv"),
        ("MATCH (o:Order {order_id: row.order_id}), (p:Product {product_id: row.product_id}) MERGE (o)-[r:CONTAINS]->(p) SET r.quantity = row.quantity, r.unit_price = row.unit_price", "order_items.csv"),
        ("MATCH (c:Customer {customer_id: row.customer_id}), (r:Review {review_id: row.review_id}) MERGE (c)-[:WROTE]->(r)", "reviews.csv"),
        ("MATCH (r:Review {review_id: row.review_id}), (p:Product {product_id: row.product_id}) MERGE (r)-[:REVIEWS]->(p)", "reviews.csv"),
    ]
    for cypher, filename in jobs:
        run_batches(session, f"UNWIND $rows AS row {cypher}", DATA / filename)

def main():
    load_dotenv(ROOT / ".env")
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    if not all([uri, username, password]) or "replace_me" in (password or ""):
        raise SystemExit("Configure NEO4J_URI, NEO4J_USERNAME and NEO4J_PASSWORD in .env first.")
    if not DATA.exists() or not (DATA / "customers.csv").exists():
        raise SystemExit("Dataset not found. Run: python scripts/generate_dataset.py")

    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            create_constraints(session)
            import_nodes(session)
            import_relationships(session)
        print("\\nImport finished. Run cypher/03_validation.cypher in Neo4j Browser.")
    finally:
        driver.close()

if __name__ == "__main__":
    main()
