#!/usr/bin/env python3
import argparse

from executives import (
    download_exercises,
    list_all_tracks,
    list_my_tracks,
    configure
)
from constants import (
    ALLOWED_STATUSES,
    ALLOWED_DIFFICULTIES,
    ALLOWED_GROUPS
)

description          = '------------------------------------------------------------------------------------------------------------------------\n' \
                       'This is exercism-cli wrapper allowing to bulk download exercism exercises based on given conditions. \n' \
                       'You have to have official exercism-cli installed and configured first (https://exercism.io/cli-walkthrough). \n' \
                       '\n' \
                       'Source code: https://github.com/AndrzejSzeszko/exercism-bd\n' \
                       '------------------------------------------------------------------------------------------------------------------------\n' \
                       '\n' \
                       'EXAMPLES OF USE:\n' \
                       '\n' \
                       'exercism-bd -c   -->   Stores you email and password on your local machine (provide credentials to save when prompted). \n' \
                       '\n' \
                       'exercism-bd -t python javascript -d easy   -->   Downloads all easy exercises form python and javascript tracks. \n' \
                       '\n' \
                       'exercism-bd -g side -s unlocked   -->   Downloads unlocked side exercises from all tracks. \n' \
                       '\n' \
                       'exercism-bd --list_my_tracks   -->   Lists tracks you joined. \n' \
                       '\n' \
                       '------------------------------------------------------------------------------------------------------------------------'

tracks_help          = 'Filter exercises by track.\n' \
                       'To list all existing tracks run: exercism-bd --list-all-tracks.\n' \
                       'To list tracks you joined run: exercism-bd --list-my-tracks.\n' \
                       'If not provided, all accessible exercises from all accessible tracks will be downloaded.\n '

difficulty_help      = f'Filter exercises by difficulty. Allowed values: {", ".join(ALLOWED_DIFFICULTIES)}.\n' \
                       f'If not provided, all accessible exercises of all difficulties will be downloaded.\n '

group_help           = f'Filter exercises by group. Allowed values: {", ".join(ALLOWED_GROUPS)}.\n' \
                       f'If not provided, all accessible exercises from all accessible groups will be downloaded.\n' \
                       f'Requires authentication. If you are sick of typing your credentials everytime they are needed, \n' \
                       f'run exercism-bd -c to store them on your local machine.\n '

status_help          = f'Filter exercises by status. Allowed values: {", ".join(set(ALLOWED_STATUSES.values()))}.\n' \
                       f'If not provided, all accessible exercises of all statuses will be downloaded.\n' \
                       f'Requires authentication. If you are sick of typing your credentials everytime they are needed, \n' \
                       f'run exercism-bd -c to store them on your local machine.\n '

list_all_tracks_help = 'List all currently existing tracks.\n '

list_my_tracks_help  = 'List tracks you joined.\n' \
                       'Requires authentication. If you are sick of typing your credentials everytime they are needed, \n' \
                       'run exercism-bd -c to store them on your local machine.\n '

help_help            = 'Show this help message and exit.\n '

configure_help       = 'Store your email and password on your local machine.\n '


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

filtering_group = parser.add_argument_group('FILTERING options')
filtering_group.add_argument('-t', '--tracks', type=str, metavar='TRACK', required=False, nargs='*', help=tracks_help, )
filtering_group.add_argument('-d', '--difficulty', type=str, metavar='DIFFICULTY', choices=ALLOWED_DIFFICULTIES, required=False, help=difficulty_help)
filtering_group.add_argument('-g', '--group', type=str, metavar='GROUP', choices=ALLOWED_GROUPS, required=False, help=group_help)
filtering_group.add_argument('-s', '--status', type=str, metavar='STATUS', choices=set(ALLOWED_STATUSES.values()), required=False, help=status_help)

configuration_group = parser.add_argument_group('CONFIGURATION options')
configuration_group.add_argument('-c', '--configure', required=False, action='store_true', help=configure_help)

args = parser.parse_args()


if __name__ == '__main__':
    if args.help:
        parser.print_help()

    elif args.list_all_tracks:
        list_all_tracks()

    elif args.list_my_tracks:
        list_my_tracks()

    elif args.configure:
        configure()

    else:
        download_exercises(
            tracks=args.tracks,
            group=args.group,
            difficulty=args.difficulty,
            status=args.status
        )
