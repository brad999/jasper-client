"""
Mood module
Name: Shutdown.py 
Description: 	Responds to "shutdown", shuts down system. Must run Jasper as root to work.
Dependencies:	None
"""
import os, re

WORDS = ["SHUTDOWN", "YES", "NO"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """

    def handleResponse(text):
        if 'no' in text.lower():
            mic.say("Alright, I will stay alive.")
        elif 'yes' in text.lower():
            mic.say("It was nice knowing you. Good bye.")
            os.system("shutdown -h now")
        else:
            mic.say("I did not get that so I will stay alive.")
 
    mic.say("Are you sure you want me to die?")
    handleResponse(mic.activeListen())

def isValid(text):
    """
        Returns True if the input is related to TV.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(shutdown)\b', text, re.IGNORECASE))
