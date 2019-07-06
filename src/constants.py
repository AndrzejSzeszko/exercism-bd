LOGIN_URL = 'https://exercism.io/users/sign_in'

CRAWLING_URL_PATTERN_NOT_LOGGED_IN = 'https://exercism.io/tracks/'
CRAWLING_URL_PATTERN_LOGGED_IN = 'https://exercism.io/my/tracks/'

ALLOWED_STATUSES = ('in-progress', 'unlocked', 'completed', 'locked')
ALLOWED_DIFFICULTIES = ('easy', 'medium', 'hard')
ALLOWED_GROUPS = ('core', 'side')
