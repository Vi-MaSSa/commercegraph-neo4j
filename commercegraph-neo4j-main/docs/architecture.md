# Architecture

## Data flow

1. `scripts/generate_dataset.py` creates deterministic synthetic CSV files.
2. `scripts/import_to_aura.py` reads each CSV locally.
3. The Neo4j Python Driver sends batches to Aura using parameterized Cypher and `UNWIND`.
4. Validation queries inspect node and relationship counts.
5. Analytical Cypher queries answer the documented business questions.

## Why the importer uses the Python Driver

Aura cannot automatically read arbitrary local paths from a developer's computer. A local `LOAD CSV file:///...` path therefore does not refer to the developer's machine. This project uses the Python Driver to stream local CSV records to Aura in batches. A future alternative is to host CSV files at publicly accessible HTTPS URLs and use `LOAD CSV WITH HEADERS`.

## Security

Credentials are loaded from environment variables via `.env`. Do not commit secrets, screenshots containing credentials, or Aura connection details that expose access.
