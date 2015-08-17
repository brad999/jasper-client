# -*- coding: utf-8-*-
"""
Know It All module

Name:           knowItAll.py
Description:    responds to questions pharsed several ways
                uses WolframAlpha to return answers
Dependencies:   WolframAlpha API (requires key)
                wolframalpha installed via pip
Author:         ajay-gandhi (github)
                Brad Ahlers (github - brad999)
"""
import re
import wolframalpha
from client import app_utils

WORDS = ["WHO", "WHAT", "HOW", "TELL", "ME", "ABOUT", "WHEN", "DEFINE"]
PRIORITY = -1


def handle(text, mic, profile):
    app_id = profile['keys']['WolframAlpha']
    client = wolframalpha.Client(app_id)

    query = client.query(text)
    app_utils.updateAPITracker(mic.db, 'WolframAlpha')

    if len(query.pods) > 0:
        texts = ""
        pod = query.pods[1]
        if pod.text:
            texts = pod.text
            # only get the first line of the response
            # primarily used to remove multiple definitions
            texts = texts.split("\n", 1)[0]
        else:
            texts = "I can not find anything"

        mic.say('I', texts.replace("|", ""))
    else:
        mic.say('A', "Sorry, Could you be more specific?.")


def isValid(text):
    return bool(re.search(r'\bwho|what|when|how|tell me|define\b',
                text, re.IGNORECASE))
