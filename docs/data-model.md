# Data model

See the schema table in the root README. Each entity uses a stable identifier:
`customer_id`, `order_id`, `product_id`, `category_id`, `brand_id`, `supplier_id`, `payment_id`, `shipment_id`, `review_id`.

## Relationship properties

`CONTAINS` stores `quantity` and `unit_price`, preserving the price at the time of purchase rather than relying on the product's current catalog price.

`PLACED` stores no additional properties in the initial model. Later iterations may add channel or attribution metadata when the business question requires it.
