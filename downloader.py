import subprocess
import requests

from bs4 import BeautifulSoup

from constants import (
    LOGIN_URL,
    CRAWLING_URL_PATTERN_NOT_LOGGED_IN,
    CRAWLING_URL_PATTERN_LOGGED_IN,
    STRINGS_REPLACEMENTS
)


def __make_raw_name_cli_usable(raw_name):
    name = raw_name.strip().lower()
    for string, replacement in STRINGS_REPLACEMENTS:
        name = name.replace(string, replacement)
    return name

def __get_all_tracks():
    request = requests.get(CRAWLING_URL_PATTERN_NOT_LOGGED_IN)
    soup = BeautifulSoup(request.content, 'html.parser')
    all_tracks_h2s = soup.find_all('h2')
    return tuple(track.text for track in all_tracks_h2s)

def __log_in(session, email, password):
    request = session.get(LOGIN_URL)
    soup = BeautifulSoup(request.content, 'html.parser')
    authenticity_token = soup.find(attrs={'name': 'authenticity_token'})['value']
    credentials = {
            'user[email]': email,
            'user[password]': password,
            'authenticity_token': authenticity_token
        }
    request = session.post(LOGIN_URL, data=credentials)
    soup = BeautifulSoup(request.content, 'html.parser')
    return bool(soup.find(class_='logged-in'))

def __get_exercises(crawling_soup):
    exercises_tags = crawling_soup.find_all(class_='exercise')

    exercises = {}
    for exercise_tag in exercises_tags:
        raw_name = exercise_tag.find('h3').text
        name = __make_raw_name_cli_usable(raw_name)
        difficulty = exercise_tag.find(class_='difficulty').text
        exercises[name] = {
            'difficulty': difficulty,
            'group': None,
            'status': None
        }
    return exercises

def __get_core_exercises(crawling_soup, exercises_not_logged_in):
    core_exercises_tags = crawling_soup.find_all(class_='exercise')

    core_exercises = {}
    for exercise_tag in core_exercises_tags:
        raw_name = exercise_tag['id']
        name = __make_raw_name_cli_usable(raw_name)
        raw_status = exercise_tag.find(class_='status').text
        status = raw_status.lower().replace(' ', '-')
        core_exercises[name] = {
            'difficulty': exercises_not_logged_in[name]['difficulty'],
            'group': 'core',
            'status': status
        }
    return core_exercises

def __get_side_exercises(crawling_soup):
    side_exercises_tags = crawling_soup.find_all(class_='widget-side-exercise')

    side_exercises = {}
    for exercise_tag in side_exercises_tags:
        raw_name = exercise_tag.find('div')['id']
        name = __make_raw_name_cli_usable(raw_name)
        raw_status = exercise_tag['class'][-1]
        status = 'completed' if raw_status in ['in-progress', 'mentoring-requested'] else raw_status
        difficulty = exercise_tag.find(class_='difficulty').text
        side_exercises[name] = {
            'difficulty': difficulty,
            'group': 'side',
            'status': status
        }
    return side_exercises

def __get_exercises_logged_in(session, tracks, exercises_not_logged_in):
    exercises_by_track = {}
    for track in tracks:
        crawling_url = CRAWLING_URL_PATTERN_LOGGED_IN + track
        request = session.get(crawling_url)
        crawling_soup = BeautifulSoup(request.content, 'html.parser')

        core_exercises = __get_core_exercises(crawling_soup, exercises_not_logged_in[track])
        side_exercises = __get_side_exercises(crawling_soup)
        exercises_by_track[track] = dict(**core_exercises, **side_exercises)

    return exercises_by_track

def __get_exercises_not_logged_in(session, tracks):
    exercises_by_track = {}
    for track in tracks:
        crawling_url = CRAWLING_URL_PATTERN_NOT_LOGGED_IN + track + '/exercises'
        request = session.get(crawling_url)
        crawling_soup = BeautifulSoup(request.content, 'html.parser')

        exercises = __get_exercises(crawling_soup)
        exercises_by_track[track] = exercises

    return exercises_by_track

def download_exercises(tracks=None, group=None, difficulty=None, status=None, email=None, password=None):
    conditions = []
    if group:
        conditions.append('group')
    if difficulty:
        conditions.append('difficulty')
    if status:
        conditions.append('status')

    session = requests.Session()
    tracks = tracks if tracks else __get_all_tracks()
    exercises_not_logged_in = __get_exercises_not_logged_in(session, tracks)

    is_user_logged_in = False
    if email and password:
        is_user_logged_in = __log_in(session, email, password)
        exercises_logged_in = __get_exercises_logged_in(session, tracks, exercises_not_logged_in)

    exercises_by_track = exercises_logged_in if is_user_logged_in else exercises_not_logged_in
    for track, exercises in exercises_by_track.items():
        for exercise, properties in exercises.items():
            group_condition_met = properties['group'] == group if 'group' in conditions else True
            difficulty_condition_met = properties['difficulty'] == difficulty if 'difficulty' in conditions else True
            status_condition_met = properties['status'] == status if 'status' in conditions else True

            if group_condition_met and difficulty_condition_met and status_condition_met:
                command = f'exercism download --track {track} --exercise {exercise}'
                output = subprocess.run(command.split(), capture_output=True)
                stderr = output.stderr.decode('UTF-8').strip()
                stdout = output.stdout.decode('UTF-8').strip()
                message = f'Track: {track}, Exercise: {exercise}\n{stderr}\n{stdout}\n'
                print(message)
