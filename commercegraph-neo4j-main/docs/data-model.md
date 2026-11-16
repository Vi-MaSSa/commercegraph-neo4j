# Data model

See the schema table in the root README. Each entity uses a stable identifier:
`customer_id`, `order_id`, `product_id`, `category_id`, `brand_id`, `supplier_id`, `payment_id`, `shipment_id`, `review_id`.

## Property types

The generator keeps `Order.order_date` as a Python date. Since CSV stores text, the importer parses `Product.price` and `CONTAINS.unit_price` as floats, `Review.rating` and `CONTAINS.quantity` as integers, and `Order.order_date` as a Neo4j `DATE`.

## Relationship properties

`CONTAINS` stores `quantity` as an integer and `unit_price` as a float, preserving the price at the time of purchase rather than relying on the product's current catalog price.

`PLACED` stores no additional properties in the initial model. Later iterations may add channel or attribution metadata when the business question requires it.
