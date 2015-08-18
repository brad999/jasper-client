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
    travelTime = directions_result[0]['legs'][0]['duration']['text']
    travelTime = travelTime.replace('mins', 'minutes')
    return travelTime


def checkState(location):
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California",
              "Colorado", "Connecticut", "Delaware", "Florida",
              "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
              "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
              "Maryland", "Massachusetts", "Michigan", "Minnesota",
              "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
              "New Hampshire", "New Jersey", "New Mexico", "New York",
              "North Carolina", "North Dakota", "Ohio", "Oklahoma",
              "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
              "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
              "Virginia", "Washington", "West Virginia", "Wisconsin",
              "Wyoming"]
    if any(x.lower() in location.lower() for x in states):
        return True
    else:
        return False

def getCoordinates(profile, db, location):
    gmaps = googlemaps.Client(key=profile['keys']["GoogleMaps"])
    # check for state, if no state assume Michigan
    if not checkState(location):
        location = location + " michigan"
    print location
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    coordinates = str(lat) + ', ' + str(lng)
    return coordinates


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

    if 'traffic' in text.lower() or 'accident' in text.lower() or\
       'crash' in text.lower():
       incidences = ' '.join(getTraffic(profile, mic.db))
       if incidences:
           mic.say('I', incidences)
       else:
           mic.say('A', "Roads are clear.")
    elif 'how long does it take to get to work' in text.lower() \
        or 'travel time' in text.lower():
        travelTime = getTravelTime(profile, mic.db,
                                   profile['locations']['home'],
                                   profile['locations']['work'])

        if travelTime:
            mic.say('I', "Travel time to work is " + travelTime)
        else:
            mic.say('A', "I am currently unable to retrieve this information")
    else:
        intent = app_utils.determineIntent(profile, text)
        # Use intent if found
        if intent:
            # check intent to get destination
            if json.loads(json.dumps(intent))['intent'] == 'travel_time':
                witSuggestion = (json.loads(json.dumps(intent))['entities']
                                 ['location'][0]['suggested'])
                if witSuggestion:
                    location = (json.loads(json.dumps(intent))['entities']
                             ['location'][0]['value'])
                    coordinates = getCoordinates(profile, mic.db, location)
                    travelTime = getTravelTime(profile, mic.db,
                                               profile['locations']['home'],
                                               coordinates)
                    if travelTime:
                        mic.say('I', "Travel time to " + location + " is " + travelTime + ".")
                    else:
                        mic.say('A', "I am currently unable to retrieve this information")


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(traffic|crashes|accidents|commute|' +
                          r'how long does it take to get to work|' +
                          r'how long does it)\b',
                          text, re.IGNORECASE))
