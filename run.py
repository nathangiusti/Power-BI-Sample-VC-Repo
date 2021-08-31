import json
import sys


for i in range(1, len(sys.argv)):
    if sys.argv[i].endswith('.json'):
        with open(sys.argv[i], 'r') as f:
            json_str = json.dumps(json.load(f), indent=4)
        with open(sys.argv[i], 'w') as f:
            f.write(json_str)
        print('Pretty Printed {}'.format(sys.argv[i]))
