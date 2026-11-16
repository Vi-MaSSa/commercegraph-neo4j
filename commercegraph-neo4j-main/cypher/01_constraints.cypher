// Run once before importing data. Constraints are idempotent.
CREATE CONSTRAINT customer_id IF NOT EXISTS FOR (n:Customer) REQUIRE n.customer_id IS UNIQUE;
CREATE CONSTRAINT order_id IF NOT EXISTS FOR (n:Order) REQUIRE n.order_id IS UNIQUE;
CREATE CONSTRAINT product_id IF NOT EXISTS FOR (n:Product) REQUIRE n.product_id IS UNIQUE;
CREATE CONSTRAINT category_id IF NOT EXISTS FOR (n:Category) REQUIRE n.category_id IS UNIQUE;
CREATE CONSTRAINT brand_id IF NOT EXISTS FOR (n:Brand) REQUIRE n.brand_id IS UNIQUE;
CREATE CONSTRAINT supplier_id IF NOT EXISTS FOR (n:Supplier) REQUIRE n.supplier_id IS UNIQUE;
CREATE CONSTRAINT payment_id IF NOT EXISTS FOR (n:Payment) REQUIRE n.payment_id IS UNIQUE;
CREATE CONSTRAINT shipment_id IF NOT EXISTS FOR (n:Shipment) REQUIRE n.shipment_id IS UNIQUE;
CREATE CONSTRAINT review_id IF NOT EXISTS FOR (n:Review) REQUIRE n.review_id IS UNIQUE;
