"""Generate a deterministic synthetic e-commerce graph dataset."""
from pathlib import Path
import csv
import random
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "generated"
SEED = 42
rng = random.Random(SEED)

def write_csv(name, rows):
    if not rows:
        return
    path = OUT / f"{name}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows):>4} rows -> {path.relative_to(ROOT)}")

def main():
    OUT.mkdir(parents=True, exist_ok=True)

    categories = [
        {"category_id": f"CAT{i:03}", "name": name}
        for i, name in enumerate(
            ["Electronics", "Home", "Sports", "Books", "Beauty", "Fashion", "Toys", "Grocery"], 1
        )
    ]
    brands = [
        {"brand_id": f"BR{i:03}", "name": f"Brand {i:02}"}
        for i in range(1, 13)
    ]
    suppliers = [
        {"supplier_id": f"SUP{i:03}", "name": f"Supplier {i:02}", "country": rng.choice(["BR", "US", "DE", "CN"])}
        for i in range(1, 19)
    ]
    customers = [
        {"customer_id": f"CUS{i:04}", "name": f"Customer {i:04}", "city": rng.choice(["Sao Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte", "Recife"]), "segment": rng.choice(["new", "regular", "premium"])}
        for i in range(1, 151)
    ]
    products = []
    for i in range(1, 101):
        category = rng.choice(categories)
        brand = rng.choice(brands)
        supplier = rng.choice(suppliers)
        products.append({
            "product_id": f"PRD{i:04}",
            "name": f"{category['name']} Product {i:03}",
            "price": round(rng.uniform(19.9, 1499.9), 2),
            "category_id": category["category_id"],
            "brand_id": brand["brand_id"],
            "supplier_id": supplier["supplier_id"],
        })

    orders, order_items, payments, shipments, reviews = [], [], [], [], []
    start = date(2025, 1, 1)
    for i in range(1, 401):
        customer = rng.choice(customers)
        order_date = start + timedelta(days=rng.randint(0, 364))
        orders.append({
            "order_id": f"ORD{i:05}",
            "customer_id": customer["customer_id"],
            "order_date": order_date.isoformat(),
            "status": rng.choice(["delivered", "delivered", "shipped", "cancelled"]),
        })
        chosen = rng.sample(products, rng.randint(1, 4))
        for product in chosen:
            order_items.append({
                "order_id": f"ORD{i:05}",
                "product_id": product["product_id"],
                "quantity": rng.randint(1, 3),
                "unit_price": product["price"],
            })
        payments.append({
            "payment_id": f"PAY{i:05}",
            "order_id": f"ORD{i:05}",
            "method": rng.choice(["credit_card", "pix", "debit_card", "boleto"]),
            "status": rng.choice(["approved", "approved", "pending", "refunded"]),
        })
        shipments.append({
            "shipment_id": f"SHP{i:05}",
            "order_id": f"ORD{i:05}",
            "carrier": rng.choice(["Carrier A", "Carrier B", "Carrier C"]),
            "status": rng.choice(["delivered", "in_transit", "delayed"]),
        })

    # Create reviews from customers who actually bought the reviewed product.
    for i, item in enumerate(rng.sample(order_items, 180), 1):
        order = next(o for o in orders if o["order_id"] == item["order_id"])
        reviews.append({
            "review_id": f"REV{i:04}",
            "customer_id": order["customer_id"],
            "product_id": item["product_id"],
            "rating": rng.randint(1, 5),
            "comment": rng.choice(["Good quality", "As expected", "Fast delivery", "Could be better", "Excellent value"]),
        })

    write_csv("categories", categories)
    write_csv("brands", brands)
    write_csv("suppliers", suppliers)
    write_csv("customers", customers)
    write_csv("products", products)
    write_csv("orders", orders)
    write_csv("order_items", order_items)
    write_csv("payments", payments)
    write_csv("shipments", shipments)
    write_csv("reviews", reviews)

    node_total = sum(map(len, [categories, brands, suppliers, customers, products, orders, payments, shipments, reviews]))
    print(f"\nGenerated {node_total} nodes across 9 labels and {len(order_items)} order-item rows.")
    print("Synthetic data only. Fixed random seed:", SEED)

if __name__ == "__main__":
    main()
