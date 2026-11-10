# CommerceGraph — E-commerce Intelligence with Neo4j

> A reproducible graph-data project for exploring customer behavior, product affinity, sales and supplier networks.

**Status:** Phase 1 — project foundation and reproducible dataset.

## 1. Business problem

E-commerce data contains connected entities: customers place orders, orders contain products, products belong to categories and brands, suppliers provide products, and orders are associated with payments and shipments. CommerceGraph models these connections in Neo4j so that multi-hop questions can be explored naturally with Cypher.

## 2. Why a graph database?

A relational model remains appropriate for transactional systems and structured reporting. A graph model is especially useful when the question depends on traversing relationships, such as finding products bought together, exploring supplier dependencies, or discovering customer-product paths. This project demonstrates those graph-specific use cases rather than claiming that graphs replace relational databases.

## 3. Technology

- Neo4j Aura (managed graph database)
- Cypher
- Python 3.10+
- Neo4j Python Driver
- CSV for portable source data

## 4. Graph model

### Node labels

`Customer`, `Order`, `Product`, `Category`, `Brand`, `Supplier`, `Payment`, `Shipment`, `Review`

### Relationships

| Relationship | Pattern | Meaning |
|---|---|---|
| `PLACED` | Customer → Order | Customer placed an order |
| `CONTAINS` | Order → Product | Order contains a product |
| `IN_CATEGORY` | Product → Category | Product belongs to a category |
| `BELONGS_TO` | Product → Brand | Product belongs to a brand |
| `SUPPLIES` | Supplier → Product | Supplier supplies a product |
| `HAS_PAYMENT` | Order → Payment | Order has a payment |
| `HAS_SHIPMENT` | Order → Shipment | Order has a shipment |
| `WROTE` | Customer → Review | Customer wrote a review |
| `REVIEWS` | Review → Product | Review refers to a product |

### Modeling notes

- Every node has a stable business identifier (`*_id`).
- Relationships are created with `MERGE` to make imports repeatable.
- An order can contain multiple products; a product can appear in many orders.
- The generated data is synthetic and must not be interpreted as real customer or commercial information.

## 5. Repository structure

```text
commercegraph-neo4j/
├── data/                  # Generated CSV files
├── cypher/                # Constraints, schema and analytical queries
├── docs/                  # Architecture, model and troubleshooting
├── scripts/               # Dataset generation and Aura import
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 6. Quick start

### Requirements

- Python 3.10 or newer
- A Neo4j Aura database and its connection URI
- Network access to your Aura instance

### Install dependencies

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

### Generate the synthetic dataset

```bash
python scripts/generate_dataset.py
```

The generator writes CSV files to `data/generated/`. It uses a fixed random seed by default, so the dataset is reproducible.

### Configure Aura credentials

Copy `.env.example` to `.env` and fill in the connection details from Neo4j Aura:

```env
NEO4J_URI=neo4j+s://<your-aura-id>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
```

Never commit `.env` or publish your database password.

### Create constraints and import

```bash
python scripts/import_to_aura.py
```

The importer reads local CSV files and sends parameterized batches with `UNWIND` through the official Neo4j Python Driver. This approach works with Aura without requiring the database server to access your computer's local files.

## 7. Validation

After import, run the queries in `cypher/03_validation.cypher` in Neo4j Browser. Confirm that all expected labels exist, identifiers are unique, and relationship counts are non-zero.

## 8. Business questions

The analytical query pack will answer questions such as:

1. Which customers place the most orders?
2. Which product pairs most often occur in the same order?
3. Which products have the highest review ratings?
4. Which suppliers provide the broadest product coverage?
5. Which products could be recommended to a customer based on co-purchase behavior?

## 9. Data and limitations

All records are synthetic. The generator is designed for learning and portfolio demonstration, not for production forecasting. Recommendation scores in the initial version are simple co-occurrence counts, not a trained machine-learning model.

## 10. Roadmap

- [x] Define project scope and graph schema
- [x] Add deterministic synthetic-data generator
- [x] Add Aura importer using batched `UNWIND`
- [ ] Validate imported graph and capture Browser evidence
- [ ] Add business query pack and explain query plans
- [ ] Document performance decisions and troubleshooting
- [ ] Publish final architecture and result screenshots

## 11. Author

Add your GitHub profile and contact information here.
