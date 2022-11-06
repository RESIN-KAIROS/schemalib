import os 
import json
import argparse
import re 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema_dir', type=str, default='scenario-schemas')
    args = parser.parse_args() 

    # create @id mapping 
    

    for filename in os.listdir(args.schema_dir):
        if os.path.splitext(filename)[1] == '.json':
            with open(os.path.join(args.schema_dir, filename)) as f:
                scenario_schema = json.load(f)
                scenario = os.path.splitext(filename)[0]

                event_n =0 
                episode_n =0 
                participant_n =0 
                entity_n =0 
                rel_n =0 
                temporal_n =0 

                event_n = len(scenario_schema['events'])
                for e in scenario_schema['events']:
                    p_list = e.get('participants', [])
                    participant_n += len(p_list)
                    if 'children' in e: 
                        episode_n+=1 
                        for child in e['children']:
                            temporal_n += len(child['outlinks']) 
                entity_n = len(scenario_schema['entities'])
                rel_n = len(scenario_schema['relations'])

                print(f'{scenario} schema')
                print(f'{episode_n} & {event_n} & {entity_n} & {rel_n+temporal_n}')

