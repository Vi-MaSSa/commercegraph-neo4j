// Inspect labels and relationship types after import.
CALL db.labels() YIELD label RETURN label ORDER BY label;
CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType ORDER BY relationshipType;
  