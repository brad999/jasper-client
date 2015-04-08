"""
Mood module
Name: TV.py 
Description: 	responds to common TV commands (turn up/down volume, change input, turn on/off, etc)
Dependencies:	python-cec library
		CEC compatible TV and controller (Raspberry Pi)
"""
import cec, re

WORDS = ["VOLUME", "UP", "DOWN", "TV", "TELEVISION", "POWER", "ON", "OFF"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """
    cec.init()
    tv = cec.Device(0)

    # !! add volume and mute functions	
    if 'on' in text.lower():
        tv.power_on()
        mic.say("TV powered on.")
    elif 'off' in text.lower() or 'off' in text.lower():
        tv.standby()
        mic.say("TV powered off.")
    else:
        mic.say("I'm sorry that command is not currently supported")
	

def isValid(text):
    """
        Returns True if the input is related to TV.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(tv|television)\b', text, re.IGNORECASE))
