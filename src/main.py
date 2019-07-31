#!/usr/bin/env python3
import argparse

from utils.executives import get_all_tracks
from utils.ui import (
    bold,
    underline
)
from clint.textui import colored
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

allowed_statuses = underline(bold(", ".join(set(ALLOWED_STATUSES.values()))))
allowed_difficulties = underline(bold(", ".join(ALLOWED_DIFFICULTIES)))
allowed_groups = underline(bold(", ".join(ALLOWED_GROUPS)))

description          = f'------------------------------------------------------------------------------------------------------------------------\n' \
                       f'This is exercism-cli wrapper allowing to bulk download exercism exercises based on given conditions. \n' \
                       f'You have to have official exercism-cli installed and configured first ({colored.blue("https://exercism.io/cli-walkthrough")}). \n' \
                       f'\n' \
                       f'Source code: {colored.blue("https://github.com/AndrzejSzeszko/exercism-bd")}\n' \
                       f'------------------------------------------------------------------------------------------------------------------------\n' \
                       f'\n' \
                       f'{bold("EXAMPLES OF USE")}:\n' \
                       f'\n' \
                       f'{bold("exercism-bd -c")}   -->   Stores you email and password on your local machine (provide credentials to save when prompted). \n' \
                       f'\n' \
                       f'{bold("exercism-bd -t python javascript -d easy")}    -->   Downloads all easy exercises form python and javascript tracks. \n' \
                       f'\n' \
                       f'{bold("exercism-bd -g side -s unlocked")}    -->   Downloads unlocked side exercises from all tracks. \n' \
                       f'\n' \
                       f'{bold("exercism-bd --list_my_tracks")}    -->   Lists tracks you joined. \n' \
                       f'\n' \
                       f'------------------------------------------------------------------------------------------------------------------------'

tracks_help          = f'Filter exercises by track.\n' \
                       f'To list all existing tracks run: {bold("exercism-bd --list-all-tracks")}.\n' \
                       f'To list tracks you joined run: {bold("exercism-bd --list-my-tracks")}.\n' \
                       f'If not provided, all accessible exercises from all accessible tracks will be downloaded.\n '

difficulty_help      = f'Filter exercises by difficulty. Allowed values: {allowed_difficulties}.\n' \
                       f'If not provided, all accessible exercises of all difficulties will be downloaded.\n '

group_help           = f'Filter exercises by group. Allowed values: {allowed_groups}.\n' \
                       f'If not provided, all accessible exercises from all accessible groups will be downloaded.\n' \
                       f'Requires authentication. If you are sick of typing your credentials everytime they are needed, \n' \
                       f'run exercism-bd -c to store them on your local machine.\n '

status_help          = f'Filter exercises by status. Allowed values: {allowed_statuses}.\n' \
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

auxiliary_group = parser.add_argument_group(bold('AUXILIARY OPTIONS'))
auxiliary_group.add_argument(
    '-h',
    '--help',
    required=False,
    action='store_true',
    help=help_help
)
auxiliary_group.add_argument(
    '--list-all-tracks',
    required=False,
    action='store_true',
    help=list_all_tracks_help
)
auxiliary_group.add_argument(
    '--list-my-tracks',
    required=False,
    action='store_true',
    help=list_my_tracks_help
)

filtering_group = parser.add_argument_group(bold('FILTERING OPTIONS'))
filtering_group.add_argument(
    '-t',
    '--tracks',
    type=str,
    metavar='TRACK',
    # choices=get_all_tracks(),
    required=False,
    nargs='*',
    help=tracks_help,
)
filtering_group.add_argument(
    '-d',
    '--difficulty',
    type=str,
    metavar='DIFFICULTY',
    choices=ALLOWED_DIFFICULTIES,
    required=False,
    help=difficulty_help
)
filtering_group.add_argument(
    '-g',
    '--group',
    type=str,
    metavar='GROUP',
    choices=ALLOWED_GROUPS,
    required=False,
    help=group_help
)
filtering_group.add_argument(
    '-s',
    '--status',
    type=str,
    metavar='STATUS',
    choices=set(ALLOWED_STATUSES.values()),
    required=False,
    help=status_help
)

configuration_group = parser.add_argument_group(bold('CONFIGURATION OPTIONS'))
configuration_group.add_argument(
    '-c',
    '--configure',
    required=False,
    action='store_true',
    help=configure_help
)

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

    # download_exercises(
    #     tracks=['java'],
    #     group=args.group,
    #     difficulty=args.difficulty,
    #     status=args.status
    # )
