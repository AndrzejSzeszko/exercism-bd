import re
import subprocess
import requests

from bs4 import BeautifulSoup

from constants import (
    LOGIN_URL,
    CRAWLING_URL_PATTERN_NOT_LOGGED_IN,
    CRAWLING_URL_PATTERN_LOGGED_IN,
    ALLOWED_STATUSES
)


def __make_raw_name_cli_usable(raw_name):
    return re.sub('^exercise-', '', raw_name)


def __extract_last_chunk_of_href(href):
    return re.search('[^/]+$', href).group()


def __get_exercises(crawling_soup):
    exercises_tags = crawling_soup.find_all(class_='exercise')

    exercises = {}
    for exercise_tag in exercises_tags:
        href = exercise_tag.attrs.get('href')
        name = __extract_last_chunk_of_href(href)
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
        status = ALLOWED_STATUSES[raw_status]
        difficulty = exercise_tag.find(class_='difficulty').text
        side_exercises[name] = {
            'difficulty': difficulty,
            'group': 'side',
            'status': status
        }
    return side_exercises


def log_in(session, email, password):
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


def get_my_tracks(email, password):
    session = requests.Session()
    log_in(session, email, password)
    request = session.get(CRAWLING_URL_PATTERN_LOGGED_IN)
    crawling_soup = BeautifulSoup(request.content, 'html.parser')
    exercises_tags = crawling_soup.find_all(class_='joined')

    my_tracks = []
    for exercise_tag in exercises_tags:
        href = exercise_tag.attrs.get('href')
        track = __extract_last_chunk_of_href(href)
        my_tracks.append(track)

    return my_tracks


def get_all_tracks():
    request = requests.get(CRAWLING_URL_PATTERN_NOT_LOGGED_IN)
    soup = BeautifulSoup(request.content, 'html.parser')
    exercises_links = soup.find_all('a', class_='track')

    all_tracks = []
    for link in exercises_links:
        href = link.attrs.get('href')
        all_tracks.append(__extract_last_chunk_of_href(href))

    return all_tracks


def get_exercises_logged_in(session, tracks, exercises_not_logged_in):
    exercises_by_track = {}
    for track in tracks:
        crawling_url = CRAWLING_URL_PATTERN_LOGGED_IN + track
        request = session.get(crawling_url)
        crawling_soup = BeautifulSoup(request.content, 'html.parser')

        core_exercises = __get_core_exercises(crawling_soup, exercises_not_logged_in[track])
        side_exercises = __get_side_exercises(crawling_soup)
        exercises_by_track[track] = dict(**core_exercises, **side_exercises)

    return exercises_by_track


def get_exercises_not_logged_in(session, tracks):
    exercises_by_track = {}
    for track in tracks:
        crawling_url = CRAWLING_URL_PATTERN_NOT_LOGGED_IN + track + '/exercises'
        request = session.get(crawling_url)
        crawling_soup = BeautifulSoup(request.content, 'html.parser')

        exercises = __get_exercises(crawling_soup)
        exercises_by_track[track] = exercises

    return exercises_by_track


def run_exercism_download(exercises_by_track, group, difficulty, status):
    for track, exercises in exercises_by_track.items():
        for exercise_name, exercise_properties in exercises.items():
            group_condition_met = exercise_properties['group'] == group if group else True
            difficulty_condition_met = exercise_properties['difficulty'] == difficulty if difficulty else True
            status_condition_met = exercise_properties['status'] == status if status else True

            if group_condition_met and difficulty_condition_met and status_condition_met:
                command = f'exercism download --track={track} --exercise={exercise_name}'
                output = subprocess.run(command.split(), capture_output=True)
                stderr = output.stderr.decode('UTF-8').strip()
                stdout = output.stdout.decode('UTF-8').strip()
                message = f'Track: {track}, Exercise: {exercise_name}\n{stderr}\n{stdout}\n'
                print(message)
