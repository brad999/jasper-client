# -*- coding: utf-8-*-
import re
import json
import urllib2

WORDS = ["WEATHER", "TODAY", "TOMORROW"]


def replaceAcronyms(text):
    """
    Replaces some commonly-used acronyms for an improved verbal weather report.
    """

    def parseDirections(text):
        words = {
            'N': 'north',
            'S': 'south',
            'E': 'east',
            'W': 'west',
        }
        output = [words[w] for w in list(text)]
        return ' '.join(output)
    acronyms = re.findall(r'\b([NESW]+)\b', text)

    for w in acronyms:
        text = text.replace(w, parseDirections(w))

    text = re.sub(r'(\b\d+)F(\b)', '\g<1> Fahrenheit\g<2>', text)
    text = re.sub(r'(\b)mph(\b)', '\g<1>miles per hour\g<2>', text)
    text = re.sub(r'(\b)in\.', '\g<1>inches', text)

    return text


def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, with a summary of
    the relevant weather for the requested date (typically, weather
    information will not be available for days beyond tomorrow).

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user
    """
    f = urllib2.urlopen('http://api.wunderground.com/api/' +
                        str(profile['keys']["weatherUnderground"]) +
                        '/forecast/q/' + profile['location'] + '.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)

    currentWeather = parsed_json['forecast']['txt_forecast']['forecastday'][0]['fcttext']

    if currentWeather:
        currentWeather = replaceAcronyms(currentWeather)
        mic.say('I', currentWeather)
    else:
        mic.say('A', "I'm sorry, I can't seem to access that information. " +
                "Please make sure that you've set your location on the " +
                "dashboard.")


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(weathers?|temperature|forecast)\b',
                          text, re.IGNORECASE))
