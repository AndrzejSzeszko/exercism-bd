import os
import json
import requests

from json.decoder import JSONDecodeError
from constants import CANNOT_READ_CONFIG_FILE_MESSAGE
from utils import (
    log_in,
    get_all_tracks,
    get_my_tracks,
    get_exercises_not_logged_in,
    get_exercises_logged_in,
    run_exercism_download,
    get_exercism_workspace_path,
    get_credentials_from_config_file
)


def download_exercises(tracks=None, group=None, difficulty=None, status=None, email=None, password=None):
    session = requests.Session()
    tracks = tracks if tracks else get_all_tracks()
    exercises_not_logged_in = get_exercises_not_logged_in(session, tracks)

    user_logged_in = False
    if email or password:
        user_logged_in = log_in(session, email, password)
        if not user_logged_in:
            return
        exercises_logged_in = get_exercises_logged_in(session, tracks, exercises_not_logged_in)

    exercises_by_track = exercises_logged_in if user_logged_in else exercises_not_logged_in
    run_exercism_download(exercises_by_track, group, difficulty, status)

    print('done')


def list_all_tracks():
    for track in get_all_tracks():
        print(track)


def list_my_tracks(email, password):
    if not (email and password):
        try:
            email, password = get_credentials_from_config_file()
        except (FileNotFoundError, JSONDecodeError):
            print(CANNOT_READ_CONFIG_FILE_MESSAGE)
            return

    for track in get_my_tracks(email, password):
        print(track)


def configure(email, password):
    exercism_workspace_path = get_exercism_workspace_path()
    exercism_bd_workspace_path = os.path.join(exercism_workspace_path, 'exercism-bd')
    os.makedirs(exercism_bd_workspace_path, exist_ok=True)
    config_file_path = os.path.join(exercism_bd_workspace_path, 'config.json')

    with open(config_file_path, 'w+') as config_file:
        config_file.seek(0)
        config_file.truncate()

        config_data = {'email': email, 'password': password}
        json.dump(config_data, config_file, indent=4)

    print('Email and password saved.\n')
