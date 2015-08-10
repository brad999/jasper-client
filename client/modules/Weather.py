# -*- coding: utf-8-*-
import re
import json
import urllib2
import datetime

WORDS = ["WEATHER", "TODAY", "TOMORROW"]


def getWeather(profile, day):
    f = urllib2.urlopen('http://api.wunderground.com/api/' +
                        str(profile['keys']["weatherUnderground"]) +
                        '/forecast/q/' + profile['location'] + '.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)

    for i in parsed_json['forecast']['txt_forecast']['forecastday']:
        if i['title'] == day:
            return i['fcttext']

    return ""

def getExtendedWeather(profile, day):
    f = urllib2.urlopen('http://api.wunderground.com/api/' +
                        str(profile['keys']["weatherUnderground"]) +
                        '/forecast10day/q/' + profile['location'] + '.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)

    for i in parsed_json['forecast']['txt_forecast']['forecastday']:
        if i['title'] == day:
            return i['fcttext']

    return ""

def sayWeather(mic, weather):
    if weather:
        weather = replaceAcronyms(weather)
        mic.say('I', weather)
    else:
        mic.say('A', "I'm sorry, I can't seem to access that information.")

def dayOfWeek(dayInt):
    """
    Takes the day of the week as integar and returns the
    name of the day as a string
    """
    if dayInt == 0:
        return "Monday"
    elif dayInt == 1:
        return "Tuesday"
    elif dayInt == 2:
        return "Wednesday"
    elif dayInt == 3:
        return "Thursday"
    elif dayInt == 4:
        return "Friday"
    elif dayInt == 5:
        return "Saturday"
    elif dayInt == 6:
        return "Sunday"

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
    # Tomorrow's weather
    if 'tomorrow' in text.lower():
        today = datetime.date.today().weekday()
        nextDay = today + 1
        tomorrow = dayOfWeek(nextDay)
        tomorrowWeather = getWeather(profile, tomorrow)
        sayWeather(mic, tomorrowWeather)
    # Tonight's weather
    elif 'tonight' in text.lower():
        today = datetime.date.today().weekday()
        tonight = dayOfWeek(today) + ' Night'
        tonightWeather = getWeather(profile, tonight)
        sayWeather(mic, tonightWeather)
    # Monday's weather
    elif 'monday' in text.lower():
        if 'night' in text.lower():
            weather = getExtendedWeather(profile, 'Monday Night')
        else:
            weather = getExtendedWeather(profile, 'Monday')
        sayWeather(mic, weather)
    # Tuesday's weather
    elif 'tuesday' in text.lower():
        if 'night' in text.lower():
            weather = getExtendedWeather(profile, 'Tuesday Night')
        else:
            weather = getExtendedWeather(profile, 'Tuesday')
        sayWeather(mic, weather)
    # Wednesday's weather
    elif 'wednesday' in text.lower():
        if 'night' in text.lower():
            weather = getExtendedWeather(profile, 'Wednesday Night')
        else:
            weather = getExtendedWeather(profile, 'Wednesday')
        sayWeather(mic, weather)
    # Thursday's weather
    elif 'thursday' in text.lower():
        if 'night' in text.lower():
            weather = getExtendedWeather(profile, 'Thursday Night')
        else:
            weather = getExtendedWeather(profile, 'Thursday')
        sayWeather(mic, weather)
    # Friday's weather
    elif 'friday' in text.lower():
        if 'night' in text.lower():
            weather = getExtendedWeather(profile, 'Friday Night')
        else:
            weather = getExtendedWeather(profile, 'Friday')
        sayWeather(mic, weather)
    # Saturday's weather
    elif 'saturday' in text.lower():
        if 'night' in text.lower():
            weather = getExtendedWeather(profile, 'Saturday Night')
        else:
            weather = getExtendedWeather(profile, 'Saturday')
        sayWeather(mic, weather)
    # Sunday's weather
    elif 'sunday' in text.lower():
        if 'night' in text.lower():
            weather = getExtendedWeather(profile, 'Sunday Night')
        else:
            weather = getExtendedWeather(profile, 'Sunday')
        sayWeather(mic, weather)
    # If no key words then find the current weather
    else:
        f = urllib2.urlopen('http://api.wunderground.com/api/' +
                            str(profile['keys']["weatherUnderground"]) +
                            '/forecast/q/' + profile['location'] + '.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)

        currentWeather = (parsed_json['forecast']['txt_forecast']
                          ['forecastday'][0]['fcttext'])
        sayWeather(mic, currentWeather)


def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(weathers?|temperature|forecast)\b',
                          text, re.IGNORECASE))
