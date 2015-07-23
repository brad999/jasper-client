# -*- coding: utf-8-*-
"""
Movie module

Name:           knowItAll.py
Description:    responds to questions pharsed several ways
                uses WolframAlpha to return answers
Dependencies:   WolframAlpha API (requires key)
                wolframalpha installed via pip
Author:         ajay-gandhi (github)
                Brad Ahlers (github - brad999)
"""
import random, re, wolframalpha, time, sys
from sys import maxint

from client import jasperpath
WORDS = ["WHO", "WHAT", "HOW", "TELL", "ME", "ABOUT", "WHEN"]

PRIORITY = -1

def handle(text, mic, profile):
    app_id = profile['keys']['WolframAlpha']
    client = wolframalpha.Client(app_id)

    query = client.query(text)
    if len(query.pods) > 0:
        texts = ""
        pod = query.pods[1]
        if pod.text:
            texts = pod.text
        else:
            texts = "I can not find anything"

        mic.say('I',texts.replace("|",""))
    else:
        mic.say('A',"Sorry, Could you be more specific?.")


def isValid(text):
    if re.search(r'\bwho\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bwhat\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bhow\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\btell me about\b', text, re.IGNORECASE):
        return True
    elif re.search(r'\bwhen\b', text, re.IGNORECASE):
        return True
    else:
        return False
