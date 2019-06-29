#!/usr/bin/env python3
import argparse

from downloader import download_exercises
from constants import (
    ALLOWED_STATUSES,
    ALLOWED_DIFFICULTIES,
    ALLOWED_GROUPS
)

description = 'This is exercism-cli wrapper allowing to bulk download exercism exercises based on given conditions.'
parser = argparse.ArgumentParser(description=description)

parser.add_argument('tracks', type=tuple, metavar='', nargs='*', help=f'tracks you want to download exercises from. If not provided all accessible exercises from all accessible tracks will be downloaded.')
parser.add_argument('-g', '--group', type=str, metavar='', required=False, help=f'allowed values: {", ".join(ALLOWED_GROUPS)}. If not provided all accessible exercises from all accessible groups will be downloaded.')
parser.add_argument('-d', '--difficulty', type=str, metavar='', required=False, help=f'allowed values: {", ".join(ALLOWED_DIFFICULTIES)}. If not provided all accessible exercises of all difficulties will be downloaded.')
parser.add_argument('-s', '--status', type=str, metavar='', required=False, help=f'allowed values: {", ".join(ALLOWED_STATUSES)}. If not provided all accessible exercises of all statuses will be downloaded.')
parser.add_argument('-e', '--email', type=str, metavar='', required=False, help='your email to log in to exercism account. If not provided you can filter by track and/or difficulty only.')
parser.add_argument('-p', '--password', type=str, metavar='', required=False, help='your password to log in to exercism account. If not provided you can filter by track and/or difficulty only.')

args = parser.parse_args()


if __name__ == '__main__':
    download_exercises(
        *args.tracks,
        group=args.group,
        difficulty=args.difficulty,
        status=args.status,
        email=args.email,
        password=args.password
    )

    print('done')
