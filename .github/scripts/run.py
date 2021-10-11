import os
import sys

import requests

tenant_id = 'cef04b19-7776-4a94-b89b-375c77a8f936'
bi_360_dev = '35b552e9-32c3-47ec-938c-2f30e026f2a6'


def main():

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
            file_import = {'file': open(file, 'rb')}
            requests.request("POST", "https://api.powerbi.com/v1.0/myorg/groups/{}/imports".format(bi_360_dev),
                             files=file_import, headers=token)

    print(access_token)

if __name__ == '__main__':
    main()