"""
Mood module
Name: text.py
Description:     Sends text message to designated recipient. Responds to "text"
Dependencies:    Gmail, Contacts list
Author:          Brad Ahlers (github - brad999)
"""
import re, smtplib, yaml
from client import jasperpath

WORDS = ["TEXT"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """

    #determine recipient name
    # !! add "tell" command in addition to "text"
    # !! add logic to determine name and message if not in initial command
    x = re.search("text (\w+) (.*)",text, re.IGNORECASE)
    name = x.group(1)
    message = x.group(2)

    #check for recipient number in contacts.yml
    f = open(jasperpath.data('text','CONTACTS.yml'))
    contacts = yaml.safe_load(f)
    recipientNumber = str(contacts[name.lower()])
    f.close()
    if recipientNumber:
        #check for a message
        if message:
            # !! move send to app_utils.py
            # !! add logic to confirm message and recipient before sending
            session = smtplib.SMTP('smtp.gmail.com', 587)
            session.starttls()
            session.login(str(profile['gmail_address']), str(profile['gmail_password']))
            session.sendmail(str(profile['gmail_address']), recipientNumber, message.lower())
            mic.say("Message has been sent to " + name + ".")
        else:
            mic.say("I'm sorry. I didn't get that message")
    else:
        mic.say("I'm sorry. I could not find " + name + " in my address book.")

def isValid(text):
    """
        Returns True if the input is related to TV.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(text)\b', text, re.IGNORECASE))

