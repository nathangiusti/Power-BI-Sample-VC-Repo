import os

import requests

tenant_id = 'cef04b19-7776-4a94-b89b-375c77a8f936'


def main():

    data = {
        'client_id': os.environ['CLIENT_ID'],
        'grant_type': 'client_credentials',
        'resource': 'https://analysis.windows.net/powerbi/api',
        'response_mode': 'query',
        'client_secret': os.environ['SECRET']
    }
    resp = requests.get('https://login.microsoftonline.com/{}/oauth2/token'.format(tenant_id), data=data)

    access_token = resp.json()['access_token']

    print(access_token)
    