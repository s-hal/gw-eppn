import logging
import argparse
import yaml
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


LOGGER = logging.getLogger(__name__)

def get_config(file):
    with open(file, encoding='utf-8') as f:
        return yaml.safe_load(f.read())


def authn(config):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(config['token'], config['scopes'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config['csf'], config['scopes'])
            creds = flow.run_local_server(port=0)
        with open(config['token'], 'w') as token:
            token.write(creds.to_json())
    return creds


def increase(s):
    a = '0123456789abcdefghijklmnopqrstuvwxyz'
    if not s:
        return "1"
    else:
        new_s = []
        continue_change = True
        for c in s[::-1].lower():
            if continue_change:
                if c == 'z':
                    new_s.insert(0, '0')
                else:
                    new_s.insert(0, a[a.index(c) + 1])
                    continue_change = False
            else:
                new_s.insert(0, c)
        return ''.join(new_s)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file")
    parser.add_argument("--log-level",
                        dest='log_level',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO',
                        help="set the log level, default=INFO")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--eppn', action='store_const', const=True)
    group.add_argument('--schema', action='store_const', const=True)
    parser.set_defaults(feature=False)
    return  parser.parse_args()


def add_schema(config, service):
    slist = service.schemas().list(customerId=config['customer_id'], fields='schemas/schemaName').execute()
    try:
        sunique = set(n for s in slist['schemas'] for n in s.values())
    except KeyError:
        sunique = ()

    for schema in config['schemas']:
        if schema['schemaName'] not in sunique:
            service.schemas().insert(customerId=config['customer_id'], body=schema).execute()


def add_eppn(config, service):
    results = service.users().list(customer=config['customer_id'],
                                   projection='custom',
                                   customFieldMask=config['schema_name'],
                                   query=config['search_query']).execute()

    users = results.get('users', [])

    if users:
        high_eppn = ''
        no_eppn = []
        for user in users:
            try:
                if high_eppn < user['customSchemas'][config['schema_name']]['eduPersonPrincipalName'].lower().split("@")[0]:
                    high_eppn = user['customSchemas'][config['schema_name']]['eduPersonPrincipalName'].lower().split("@")[0]
            except KeyError:
                no_eppn.append(user['id'])

        for u in no_eppn:
            high_eppn = increase(high_eppn).zfill(config['mlen'])
            if len(high_eppn) > config['mlen']:
                raise ValueError("ePPN exceeds maximum length")

            user_patch_params = {
                'userKey': u,
                'body': {
                    'customSchemas': {
                        config['schema_name']: {
                            'eduPersonPrincipalName': f"{high_eppn}@{config['scope']}" if 'scope' in config else high_eppn
                        },
                    },
                },
            }
            service.users().patch(**user_patch_params).execute()

def main():
    args = get_args()
    config = get_config(args.config)

    service = build('admin', 'directory_v1', credentials=authn(config))
    if args.schema:
        add_schema(config, service)
    elif args.eppn:
        add_eppn(config, service)


if __name__ == '__main__':
    main()