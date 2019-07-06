import requests

from utils import (
    log_in,
    get_all_tracks,
    get_my_tracks,
    get_exercises_not_logged_in,
    get_exercises_logged_in,
    run_exercism_download
)


def download_exercises(tracks=None, group=None, difficulty=None, status=None, email=None, password=None):
    session = requests.Session()
    tracks = tracks if tracks else get_all_tracks()
    exercises_not_logged_in = get_exercises_not_logged_in(session, tracks)

    is_user_logged_in = False
    if email and password:
        is_user_logged_in = log_in(session, email, password)
        exercises_logged_in = get_exercises_logged_in(session, tracks, exercises_not_logged_in)

    exercises_by_track = exercises_logged_in if is_user_logged_in else exercises_not_logged_in
    run_exercism_download(exercises_by_track, group, difficulty, status)

    print('done')


def list_all_tracks():
    for track in get_all_tracks():
        print(track)


def list_my_tracks(email, password):
    for track in get_my_tracks(email, password):
        print(track)
