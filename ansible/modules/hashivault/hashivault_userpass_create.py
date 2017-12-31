#!/usr/bin/env python
DOCUMENTATION = '''
---
module: hashivault_userpass_create
version_added: "2.2.0"
short_description: Hashicorp Vault userpass create module
description:
    - Module to create userpass users in Hashicorp Vault.
options:
    url:
        description:
            - url for vault
        default: to environment variable VAULT_ADDR
    ca_cert:
        description:
            - "path to a PEM-encoded CA cert file to use to verify the Vault server TLS certificate"
        default: to environment variable VAULT_CACERT
    ca_path:
        description:
            - "path to a directory of PEM-encoded CA cert files to verify the Vault server TLS certificate : if ca_cert is specified, its value will take precedence"
        default: to environment variable VAULT_CAPATH
    client_cert:
        description:
            - "path to a PEM-encoded client certificate for TLS authentication to the Vault server"
        default: to environment variable VAULT_CLIENT_CERT
    client_key:
        description:
            - "path to an unencrypted PEM-encoded private key matching the client certificate"
        default: to environment variable VAULT_CLIENT_KEY
    verify:
        description:
            - "if set, do not verify presented TLS certificate before communicating with Vault server : setting this variable is not recommended except during testing"
        default: to environment variable VAULT_SKIP_VERIFY
    authtype:
        description:
            - "authentication type to use: token, userpass, github, ldap"
        default: token
    token:
        description:
            - token for vault
        default: to environment variable VAULT_TOKEN
    username:
        description:
            - username to login to vault.
        default: to environment variable VAULT_USER
    password:
        description:
            - password to login to vault.
        default: to environment variable VAULT_PASSWORD
    name:
        description:
            - user name to create.
    pass:
        description:
            - user to create password.
    policies:
        description:
            - user policies.
        default: default
'''
EXAMPLES = '''
---
- hosts: localhost
  tasks:
    - hashivault_userpass_create:
      name: 'bob'
      pass: 'S3cre7s'
      policies: 'bob'
'''


def main():
    argspec = hashivault_argspec()
    argspec['name'] = dict(required=True, type='str')
    argspec['pass'] = dict(required=True, type='str')
    argspec['policies'] = dict(required=False, type='str', default='default')
    module = hashivault_init(argspec)
    result = hashivault_userpass_create(module.params)
    if result.get('failed'):
        module.fail_json(**result)
    else:
        module.exit_json(**result)


from ansible.module_utils.basic import *
from ansible.module_utils.hashivault import *


@hashiwrapper
def hashivault_userpass_create(params):
    client = hashivault_auth_client(params)
    name = params.get('name')
    password = params.get('pass')
    policies = params.get('policies')
    client.create_userpass(name, password, policies)
    return {'changed': True}


if __name__ == '__main__':
    main()
