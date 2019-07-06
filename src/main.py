#!/usr/bin/env python3
import argparse

from executives import (
    download_exercises,
    list_all_tracks,
    list_my_tracks
)
from constants import (
    ALLOWED_STATUSES,
    ALLOWED_DIFFICULTIES,
    ALLOWED_GROUPS
)

description          = 'This is exercism-cli wrapper allowing to bulk download exercism exercises based on given conditions. \n\n' \
                       '-------------------------------------------------------------------------------------------------------------------------\n' \
                       '\n' \
                       'Examples of use:\n' \
                       '\n' \
                       'exercism-bd -t python javascript -d easy   -->   downloads all easy exercises form python and javascript tracks \n' \
                       '\n' \
                       'exercism-bd -g side -s unlocked -e dummy@email.com -p dummypass   -->   downloads unlocked side exercises from all tracks \n' \
                       '\n' \
                       '-------------------------------------------------------------------------------------------------------------------------'

tracks_help          = 'Tracks you want to download exercises from.\n' \
                       'To list all available tracks run: exercism-bd --list-all-tracks.\n' \
                       'If not provided, all accessible exercises from all accessible tracks will be downloaded.\n '

group_help           = f'Allowed values: {", ".join(ALLOWED_GROUPS)}.\n' \
                       f'If not provided, all accessible exercises from all accessible groups will be downloaded.\n '

difficulty_help      = f'Allowed values: {", ".join(ALLOWED_DIFFICULTIES)}.\n' \
                       f'If not provided, all accessible exercises of all difficulties will be downloaded.\n '

status_help          = f'Allowed values: {", ".join(set(ALLOWED_STATUSES.values()))}.\n' \
                       f'If not provided, all accessible exercises of all statuses will be downloaded.\n '

email_help           = 'Email to log in to your exercism account.\n' \
                       'If not provided, you won\'t be allowed to filter by status or group.\n '

password_help        = 'Password to log in to your exercism account.\n' \
                       'If not provided, you won\'t be allowed to filter by status or group.\n '

list_all_tracks_help = 'Lists all currently available tracks.\n '

list_my_tracks_help  = 'Lists tracks you joined.\n '


parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--list-all-tracks', required=False, action='store_true', help=list_all_tracks_help)

no_auth_needed_group = parser.add_argument_group('filtering options that can be used without authentication')
no_auth_needed_group.add_argument('-t', '--tracks', type=str, metavar='', required=False, nargs='*', help=tracks_help, )
no_auth_needed_group.add_argument('-d', '--difficulty', type=str, metavar='', choices=ALLOWED_DIFFICULTIES, required=False, help=difficulty_help)

auth_needed_group = parser.add_argument_group('filtering options that cannot be used without authentication')
auth_needed_group.add_argument('-g', '--group', type=str, metavar='', choices=ALLOWED_GROUPS, required=False, help=group_help)
auth_needed_group.add_argument('-s', '--status', type=str, metavar='', required=False, help=status_help)
auth_needed_group.add_argument('--list-my-tracks', required=False, action='store_true', help=list_my_tracks_help)

authentication_group = parser.add_argument_group('authentication')
authentication_group.add_argument('-e', '--email', type=str, metavar='', required=False, help=email_help)
authentication_group.add_argument('-p', '--password', type=str, metavar='', required=False, help=password_help)

args = parser.parse_args()


if __name__ == '__main__':
    if args.list_all_tracks:
        list_all_tracks()

    elif args.list_my_tracks:
        list_my_tracks(args.email, args.password)

    else:
        download_exercises(
            tracks=args.tracks,
            group=args.group,
            difficulty=args.difficulty,
            status=args.status,
            email=args.email,
            password=args.password
        )
