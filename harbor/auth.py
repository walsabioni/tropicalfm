#!/bin/sh
"true" '''\'
VENV_PYTHON=$(dirname "$0")/venv/bin/python

if [ -x $VENV_PYTHON ]; then
    exec $VENV_PYTHON "$0" "$@"
else
    exec python3 "$0" "$@"
fi
'''

import argparse
from collections import OrderedDict
import datetime
import json
import pickle
import pprint
import os
import sys

from dateutil.parser import parse as dateutil_parse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz


SHEET_TIMEZONE = pytz.timezone('US/Pacific')
USER_DATA_CACHE_FILE = os.path.join(os.path.dirname(__file__), 'user-data.pkl')
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
if not os.path.exists(CREDENTIALS_FILE):
    print(f'No Google credentials file found at {CREDENTIALS_FILE}. Exiting.')
    sys.exit(1)


def sanitize_password(password):
    return password.lower().strip()


def get_and_cache_user_data(sheet_key):
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/drive',
    ])
    client = gspread.authorize(creds)
    data = OrderedDict()

    sheet = client.open_by_key(sheet_key).sheet1
    rows = sheet.get_all_values()

    headers = ('name', 'start', 'end', 'password')
    for header_row, row in enumerate(rows):
        if all(header in row[column].lower() for column, header in enumerate(headers)):
            break
    else:
        print("Couldn't find header row.")
        sys.exit(1)

    for name, start, end, password, *_ in rows[header_row + 1:]:
        try:
            start = SHEET_TIMEZONE.localize(dateutil_parse(start))
            end = SHEET_TIMEZONE.localize(dateutil_parse(end))
        except ValueError:
            pass
        else:
            password = sanitize_password(password)
            if password:
                data[password] = OrderedDict((('name', name or 'unknown'), ('start', start), ('end', end)))

    with open(USER_DATA_CACHE_FILE, 'wb') as cache_file:
        pickle.dump(data, cache_file)

    return data


def auth_data(user_data, password, date, grace=0):
    data = OrderedDict((('authorized', False), ('valid_user', False)))

    user_data = user_data.get(sanitize_password(password))
    if user_data is not None:
        data['valid_user'] = True
        for key, value in user_data.items():
            data[key] = str(value)
        start = user_data['start'] - datetime.timedelta(seconds=grace)
        end = user_data['end'] + datetime.timedelta(seconds=grace)
        data['start_with_grace_period'], data['end_with_grace_period'] = str(start), str(end)
        data['authorized'] = start <= date <= end
        data['seconds_to_kickoff'] = round((end - date).total_seconds()) if data['authorized'] else -1

    return data


def main():
    parser = argparse.ArgumentParser(description='harbor authentication script')
    parser.add_argument('password', help='password to check (if left blank, download and cache)', nargs='?')
    parser.add_argument('-k', '--sheet-key', help='google sheet key', required=True)
    parser.add_argument('--timezone', help='timezone (default: US/Pacific)', default='US/Pacific')
    parser.add_argument('-d', '--date', help='date and time to check (default: now)')
    parser.add_argument('-f', '--force', help="force a download when checking password (don't use cache)")
    parser.add_argument('-g', '--grace-period', type=int, default=90, help='grace period in seconds (default: 90)')
    parser.add_argument('--dump', action='store_true', help='dump all user data')

    args = parser.parse_args()

    if args.force or not args.password or not os.path.exists(USER_DATA_CACHE_FILE):
        user_data = get_and_cache_user_data(sheet_key=args.sheet_key)
    else:
        with open(USER_DATA_CACHE_FILE, 'rb') as cache_file:
            user_data = pickle.load(cache_file)

    if args.dump:
        pprint.pprint(user_data)
    elif args.password:
        timezone = pytz.timezone(args.timezone)
        if args.date:
            date = timezone.localize(dateutil_parse(args.date, fuzzy=True).replace(tzinfo=None))
        else:
            date = datetime.datetime.now(timezone)

        data = auth_data(user_data=user_data, password=args.password, date=date, grace=args.grace_period)
        print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()