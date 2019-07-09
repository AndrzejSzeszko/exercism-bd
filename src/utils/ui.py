def bold(string):
    start = '\033[1m'
    end = '\033[0m'
    return f'{start}{string}{end}'


def underscore(string):
    start = '\033[4m'
    end = '\033[0m'
    return f'{start}{string}{end}'
