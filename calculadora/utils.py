
import re

NUM_OR_DOT = re.compile(r'^[0-9.]$')

def isNumOrDot(string: str):
    return bool(NUM_OR_DOT.search(string))

def isValidNumbe(string: str):
    valid = False
    try:
        float(string)
        valid = True

    except ValueError:
        valid = False
    return valid

def isEmpty(string: str):
    return len(string) == 0