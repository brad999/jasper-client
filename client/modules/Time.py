# -*- coding: utf-8-*-
import datetime
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["TIME", "WHAT", "IS", "IT", "THE"]


def handle(text, mic, profile):
    """
        Reports the current time based on the user's timezone.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    tz = getTimezone(profile)
    now = datetime.datetime.now(tz=tz)
    service = DateService()
    response = service.convertTime(now)
    mic.say('I', "It is %s right now." % response)


def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    if text.lower() == "what time is it" or text.lower() == "what is the time":
        return True
    else:
        return False
