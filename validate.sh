#!/usr/bin/env bash
SCHEMA_PATH=scenario-schemas/disease_outbreak.json

curl -X POST "https://validation.kairos.nextcentury.com/json-ld/ksf/validate" \
    -H "accept: application/json" \
    -H "Content-Type: application/ld+json" \
    -d "$(cat ${SCHEMA_PATH})"