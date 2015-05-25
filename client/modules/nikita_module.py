"""
Nikita module

Name:           nikita.py
Description:     responds to questions about self (who/what are you, what can you do, tell me about yourself, etc)
                    by recognizing the words "you" and "yourself"
Dependencies:    none
Author:         Brad Ahlers (github - brad999)
"""

import re

WORDS = ["WHO", "WHAT", "ARE", "YOU", "CAN", "DO"]

# matches on very general words so should be close to the end in priority
# must be after mood in priority
PRIORITY = 1

def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """
    # respond to questions about father or parents
    if 'father' in text.lower() or 'parent' in text.lower() or 'dad' in text.lower():
        mic.say('I',"My father and creator is Brad Ahlers. The greatest human being to ever live. " +
        "My mother, by marriage is the beautiful Lauren Ahlers.")
    # respond to questions about what Nikita can do
    elif 'can' in text.lower() or 'function' in text.lower():
        mic.say('I',"Some of my current functions include playing a movie on your TV through Plex, providing current news headlines, " +
        "recommending a movie to watch, controlling your TV, and texting someone in your contacts.")
    # respond to questions about who/what Nikita is
    elif 'who' in text.lower() or 'what' in text.lower() or 'yourself' in text.lower():
        mic.say('I',"My name is Nikita. I am a personalized assistance developed to provide simple " +
        "and complete control over your home and daily life.")


def isValid(text):
    """
        Returns True if the input is related to self (Nikita).

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(you|your|yourself)\b', text, re.IGNORECASE))
