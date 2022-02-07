# TA1 Schema Library
TA1 schemas 

## Visualization tool
The visualization tool is for download at https://github.com/cu-clear/schema-interface/releases/tag/v0.5.2.

User manual: https://chrysographes.notion.site/Schema-Curation-Manual-c17f79c7450246d3ad7796e43bebea1b
## Contribution guide 
- Validate the schema `json` file at https://validation.kairos.nextcentury.com//#/SDF/validateKsfRequest
- Upload the validated schema to `scenario-schemas/`
- Upload the human readable format to `hrf`

### Rules of thumb for schema curation 
  1. Every event must have the "name", "@id", "qnode", "qlabel", "ta1explanation" field. The "ta1explanation" field can come from the XPO overlay event description, or you can also explain why this event belongs in the schema.
  2. The participant "roleName" should come from the XPO overlay. If the event is not in the xpo, you can try to find similar role names.
  3. The participant "entity" field should be cross-referred in the "entities" list.
  4. All "@id" fields contain an UNIQUE 5 digit id. Our convention is that events use "1XXXX", relations use "3XXXXX", entities use "0XXXX" and participants use "2XXXX". There is no relation between the participant id and the entity id.
  5. Temporal links are represented by "outlinks". "outlinks" are specified within the "child" construct. 
  6. Logical gates should be added sparingly. If you need to add a logical gate (for example XOR(A, B)) , you will need to first create a virtual container node C which has children A and B, then set the "children_gate" to "xor". The default value for "children_gate" is "or".
  7. The schema for each scenario should only have 1 root node (node without parent).

## Submission guide 
- Validate all individual schemas using `validate.sh`
- Run `combine_schema.py` to obtain the final schema.
- Run `validate.sh` again for `resin-schemalib.json`

- The final schema library should be named `resin-schemalib.json` and the hrf file should be `resin-schemalib-hrf.pdf`
