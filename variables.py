from pathlib import Path
import re 


ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / 'files'
WINDOW_ICON_PATH  = FILES_DIR / 'icon.png'



BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 12
DEFAULT_TEXT_MARGIN = 15
MINIMUN_WIDHT = 500
PRIMARY_COLOR = '#CC5500'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#FFFFFF'


NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


def isEmpty(string: str):
    return len(string) == 0

def isValidNumber(string: str):
        valid = False
        try:
            float(string)
            valid = True  
        except ValueError:
            valid = False
        return valid


