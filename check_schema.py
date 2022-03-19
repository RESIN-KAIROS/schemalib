import os 
import json 
import argparse
import re 
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict 


QNODE_RE = r'[QP]\d+'

QNODE_WITH_PREFIX_RE = r'wd:[QP]\d+'


def make_unique_participants(schema: Dict)-> Dict:
    '''
    Participants @ids need to be 5 digit numbers 2XXXX.
    '''
    events = schema['events']
    participant_ids = set() 

    for e in events:
        participant_list = e.get('participants', [])
        for p in participant_list:
            p_id = p['@id']
            m = re.match(r'resin:Participants/(\d+)/?(.*)', p_id)
            if not m:
                print(p_id)
                raise ValueError(f'participant id {p_id} does not match format.')
            
            
            uid = m.group(1)
            # assert uid[0] == '2', f'participant uid {uid} does not start with 2'
            suffix = m.group(2)

            uid = int(uid)

            if uid in participant_ids:
                uid = max(participant_ids) +1 
                participant_ids.add(uid)
                # update the p_id field 
                new_p_id = f'resin:Participants/{uid:5d}/{suffix}'
                p['@id'] = new_p_id
                print(f'updated to {new_p_id}')
            else:
                participant_ids.add(uid)
    
    return schema 

def fix_qnode(schema: Dict, errors: List[str]=[]) -> Tuple[Dict, List]:
    events = schema['events'] 
    entities = schema['entities']
    relations = schema['relations']
    
    for e in events:
        eid = e['@id']
        if 'qnode' in e:
            qnode = e['qnode']
            if qnode == "" and 'children' in e: continue 
            m = re.match(QNODE_WITH_PREFIX_RE, qnode)
            if not m:
                m = re.match(QNODE_RE, qnode)
                if not m: errors.append(f'qnode value {qnode} of event {eid} invalid.')
                # add the prefix 
                else: e['qnode'] = f'wd:{qnode}'
                
        else:
            if 'children' not in e:
                errors.append(f'event {eid} without children missing qnode')
        
    for ent in entities:
        qnode = ent['qnode']
        eid = ent['@id']
        if isinstance(qnode, str):
            m = re.match(QNODE_WITH_PREFIX_RE, qnode)
            if not m:
                m = re.match(QNODE_RE, qnode)
                if not m: errors.append(f'qnode value {qnode} of entity {eid} invalid.')
                # add the prefix 
                else: ent['qnode'] = f'wd:{qnode}'
        else:
            if isinstance(qnode, list):
                print('list of qnodes found')
                print(qnode)

    for r in relations:
        qnode = r['relationPredicate']
        eid = r['@id']
        m = re.match(QNODE_WITH_PREFIX_RE, qnode)
        if not m:
            m = re.match(QNODE_RE, qnode)
            if not m: errors.append(f'qnode value {qnode} of relation {eid} invalid.')
            # add the prefix 
            else: r['relationPredicate'] = f'wd:{qnode}'
    
    return schema , errors 


def check_participants(schema: Dict, warnings: List[str]=[]) -> List[str]:
    events = schema['events']
    for e in events:
        eid = e['@id']
        if 'children' not in e:
            if len(e['participants']) == 0:
                warnings.append(f'event {eid} has no participants')
    
    return warnings 
                
def check_isolated_entity(schema:Dict, warnings: List[str]=[]) -> List[str]:
    entity_usage = defaultdict(int)
    events = schema['events']
    for e in events:
        if 'participants' in e:
            for p in e['participants']:
                entity = p['entity']
                entity_usage[entity] +=1 

    for r in schema['relations']:
        s = r['relationSubject']
        entity_usage[s] +=1 
        o = r['relationObject']
        entity_usage[o] +=1 

    entity_usage = dict(entity_usage)
    for e in entity_usage:
        if entity_usage[e] == 1:
            warnings.append(f'entity {e} has only been referred to once')

    return warnings 

def find_roots(schema:Dict, errors: List[str]=[])-> Set:
    events = schema['events']
    event2parent = {} 
    all_events = set()
    event2name = {} 
    for e in events:
        e_id = e['@id']
        event2name[e_id] = e['name']
        all_events.add(e_id)
        if 'children' in e:
            for child_obj in e['children']:
                child_id = child_obj['child']

                event2parent[child_id] = e_id 
    
    root_events = all_events - set(event2parent.keys())

    if len(root_events) >1:
        errors.append(f'multiple root nodes found {*root_events,}')
    
    return root_events, errors 
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument('--schema_dir', type=str, default='scenario-schemas')
    parser.add_argument('--output_dir', type=str, default='scenario-schemas-verified')
    parser.add_argument('--fix_uid', action='store_true')
    args = parser.parse_args() 


    os.makedirs(args.output_dir, exist_ok=True)

    for filename in os.listdir(args.schema_dir):
        ext = os.path.splitext(filename)[1]
        if ext != '.json': continue 
        with open(os.path.join(args.schema_dir, filename)) as f:
            scenario_schema = json.load(f)
            
            scenario = os.path.splitext(filename)[0]
            print(f'Verifying scenario {scenario}')

            errors = []
            warnings = []

            log_writer = open(os.path.join(args.output_dir, f'{scenario}.log'), 'w')

            if args.fix_uid: 
                make_unique_participants(scenario_schema)
            
            scenario_schema, errors  = fix_qnode(scenario_schema, errors)

            roots, errors  = find_roots(scenario_schema, errors)

            warnings = check_participants(scenario_schema, warnings)
            warnings = check_isolated_entity(scenario_schema, warnings)
            

            if len(errors) >0:
                log_writer.write('Errors: \n')
                for err in errors:
                    log_writer.write(err+'\n')
            if len(warnings) > 0:
                log_writer.write('Warnings: \n')
                for w in warnings:
                    log_writer.write(w +'\n')
            # save to file 
            with open(os.path.join(args.output_dir, filename),'w') as f:
                json.dump(scenario_schema, f, indent=2)

