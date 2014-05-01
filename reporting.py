#!/usr/bin/python
# -*- coding: utf-8 -*-

from itertools import chain
import argparse
import sys

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

from utils import get_flags
from utils import get_service
from utils import create_dat_file

_APP_NAME = 'analytics'
_APP_SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'

_START_DATE = '2014-04-01'
_END_DATE = '2014-04-30'
_START_INDEX = '1'
_MAX_RESULTS = '50'


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'table_id',
    type=str,
    help=(
        'The table ID of the profile you wish to access. '
        'Format is ga:xxx where xxx is your profile ID.'
    )
)
argparser.add_argument('action', type=str)
argparser.add_argument('label', type=str)


def main(argv):
    flags = get_flags(argv, __doc__, argparser)

    print_result(
        get_total_events(
            flags.table_id,
            flags.label,
            flags.action
        ),
        flags.action,
    )


def print_result(results, msg):
    if 'rows' not in results.keys():
        value = 0
    else:
        value = list(chain.from_iterable(results['rows']))[0]

    print "{}: {}".format(msg, value)


def get_total_events(table_id, label, action):
    service = get_service(_APP_NAME, 'v3')

    try:
        filter_ = \
            'ga:eventCategory==Marketplace;' \
            'ga:eventAction=={};' \
            'ga:eventLabel=={}' \
            .format(
                action,
                label,
            )

        results = service.data().ga().get(
            ids=table_id,
            start_date=_START_DATE,
            end_date=_END_DATE,
            metrics='ga:totalEvents',
            filters=filter_,
            start_index=_START_INDEX,
            max_results=_MAX_RESULTS,
        )

        results = results.execute()
    except TypeError, error:
        print ('There was an error in constructing your query : %s' % error)
    except HttpError, error:
        print (
            'Arg, there was an API error : %s : %s' %
            (error.resp.status, error._get_reason())
        )
    except AccessTokenRefreshError:
        print (
            'The credentials have been revoked or expired, please re-run '
            'the application to re-authorize'
        )
    else:
        return results


if __name__ == '__main__':
    try:
        open('{}.dat'.format(_APP_NAME))
    except IOError:
        create_dat_file(
            sys.argv,
            _APP_NAME,
            __doc__,
            __file__,
            scope=_APP_SCOPE,
            parents=[argparser],
        )

    main(sys.argv)
