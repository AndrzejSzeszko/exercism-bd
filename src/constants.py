LOGIN_URL = 'https://exercism.io/users/sign_in'

CRAWLING_URL_PATTERN_NOT_LOGGED_IN = 'https://exercism.io/tracks'
CRAWLING_URL_PATTERN_LOGGED_IN = 'https://exercism.io/my/tracks'

AUTHENTICATION_FAILED_MESSAGE = 'Authentication failed. \n' \
                                'Check if you provided correct credentials (as a arguments or via configuration file). \n' \
                                'For more information type: exercism-bd --help. \n'

CANNOT_READ_CONFIG_FILE_MESSAGE = 'Config file is empty, malformed or does not exist.\n' \
                                  'Provide email and password alongside this command or store them in configuration file properly.\n' \
                                  'For more information type: exercism-bd --help. \n'

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
