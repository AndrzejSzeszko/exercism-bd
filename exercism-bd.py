import subprocess
import requests
from pprint import pprint
from bs4 import BeautifulSoup


class Downloader:
    LOGIN_URL = 'https://exercism.io/users/sign_in'
    CRAWLING_URL_PATTERN_NOT_LOGGED_IN = 'https://exercism.io/tracks/'
    CRAWLING_URL_PATTERN_LOGGED_IN = 'https://exercism.io/my/tracks/'
    ALLOWED_STATUSES = ('in-progress', 'unlocked', 'completed', 'locked')
    ALLOWED_DIFFICULTIES = ('easy', 'medium', 'hard')
    ALLOWED_GROUPS = ('core', 'side')

    @staticmethod
    def download_exercises(*tracks, group=None, difficulty=None, status=None, email=None, password=None):
        conditions = []
        if group:
            conditions.append('group')
        if difficulty:
            conditions.append('difficulty')
        if status:
            conditions.append('status')
            
        session = requests.Session()
        tracks = tracks if tracks else Downloader.__get_all_tracks()
        exercises_not_logged_in = Downloader.__get_exercises_not_logged_in(session, tracks)

        is_user_logged_in = False
        if email and password:
            is_user_logged_in = Downloader.__log_in(session, email, password)
            exercises_logged_in = Downloader.__get_exercises_logged_in(session, tracks, exercises_not_logged_in)

        exercises_by_track = exercises_logged_in if is_user_logged_in else exercises_not_logged_in
        for track, exercises in exercises_by_track.items():
            for exercise, properties in exercises.items():
                group_condition_met = properties['group'] == group if 'group' in conditions else True
                difficulty_condition_met = properties['difficulty'] == difficulty if 'difficulty' in conditions else True
                status_condition_met = properties['status'] == status if 'status' in conditions else True

                if group_condition_met and difficulty_condition_met and status_condition_met:
                    command = f'exercism d -t {track} -e {exercise}'
                    output = subprocess.run(command.split(), capture_output=True)
                    print(output.stderr, '\n', output.stdout, '\n')

    @staticmethod
    def __log_in(session, email, password):
        request = session.get(Downloader.LOGIN_URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        authenticity_token = soup.find(attrs={'name': 'authenticity_token'})['value']
        credentials = {
                'user[email]': email,
                'user[password]': password,
                'authenticity_token': authenticity_token
            }
        request = session.post(Downloader.LOGIN_URL, data=credentials)
        soup = BeautifulSoup(request.content, 'html.parser')
        return bool(soup.find(class_='logged-in'))

    @staticmethod
    def __get_exercises_not_logged_in(session, tracks):
        exercises_by_track = {}
        for track in tracks:
            crawling_url = Downloader.CRAWLING_URL_PATTERN_NOT_LOGGED_IN + track + '/exercises'
            request = session.get(crawling_url)
            crawling_soup = BeautifulSoup(request.content, 'html.parser')

            exercises = Downloader.__get_exercises(crawling_soup)
            exercises_by_track[track] = exercises

        return exercises_by_track

    @staticmethod
    def __get_exercises_logged_in(session, tracks, exercises_not_logged_in):
        exercises_by_track = {}
        for track in tracks:
            crawling_url = Downloader.CRAWLING_URL_PATTERN_LOGGED_IN + track
            request = session.get(crawling_url)
            crawling_soup = BeautifulSoup(request.content, 'html.parser')

            core_exercises = Downloader.__get_core_exercises(crawling_soup, exercises_not_logged_in[track])
            side_exercises = Downloader.__get_side_exercises(crawling_soup)
            exercises_by_track[track] = dict(**core_exercises, **side_exercises)
                
        return exercises_by_track

    @staticmethod
    def __get_exercises(crawling_soup):
        exercises_tags = crawling_soup.find_all(class_='exercise')

        exercises = {}
        for exercise_tag in exercises_tags:
            raw_name = exercise_tag.find('h3').text
            name = raw_name.lower().replace(' ', '-')
            difficulty = exercise_tag.find(class_='difficulty').text
            exercises[name] = {
                'difficulty': difficulty,
                'group': None,
                'status': None
            }
        return exercises
    
    @staticmethod
    def __get_core_exercises(crawling_soup, exercises_not_logged_in):
        core_exercises_tags = crawling_soup.find_all(class_='exercise')

        core_exercises = {}
        for exercise_tag in core_exercises_tags:
            name = exercise_tag['id'].replace('exercise-', '')
            raw_status = exercise_tag.find(class_='status').text
            status = raw_status.lower().replace(' ', '-')
            core_exercises[name] = {
                'difficulty': exercises_not_logged_in[name]['difficulty'],
                'group': 'core',
                'status': status
            }
        return core_exercises
    
    @staticmethod
    def __get_side_exercises(crawling_soup):
        side_exercises_tags = crawling_soup.find_all(class_='widget-side-exercise')

        side_exercises = {}
        for exercise_tag in side_exercises_tags:
            name = exercise_tag.find('div')['id'].replace('exercise-', '')
            raw_status = exercise_tag['class'][-1]
            status = 'completed' if raw_status in ['in-progress', 'mentoring-requested'] else raw_status
            difficulty = exercise_tag.find(class_='difficulty').text
            side_exercises[name] = {
                'difficulty': difficulty,
                'group': 'side',
                'status': status
            }
        return side_exercises

    @staticmethod
    def __get_all_tracks():
        request = requests.get(Downloader.CRAWLING_URL_PATTERN_NOT_LOGGED_IN)
        soup = BeautifulSoup(request.content, 'html.parser')
        all_tracks_h2s = soup.find_all('h2')
        return tuple(track.text for track in all_tracks_h2s)


if __name__ == '__main__':
    tracks = ['python']
    email = 'andrzejgustaw@gmail.com'
    password = 'exxpressis'

    x = Downloader.download_exercises(*tracks, group='core', difficulty='easy', email=email, password=password)
    print('done')
