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

description          = '-------------------------------------------------------------------------------------------------------------------------\n' \
                       'This is exercism-cli wrapper allowing to bulk download exercism exercises based on given conditions. \n' \
                       'You have to have official exercism-cli installed and configured first (https://exercism.io/cli-walkthrough). \n' \
                       '\n' \
                       'Source code: https://github.com/AndrzejSzeszko/exercism-bd\n' \
                       '-------------------------------------------------------------------------------------------------------------------------\n' \
                       '\n' \
                       'EXAMPLES OF USE:\n' \
                       '\n' \
                       'exercism-bd -t python javascript -d easy   -->   downloads all easy exercises form python and javascript tracks \n' \
                       '\n' \
                       'exercism-bd -g side -s unlocked -e dummy@email.com -p dummypass   -->   downloads unlocked side exercises from all tracks \n' \
                       '\n' \
                       'exercism-bd --list_my_tracks -e dummy@email.com -p dummypass   -->   lists tracks you joined \n' \
                       '\n' \
                       '-------------------------------------------------------------------------------------------------------------------------'

tracks_help          = 'Filter exercises by track.\n' \
                       'If not provided, all accessible exercises from all accessible tracks will be downloaded.\n' \
                       'To list all existing tracks run: exercism-bd --list-all-tracks.\n' \
                       'To list tracks you joined run: exercism-bd --list-my-tracks.\n '

group_help           = f'Filter exercises by group. Allowed values: {", ".join(ALLOWED_GROUPS)}.\n' \
                       f'If not provided, all accessible exercises from all accessible groups will be downloaded.\n '

difficulty_help      = f'Filter exercises by difficulty. Allowed values: {", ".join(ALLOWED_DIFFICULTIES)}.\n' \
                       f'If not provided, all accessible exercises of all difficulties will be downloaded.\n '

status_help          = f'Filter exercises by status. Allowed values: {", ".join(set(ALLOWED_STATUSES.values()))}.\n' \
                       f'If not provided, all accessible exercises of all statuses will be downloaded.\n '

email_help           = 'Email to log in to your exercism account.\n' \
                       'If not provided, you won\'t be allowed to filter by status or group.\n '

password_help        = 'Password to log in to your exercism account.\n' \
                       'If not provided, you won\'t be allowed to filter by status or group.\n '

list_all_tracks_help = 'List all currently existing tracks.\n '

list_my_tracks_help  = 'List tracks you joined. Requires authentication (see "Examples of use" above).\n '

help_help            = 'Show this help message and exit.\n '


parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawTextHelpFormatter,
    prog='exercism-bd',
    add_help=False,
)

auxiliary_group = parser.add_argument_group('AUXILIARY options')
auxiliary_group.add_argument('-h', '--help', required=False, action='store_true', help=help_help)
auxiliary_group.add_argument('--list-all-tracks', required=False, action='store_true', help=list_all_tracks_help)
auxiliary_group.add_argument('--list-my-tracks', required=False, action='store_true', help=list_my_tracks_help)

no_auth_needed_group = parser.add_argument_group('FILTERING options that CAN be used without authentication')
no_auth_needed_group.add_argument('-t', '--tracks', type=str, metavar='TRACK', required=False, nargs='*', help=tracks_help, )
no_auth_needed_group.add_argument('-d', '--difficulty', type=str, metavar='DIFFICULTY', choices=ALLOWED_DIFFICULTIES, required=False, help=difficulty_help)

auth_needed_group = parser.add_argument_group('FILTERING options that CANNOT be used without authentication')
auth_needed_group.add_argument('-g', '--group', type=str, metavar='GROUP', choices=ALLOWED_GROUPS, required=False, help=group_help)
auth_needed_group.add_argument('-s', '--status', type=str, metavar='STATUS', required=False, help=status_help)

authentication_group = parser.add_argument_group('AUTHENTICATION')
authentication_group.add_argument('-e', '--email', type=str, metavar='EMAIL', required=False, help=email_help)
authentication_group.add_argument('-p', '--password', type=str, metavar='PASSWORD', required=False, help=password_help)

args = parser.parse_args()


if __name__ == '__main__':
    

    if args.help:
        parser.print_help()

    elif args.list_all_tracks:
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
