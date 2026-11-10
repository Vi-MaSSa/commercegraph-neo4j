# Troubleshooting

## Aura connection fails

- Confirm the URI starts with `neo4j+s://` for Aura.
- Check username, password and database name.
- Confirm the Aura instance is running and your IP/network is allowed by its network settings.
- Do not paste credentials into GitHub issues or screenshots.

## `ModuleNotFoundError: neo4j`

Activate the project virtual environment and run `pip install -r requirements.txt`.

## CSV file not found

Run `python scripts/generate_dataset.py` from the repository root before running the importer.

## Import appears to create duplicates

The importer uses uniqueness constraints and `MERGE` on stable IDs. If you changed the schema or generated IDs, inspect the validation queries and ensure IDs are stable. Do not delete the database blindly; inspect the target database first.

## `LOAD CSV file:///...` cannot find a local file

The path is resolved by the Neo4j server, not by the local Python process. For Aura, use the included Python Driver importer or host the CSV at an HTTPS URL accessible to Aura.
