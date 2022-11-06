import os 
import json
import argparse
import re 
from copy import deepcopy 

EVENT_RE = r'resin:Events/(\d{5})/?(.*)'
PARTICIPANT_RE = r'resin:Participants/(\d{5})/?(.*)'
ENTITY_RE = r'resin:Entities/(\d{5})/?(.*)'
RELATION_RE = r'resin:Relations/(\d{5})/?(.*)'


schema = {
        "@context": [
        "https://kairos-sdf.s3.amazonaws.com/context/kairos-v2.0.jsonld",
        {
        "caci": "https://caci.com/kairos/",
        "my_key": "caci:my_key",
        "giant_bitstring": "caci:giant_bitstring",
        "resin": "https://blender.cs.illinois.edu/kairos/"
        }
        ],
        "@id": "resin:Submissions/TA1/schemas_eval",
        "sdfVersion": "2.0",
        "version": "resin:schemalib/eval",
        "events": [],
        "entities": [],
        "relations": []
    }

def fix_prefix(id):
    prefix, name = id.split(':', 1)
    id = f'resin:{name}'
    return id 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema_dir', type=str, default='scenario-schemas-verified')
    args = parser.parse_args() 

    local_to_global = {} # (scenario, @id) -> @id 
    global_to_local = {} # @id -> (scenario, @id)

    e_idx = 10000
    ent_idx = 0
    rel_idx =30000
    p_idx= 20000


    # create @id mapping 

    for filename in os.listdir(args.schema_dir):
        ext = os.path.splitext(filename)[1]
        if ext != '.json': continue 
        with open(os.path.join(args.schema_dir, filename)) as f:
            scenario_schema = json.load(f)
            
            scenario = os.path.splitext(filename)[0]

            for e in scenario_schema['events']:
                e_id = e['@id']
                e_id = fix_prefix(e_id)

                
                m = re.match(EVENT_RE, e_id)
                if not m:
                    raise ValueError(f'{e_id} does not match @id format')
                local_idx = m.group(1)
                suffix = m.group(2)
                global_id = f'resin:Events/{e_idx:05d}/{suffix}'
                local_to_global[(scenario, e_id)] = global_id 
                global_to_local[global_id ] = (scenario, e_id)
                e_idx += 1

                p_list = e.get('participants', [])
                for p in p_list:
                    p_id = fix_prefix(p['@id'])
                
                    m = re.match(PARTICIPANT_RE, p_id)
                    local_idx = m.group(1)
                    suffix = m.group(2)
                    global_id = f'resin:Participants/{p_idx:05d}/{suffix}'
                    local_to_global[(scenario, p_id)] = global_id 
                    global_to_local[global_id ] = (scenario, p_id)
                    p_idx +=1 
                
            for ent in scenario_schema['entities']:
                ent_id = fix_prefix(ent['@id'])
                m = re.match(ENTITY_RE, ent_id)
                local_idx = m.group(1)
                suffix = m.group(2)
                global_id = f'resin:Entities/{ent_idx:05d}/{suffix}'
                local_to_global[(scenario, ent_id)] = global_id 
                global_to_local[global_id ] = (scenario, ent_id)
                ent_idx +=1 

            for rel in scenario_schema['relations']:
                rel_id = fix_prefix(rel['@id']) 
                m = re.match(RELATION_RE, rel_id)
                if not m:
                    raise ValueError(f'{rel_id} does not match @id format')
                local_idx = m.group(1)
                suffix = m.group(2)
                global_id = f'resin:Relations/{rel_idx:05d}/{suffix}'
                local_to_global[(scenario, rel_id)] = global_id 
                global_to_local[global_id ] = (scenario, rel_id)
                rel_idx +=1 

        
    # copy to single schema 
    for filename in os.listdir(args.schema_dir):
        ext = os.path.splitext(filename)[1]
        if ext != '.json': continue 
        with open(os.path.join(args.schema_dir, filename)) as f:
            scenario_schema = json.load(f)
            scenario = os.path.splitext(filename)[0]

            events = scenario_schema['events']
            for e in events:
                global_e = deepcopy(e)
                e_id = fix_prefix(e['@id'])
            
                global_e['@id'] = local_to_global[(scenario, e_id)]
                global_e['participants'] = []
                

                p_list = e.get('participants', [])
                for p in p_list:
                    p_id = fix_prefix(p['@id']) 

                    global_p = deepcopy(p)
                    global_p['@id'] = local_to_global[(scenario, p_id)]
                    global_p['entity'] = local_to_global[(scenario, fix_prefix(p['entity']))]

                    global_e['participants'].append(global_p)
                
                if 'children' in e:
                    global_e['children'] = []
                    children_list = e.get('children', [])

                    for child in children_list:
                        try:
                            global_child = deepcopy(child)
                            global_child['child'] = local_to_global[(scenario, fix_prefix(child['child']))]
                            global_child['outlinks'] = [local_to_global[(scenario, fix_prefix(x))] for x in child['outlinks']]

                            global_e['children'].append(global_child)
                        except KeyError as e:
                            print(e)
                
                schema['events'].append(global_e)
            
            for ent in scenario_schema['entities']:
                global_ent = deepcopy(ent)
                global_ent['@id'] = local_to_global[(scenario, fix_prefix(ent['@id']))]
                schema['entities'].append(global_ent)

            
            for rel in scenario_schema['relations']:
                global_rel = deepcopy(rel)
                global_rel['@id'] = local_to_global[(scenario, fix_prefix(rel['@id']))]
                global_rel['relationSubject'] = local_to_global[(scenario, rel['relationSubject'])]
                global_rel['relationObject'] = local_to_global[(scenario, rel['relationObject'])]
                schema['relations'].append(global_rel)


            




    with open('resin-schemalib.json','w') as f:
        json.dump(schema, f, indent=2)
