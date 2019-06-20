import subprocess 
import requests
from pprint import pprint
from bs4 import BeautifulSoup


class DetailDownloader:
    __login_url = 'https://exercism.io/users/sign_in'
    __tracks_url = 'https://exercism.io/tracks'
    __all_tracks = []

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
        request = session.get(self.__login_url)
        soup = BeautifulSoup(request.content, 'html.parser')
        authenticity_token = soup.find(
            'input', 
            attrs={'name': 'authenticity_token'}
            )['value']
        self.credentials['authenticity_token'] = authenticity_token
        request = session.post(self.__login_url, data=self.credentials)
        return BeautifulSoup(request.content, 'html.parser')

    def __populate_tracks(self):
        request = requests.get(self.__tracks_url)
        soup = BeautifulSoup(request.content, 'html.parser')
        all_tracks = soup.findall('div', )
        self.__all_tracks = 

if __name__ == '__main__':
    track = 'python'
    email = 'andrzejgustaw@gmail.com'
    password = 'exxpressis'
    downloader = DetailDownloader(track, email=email, password=password)

    downloader.get_exercises()
