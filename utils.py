from os.path import dirname as get_dirname
from os.path import join as join_path
import argparse
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import file
from oauth2client import tools


def get_flags(argv, doc, parents):
    parent_parsers = [tools.argparser]
    parent_parsers.extend([parents])
    parser = argparse.ArgumentParser(
        description=doc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers
    )
    flags = parser.parse_args(argv[1:])
    return flags


def get_service(name, version):
    storage = file.Storage(name + '.dat')
    credentials = storage.get()

    http = credentials.authorize(http=httplib2.Http())

    service = discovery.build(name, version, http=http)
    return service


def create_dat_file(argv, name, doc, filename, scope, parents=[]):
    parent_parsers = [tools.argparser]
    parent_parsers.extend(parents)
    parser = argparse.ArgumentParser(
        description=doc,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers,
    )
    flags = parser.parse_args(argv[1:])

    client_secrets = join_path(get_dirname(filename), 'client_secrets.json')

    flow = client.flow_from_clientsecrets(
        client_secrets,
        scope=scope,
        message=tools.message_if_missing(client_secrets),
    )

    storage = file.Storage(name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
