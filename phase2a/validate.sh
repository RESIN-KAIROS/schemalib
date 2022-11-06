#!/usr/bin/env bash
SCHEMA_PATH=scenario-schemas-verified 

for schema_file in ${SCHEMA_PATH}/*.json; do
    echo "Validating ${schema_file}..."
    curl -X POST "https://validation.kairos.nextcentury.com/json-ld/ksf/validate" \
        -H "accept: application/json" \
        -H "Content-Type: application/ld+json" \
        -d "$(cat ${schema_file})"
done 


# for combined schema 
curl -X POST "https://validation.kairos.nextcentury.com/json-ld/ksf/validate" \
    -H "accept: application/json" \
    -H "Content-Type: application/ld+json" \
    -d "$(cat resin-schemalib.json)"