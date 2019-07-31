LOGIN_URL = 'https://exercism.io/users/sign_in'

CRAWLING_URL_PATTERN_NOT_LOGGED_IN = 'https://exercism.io/tracks'
CRAWLING_URL_PATTERN_LOGGED_IN = 'https://exercism.io/my/tracks'

AUTHENTICATION_FAILED_MESSAGE = '\nAuthentication failed. Provided credentials do not match any exercism account.'

ALLOWED_STATUSES = {
    'completed': 'completed',
    'approved': 'in-progress',
    'mentoring-requested': 'in-progress',
    'in-progress': 'in-progress',
    'unlocked': 'unlocked',
    'locked': 'locked'
}

ALLOWED_DIFFICULTIES = {
    'easy': 'easy',
    'medium': 'medium',
    'hard': 'hard',
}

ALLOWED_GROUPS = {
    'core': 'core',
    'side': 'side'
}

# TODO: when only name of program typed it downloads all exercises - there should be warnig about that
# TODO: logging insted of printing ?
# TODO: tests
# TODO: verbose/qiuet (decoretors metaprogramming)
# TODO: statusbar
# TODO: setuptools
# TODO: snap
# TODO: docs
# TODO: docs
# TODO: docstrings
# TODO: information for user about new version
# TODO: windows executable and installer
# TODO: not trying to download not joined tracks and locked exercises
