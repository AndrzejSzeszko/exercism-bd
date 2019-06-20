import subprocess 
import requests
from pprint import pprint
from bs4 import BeautifulSoup


class DetailDownloader:
    __LOGIN_URL = 'https://exercism.io/users/sign_in'
    __TRACKS_URL = 'https://exercism.io/tracks'

    def __init__(self, track, group=None, difficulty=None, status=None, email=None, password=None):
        self.crawling_url = 'https://exercism.io/my/tracks/' + track.strip()
        self.credentials = {
                'user[email]': email,
                'user[password]': password
            }

    def get_exercises(self):
        with requests.Session() as session:
            soup = self.__get_after_log_in_soup(session)
            print(soup)

            # side_exercises = soup.find_all('a', {'class': ['pure-button', 'pure-u-md-hide']})
            # pprint(side_exercises)
            # exercises_names = []
            # for side_exercise in side_exercises:
            #     print(side_exercise)

    def __get_after_log_in_soup(self, session):
        request = session.get(self.__LOGIN_URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        authenticity_token = soup.find(
            'input', 
            attrs={'name': 'authenticity_token'}
            )['value']
        self.credentials['authenticity_token'] = authenticity_token
        request = session.post(self.__LOGIN_URL, data=self.credentials)
        return BeautifulSoup(request.content, 'html.parser')

    @property
    def __all_tracks(self):
        request = requests.get(self.__TRACKS_URL)
        soup = BeautifulSoup(request.content, 'html.parser')
        all_tracks_h2 = soup.find_all('h2')
        return tuple(track.text for track in all_tracks_h2)

    

if __name__ == '__main__':
    track = 'python'
    email = 'andrzejgustaw@gmail.com'
    password = 'exxpressis'
    downloader = DetailDownloader(track, email=email, password=password)

    downloader.get_exercises()
