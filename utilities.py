import colorama
import os

def message(title, msg, color):
    print(f'{color}{colorama.Style.BRIGHT}{title}: {colorama.Style.RESET_ALL} {colorama.Style.RESET_ALL}{msg}')

def info(msg):
    message('Info', msg, colorama.Fore.MAGENTA)

def warning(msg):
    message('Warning', msg, colorama.Fore.YELLOW)

def error(msg):
    message('Error', msg, colorama.Fore.RED)
    exit(1)

def loadenv(path):
    if os.path.exists(path):
        for line in open(path):
            var = line.strip().split('=')
            if len(var) == 2:
                os.environ[var[0]] = var[1]

def getenv(variable):
    try:
        return os.environ[variable]
    except KeyError:
        message('Missing variable', variable, colorama.Fore.MAGENTA)
        exit(1)
