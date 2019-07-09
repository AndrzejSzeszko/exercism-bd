import os
import json
import requests

from utils.executives import (
    log_in,
    get_all_tracks,
    get_my_tracks,
    get_exercises_not_logged_in,
    get_exercises_logged_in,
    run_exercism_download,
    get_exercism_workspace_path,
    intercept_credentials,
    get_credentials
)


def download_exercises(tracks=None, group=None, difficulty=None, status=None):
    session = requests.Session()
    tracks = tracks if tracks else get_all_tracks()
    exercises_not_logged_in = get_exercises_not_logged_in(session, tracks)

    user_logged_in = False
    if status or group:
        email, password = get_credentials()
        
        user_logged_in = log_in(session, email, password)
        if not user_logged_in:
            print('Check if you provided correct credentials (when prompted or via configuration file). \n')
            return

        exercises_logged_in = get_exercises_logged_in(session, tracks, exercises_not_logged_in)

    exercises_by_track = exercises_logged_in if user_logged_in else exercises_not_logged_in
    run_exercism_download(exercises_by_track, group, difficulty, status)

    print('done')


def list_all_tracks():
    for track in get_all_tracks():
        print(track)


def list_my_tracks():
    email, password = get_credentials()

    for track in get_my_tracks(email, password):
        print(track)


def configure():
    email, password = intercept_credentials()

    session = requests.Session()
    user_logged_in = log_in(session, email, password)
    if not user_logged_in:
        print('Check if you provided correct credentials when prompted. \n')
        return

    exercism_workspace_path = get_exercism_workspace_path()
    config_file_path = os.path.join(exercism_workspace_path, 'exercism-bd', '.config.json')
    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)

    with open(config_file_path, 'w+') as config_file:
        config_file.seek(0)
        config_file.truncate()

        config_data = {'email': email, 'password': password}
        json.dump(config_data, config_file, indent=4)

    print('\nEmail and password saved.\n')
