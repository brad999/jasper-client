# -*- coding: utf-8-*-
import smtplib
from email.MIMEText import MIMEText
import urllib2
import re
from pytz import timezone


def sendEmail(SUBJECT, BODY, TO, FROM, SENDER, PASSWORD, SMTP_SERVER):
    """Sends an HTML email."""
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            BODY.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break
    msg = MIMEText(BODY.encode(body_charset), 'html', body_charset)
    msg['From'] = SENDER
    msg['To'] = TO
    msg['Subject'] = SUBJECT

    SMTP_PORT = 587
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.starttls()
    session.login(FROM, PASSWORD)
    session.sendmail(SENDER, TO, msg.as_string())
    session.quit()

def sendTextMsg(profile,recipientNumber,message):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(str(profile['gmail_address']), str(profile['gmail_password']))
    session.sendmail(str(profile['gmail_address']), recipientNumber, message)
    session.quit()

def YesOrNo(text):
    return bool('ye' in text.lower() or 'sure' in text.lower() or 'please' in text.lower() or 'correct' in text.lower())

def emailUser(profile, SUBJECT="", BODY=""):
    """
    sends an email.

    Arguments:
        profile -- contains information related to the user (e.g., email
                   address)
        SUBJECT -- subject line of the email
        BODY -- body text of the email
    """
    def generateSMSEmail(profile):
        """
        Generates an email from a user's phone number based on their carrier.
        """
        if profile['carrier'] is None or not profile['phone_number']:
            return None

        return str(profile['phone_number']) + "@" + profile['carrier']

    if profile['prefers_email'] and profile['gmail_address']:
        # add footer
        if BODY:
            BODY = profile['first_name'] + \
                ",<br><br>Here are your top headlines:" + BODY
            BODY += "<br>Sent from your Jasper"

        recipient = profile['gmail_address']
        if profile['first_name'] and profile['last_name']:
            recipient = profile['first_name'] + " " + \
                profile['last_name'] + " <%s>" % recipient
    else:
        recipient = generateSMSEmail(profile)

    if not recipient:
        return False

    try:
        if 'mailgun' in profile:
            user = profile['mailgun']['username']
            password = profile['mailgun']['password']
            server = 'smtp.mailgun.org'
        else:
            user = profile['gmail_address']
            password = profile['gmail_password']
            server = 'smtp.gmail.com'
        sendEmail(SUBJECT, BODY, recipient, user,
                  "Jasper <jasper>", password, server)

        return True
    except:
        return False

def convertPunctuation(text):
    #convert punctuation words to symbols
    text = re.sub(' period','.',text,re.IGNORECASE)
    text = re.sub(' question-mark','?',text,re.IGNORECASE)
    text = re.sub(' question mark','?',text,re.IGNORECASE)
    text = re.sub(' exclamation-point','!',text,re.IGNORECASE)
    text = re.sub(' exclamation point','!',text,re.IGNORECASE)
    # !! messaging doesn't like emoticons. will try to fix later
    #text = re.sub('smiley face',':)',text,re.IGNORECASE)
    #text = re.sub('happy face',':)',text,re.IGNORECASE)
    #text = re.sub('sad face',':(',text,re.IGNORECASE)
    #capitolize first word in sentence
    text = re.split('([.!?] *)', text)
    text = ''.join([i.capitalize() for i in text])
    return text

def convertNumberWords(text):
    #convert number words to numeric form
    text = re.sub('zero','0',text,re.IGNORECASE)
    text = re.sub('one','1',text,re.IGNORECASE)
    text = re.sub('two','2',text,re.IGNORECASE)
    text = re.sub('three','3',text,re.IGNORECASE)
    text = re.sub('four','4',text,re.IGNORECASE)
    text = re.sub('five','5',text,re.IGNORECASE)
    text = re.sub('six','6',text,re.IGNORECASE)
    text = re.sub('seven','7',text,re.IGNORECASE)
    text = re.sub('eight','8',text,re.IGNORECASE)
    text = re.sub('nine','9',text,re.IGNORECASE)
    text = re.sub('ten','10',text,re.IGNORECASE)
    return text

def convertOperators(text):
    #convert operators to symbol form
    text = re.sub('plus','+',text,re.IGNORECASE)
    text = re.sub('added to','+',text,re.IGNORECASE)
    text = re.sub('minus','-',text,re.IGNORECASE)
    text = re.sub('divided by','/',text,re.IGNORECASE)
    text = re.sub('multiplied by','*',text,re.IGNORECASE)
    text = re.sub('times','*',text,re.IGNORECASE)
    return text

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def getTimezone(profile):
    """
    Returns the pytz timezone for a given profile.

    Arguments:
        profile -- contains information related to the user (e.g., email
                   address)
    """
    try:
        return timezone(profile['timezone'])
    except:
        return None


def generateTinyURL(URL):
    """
    Generates a compressed URL.

    Arguments:
        URL -- the original URL to-be compressed
    """
    target = "http://tinyurl.com/api-create.php?url=" + URL
    response = urllib2.urlopen(target)
    return response.read()


def isNegative(phrase):
    """
    Returns True if the input phrase has a negative sentiment.

    Arguments:
        phrase -- the input phrase to-be evaluated
    """
    return bool(re.search(r'\b(no(t)?|don\'t|stop|end)\b', phrase,
                          re.IGNORECASE))


def isPositive(phrase):
    """
        Returns True if the input phrase has a positive sentiment.

        Arguments:
        phrase -- the input phrase to-be evaluated
    """
    return bool(re.search(r'\b(sure|yes|yeah|go)\b', phrase, re.IGNORECASE))
