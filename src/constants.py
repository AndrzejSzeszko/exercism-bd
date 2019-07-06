LOGIN_URL = 'https://exercism.io/users/sign_in'

CRAWLING_URL_PATTERN_NOT_LOGGED_IN = 'https://exercism.io/tracks'
CRAWLING_URL_PATTERN_LOGGED_IN = 'https://exercism.io/my/tracks'

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
