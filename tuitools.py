from enum import Enum,auto
import subprocess

def clear():
    subprocess.run('clear')

class Colors(Enum):
    BLACK = "\033[0;30m"
    DARK_GREY = "\033[1;30m"
    RED = "\033[0;31m"
    LIGHT_RED = "\033[1;31m"
    GREEN = "\033[0;32m"
    LIGHT_GREEN = "\033[1;32m"
    ORANGE = "\033[0;33m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    LIGHT_BLUE = "\033[1;34m"
    PURPLE = "\033[0;35m"
    LIGHT_PURPLE = "\033[1;35m"
    CYAN = "\033[0;36m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_GRAY = "\033[0;37m"
    WHITE = "\033[1;37m"
    NC = "\033[0m"

_color_lookup = {
    Colors.BLACK: "\033[0;30m",
    Colors.DARK_GREY: "\033[1;30m",
    Colors.RED: "\033[\033[0;31m",
    Colors.LIGHT_RED: "\033[1;31m",
    Colors.GREEN: "\033[0;32m",
    Colors.LIGHT_GREEN: "\033[1;32m",
    Colors.ORANGE: "\033[0;33m",
    Colors.YELLOW: "\033[1;33m",
    Colors.BLUE: "\033[0;34m",
    Colors.LIGHT_BLUE: "\033[1;34m",
    Colors.PURPLE: "\033[0;35m",
    Colors.LIGHT_PURPLE: "\033[1;35m",
    Colors.CYAN: "\033[0;36m",
    Colors.LIGHT_CYAN: "\033[1;36m",
    Colors.LIGHT_GRAY: "\033[0;37m",
    Colors.WHITE: "\033[1;37m",
    Colors.NC: "\033[0m",
}

def colorize_string(text:str,col:Colors):
    return f'{col.value}{text}\033[0m'