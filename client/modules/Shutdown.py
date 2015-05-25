"""
Shutdown module

Name:           Shutdown.py
Description: 	Responds to "shutdown", shuts down system
Dependencies:	Must run Nikita as root
Author:         Brad Ahlers (github - brad999)
"""

import os, re

WORDS = ["SHUTDOWN", "YES", "NO", "SHUT", "DOWN"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text.

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
        Returns True if the input is related to shutdown.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(shutdown|shut down)\b', text, re.IGNORECASE))
