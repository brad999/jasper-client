"""
Echo module

Name:           echo.py
Description:    Responds to echo, repeat, or say and echoes back what was said
Dependencies:   NONE
Author:         alexsiri7 via github
"""

import re

WORDS = ["ECHO", "REPEAT", "SAY"]
PATTERN = r"\b(echo|repeat|say)\b"


def handle(text, mic, profile):
    """
        Responds to user-input
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user
    """
    output = re.sub(PATTERN, '', text, flags=re.IGNORECASE)
    mic.say('A', output)


def isValid(text):
    return bool(re.search(PATTERN, text, re.IGNORECASE))
