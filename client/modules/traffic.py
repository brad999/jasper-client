# -*- coding: utf-8-*-
import re
import json
import urllib2

WORDS = ["TRAFFIC", "CRASHES", "ACCIDENTS", "COMMUTE"]


def getTraffic(profile):
    f = urllib2.urlopen('http://dev.virtualearth.net/REST/v1/Traffic' +
                        '/Incidents/' + str(profile['TrafficArea']) +
                        '?key=' + profile['keys']["BingMaps"])
    json_string = f.read()
    parsed_json = json.loads(json_string)

    incidences = []

    for i in parsed_json['resourceSets'][0]['resources']:
        incidences.append(i['description'])

    return incidences


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

    incidences = ' '.join(getTraffic(profile))
    if incidences:
        mic.say('I', incidences)
    else:
        mic.say('A', "Roads are clear.")


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(traffic|crashes|accidents|commute)\b',
                          text, re.IGNORECASE))
