import zipfile
import json
import sys


for i in range(1, len(sys.argv)):
    if sys.argv[i].endswith('.json'):
        with open(sys.argv[i], 'r') as f:
            json_str = json.dumps(json.load(f), indent=4)
        with open(sys.argv[i], 'w') as f:
            f.write(json_str)
        print('Pretty Printed {}'.format(sys.argv[i]))
    if sys.argv[i].endswith('.pbix'):
        zf = zipfile.ZipFile(sys.argv[i])
        data = json.loads(zf.read('Report/Layout').decode('utf-16-le'))
        data['config'] = json.loads(data['config'])
        for section in data['sections']:
            for visual_container in section['visualContainers']:
                for key in ['config', 'filters', 'query', 'dataTransforms']:
                    if key in visual_container.keys():
                        visual_container[key] = json.loads(visual_container[key])
        output_path = sys.argv[i][:-5] + '.json'
        print(output_path)
        print(data)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
