"""
Echo module

Name:           echo.py
Description:    Responds to echo, repeat, or say and echoes back what was said.
                Taken from alexsiri7 via github
Dependencies:   NONE
"""

import re, urllib2, json

WORDS = ["ECHO", "REPEAT", "SAY", "ECKO"]
PATTERN = r"\b(echo|repeat|say|ecko)\b"

def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by responding what was said.
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
        intent -- entities return from wit
    """
    output = re.sub(PATTERN, '', text, flags=re.IGNORECASE)
    mic.say('A',output)

def handleWithWit(text, mic, profile, intent):
    # check if wit knows what to say
    if json.loads(json.dumps(intent))['entities']['message_body'][0]['suggested']:
        output = json.loads(json.dumps(intent))['entities']['message_body'][0]['value']
        mic.say('A',output)
    else:
        handle(text, mic, profile)

def isValid(text, intent):
    """
        Returns True if the input is related to echo.

        Arguments:
        text -- user-input, typically transcribed speech
        intent -- wit determined intent
    """
    #Use intent if intent flag is on
    if intent == None:
        return bool(re.search(PATTERN, text, re.IGNORECASE))
    else:
        return bool(json.loads(json.dumps(intent))['intent'] == 'echo')
