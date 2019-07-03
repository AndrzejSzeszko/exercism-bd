#!/usr/bin/env python3
import argparse

from downloader import download_exercises
from constants import (
    ALLOWED_STATUSES,
    ALLOWED_DIFFICULTIES,
    ALLOWED_GROUPS
)

description     = 'This is exercism-cli wrapper allowing to bulk download exercism exercises based on given conditions. \n\n' \
                  '-------------------------------------------------------------------------------------------------------------------------\n' \
                  '\n' \
                  'Examples of use:\n' \
                  '\n' \
                  'exercism-bd -t python javascript -d easy   -->   downloads all easy exercises form python and javascript tracks \n' \
                  '\n' \
                  'exercism-bd -g side -s unlocked -e dummy@email.com -p dummypass   -->   downloads unlocked side exercises from all tracks \n' \
                  '\n' \
                  '-------------------------------------------------------------------------------------------------------------------------'

tracks_help     = 'Tracks you want to download exercises from.\n' \
                  'If not provided, all accessible exercises from all accessible tracks will be downloaded.\n '

group_help      = f'Allowed values: {", ".join(ALLOWED_GROUPS)}.\n' \
                  f'If not provided, all accessible exercises from all accessible groups will be downloaded.\n '

difficulty_help = f'Allowed values: {", ".join(ALLOWED_DIFFICULTIES)}.\n' \
                  f'If not provided, all accessible exercises of all difficulties will be downloaded.\n '

status_help     = f'Allowed values: {", ".join(ALLOWED_STATUSES)}.\n' \
                  f'If not provided, all accessible exercises of all statuses will be downloaded.\n '

email_help      = 'Email to log in to your exercism account.\n' \
                  'If not provided, you won\'t be allowed to filter by status or group.\n '

password_help   = 'Password to log in to your exercism account.\n' \
                  'If not provided, you won\'t be allowed to filter by status or group.\n '


parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-t', '--tracks', type=str, metavar='', required=False, nargs='*', help=tracks_help, )
parser.add_argument('-g', '--group', type=str, metavar='', required=False, help=group_help)
parser.add_argument('-d', '--difficulty', type=str, metavar='', required=False, help=difficulty_help)
parser.add_argument('-s', '--status', type=str, metavar='', required=False, help=status_help)
parser.add_argument('-e', '--email', type=str, metavar='', required=False, help=email_help)
parser.add_argument('-p', '--password', type=str, metavar='', required=False, help=password_help)

args = parser.parse_args()


if __name__ == '__main__':
    download_exercises(
        tracks=args.tracks,
        group=args.group,
        difficulty=args.difficulty,
        status=args.status,
        email=args.email,
        password=args.password
    )

    print('done')
