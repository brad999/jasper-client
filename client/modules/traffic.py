# -*- coding: utf-8-*-
"""
Traffic module

Name:           traffic.py

Description:    responds to questions about traffic and commute time

Dependencies:   Bing Maps API (bingmapsportal.com)
                Google Maps (sudo pip install -U googlemaps)

Author:         Brad Ahlers (github - brad999)
"""

import re
import json
import urllib2
import googlemaps
import datetime
from client import app_utils

WORDS = ["TRAFFIC", "CRASHES", "ACCIDENTS", "COMMUTE", "HOW", "LONG",
         "DOES", "IT", "TAKE", "TO", "GET", "WORK"]


def getTraffic(profile, db):
    f = urllib2.urlopen('http://dev.virtualearth.net/REST/v1/Traffic' +
                        '/Incidents/' + str(profile['TrafficArea']) +
                        '?key=' + profile['keys']["BingMaps"])
    app_utils.updateAPITracker(db, 'Bing Maps')
    json_string = f.read()
    parsed_json = json.loads(json_string)

    incidences = []

    for i in parsed_json['resourceSets'][0]['resources']:
        incidences.append(i['description'])

    return incidences


def getTravelTime(profile, db, origin, destination):
    gmaps = googlemaps.Client(key=profile['keys']["GoogleMaps"])
    now = datetime.datetime.now()
    directions_result = gmaps.directions(origin, destination, departure_time=now)

    return directions_result[0]['legs'][0]['duration']['text']

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

    if 'how long does it take to get to work' in text.lower() \
       or 'travel time' in text.lower():
        travelTime = getTravelTime(profile, mic.db,
                                   profile['locations']['home'],
                                   profile['locations']['work'])
        travelTime = travelTime.replace('mins', 'minutes')

        if travelTime:
            mic.say('I', "Travel time to work is " + travelTime)
        else:
            mic.say('A', "I am currently unable to retrieve this information")
    else:
        incidences = ' '.join(getTraffic(profile, mic.db))
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
    return bool(re.search(r'\b(traffic|crashes|accidents|commute|' +
                          r'how long does it take to get to work)\b',
                          text, re.IGNORECASE))
