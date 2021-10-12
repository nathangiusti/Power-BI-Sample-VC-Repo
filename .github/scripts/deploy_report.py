import os
import sys
from pathlib import Path

import requests
import yaml

tenant_id = 'cef04b19-7776-4a94-b89b-375c77a8f936'


def main():
    with open('deploy_config.yaml', 'r') as yml_file:
        cfg = yaml.safe_load(yml_file)

    data = {
        'client_id': os.environ['CLIENT_ID'],
        'grant_type': 'client_credentials',
        'resource': 'https://analysis.windows.net/powerbi/api',
        'response_mode': 'query',
        'client_secret': os.environ['CLIENT_SECRET']
    }

    resp = requests.get('https://login.microsoftonline.com/{}/oauth2/token'.format(tenant_id), data=data)
    access_token = resp.json()['access_token']
    token = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    for file in sys.argv:
        if file.endswith('.pbix'):
            path = Path(file)
            workspace = os.path.basename(path.parent.absolute())
            file_name = os.path.basename(file)
            display_name = file_name.replace('_', ' ')
            workspace_id = cfg[workspace]
            print('Deploying {} to {}'.format(file_name, workspace))
            file_import = {'file': open(file, 'rb')}
            response = requests.request("POST",
                                        "https://api.powerbi.com/v1.0/myorg/groups/{}/imports?datasetDisplayName={}"
                                        .format(workspace_id, display_name), files=file_import, headers=token)

            if response.status_code not in [200, 201, 202, 204]:
                raise Exception('ERROR: {}: {}\nURL: {}'.format(response.status_code, response.content, response.url))


if __name__ == '__main__':
    main()
