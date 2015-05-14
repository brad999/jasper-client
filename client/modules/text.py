"""
Texting module
Name:            text.py
Description:     Sends text message to designated recipient. Responds to "text" or "tell"
Dependencies:    Gmail, Contacts list
Author:          Brad Ahlers (github - brad999)
"""
import re, smtplib, yaml
from client import nikitapath, app_utils

WORDS = ["TEXT", "TELL"]

def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """

    #determine recipient name and message
    # !! add logic to check if name was provided but no message
    if re.search("(text|tell) (\w+) (.*)",text, re.IGNORECASE):
        x = re.search("(text|tell) (\w+) (.*)",text, re.IGNORECASE)
        name = x.group(2)
        message = x.group(3)
    else:
        mic.say("Who would you like to text?")
        name = mic.activeListen()
        mic.say("What would you like to tell " + name + "?")
        message = mic.activeListen()

    #check for recipient number in contacts.yml
    f = open(nikitapath.data('text','CONTACTS.yml'))
    contacts = yaml.safe_load(f)
    recipientNumber = str(contacts[name.lower()])
    f.close()
    if recipientNumber:
        #check for a message
        if message:
            #format message properly
            message = app_utils.convertPunctuation(message.lower())
            #confirm message and recipient before sending
            mic.say("Are you sure you would like to tell " + name + ", " + message + "?")
            if app_utils.YesOrNo(mic.activeListen()):
                #send text message
                app_utils.sendTextMsg(profile,recipientNumber,message)
                mic.say("Message has been sent to " + name + ".")
            else:
                mic.say("Message was not sent.")
        else:
            mic.say("I'm sorry. I didn't understand that message")
    else:
        mic.say("I'm sorry. I could not find " + name + " in my address book.")

def isValid(text):
    """
        Returns True if the input is related to texting.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(text|tell(?!me))\b', text, re.IGNORECASE))
