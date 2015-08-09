"""
Plex module

Name:           plex.py

Description:    responds to the words "plex", "play", "pause",
                "stop", and "rewind"
                controls plex client (play,pause,stop,rewind)

Dependencies:   Plex DB
                (located at /var/lib/plexmediaserver/Library/Application
                Support/Plex Media Server/Plug-in Support/Databases/
                com.plexapp.plugins.library.db)
                active Plex client, client configured in profile.yaml

Author:         Brad Ahlers (github - brad999)
"""

import urllib2
import json
import re
import sqlite3
from client import app_utils

WORDS = ["PLEX", "PLAY", "PAUSE", "STOP", "YES", "NO", "REWIND", "PAWS"]
PRIORITY = 4


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text.
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user
    """

    def determineAction(text, frustrationCounter):
        if 'play' in text.lower():
            action = 'play'
        elif 'pause' in text.lower():
            action = 'pause'
        elif 'stop' in text.lower():
            action = 'stop'
        elif 'rewind' in text.lower():
            action = 'rewind'
        else:
            # If this is the first attempt then ask again, else give up
            if frustrationCounter == 0:
                mic.say('A', "I'm sorry. I don't understand what you \
                        would like me to do. Please pick between play, \
                        pause, or stop.")
                action = determineAction(mic.activeListen(), 1)
            else:
                mic.say('A', "I'm sorry. I still don't understand you. \
                        Please try again later once you learn to speech.")
                action = 'quit'

        return action, text

    def findMovie(movie):
        # tries to find the movie provided in the plex database
        # return the name of the movie and information required to play
        try:
            dbCon = sqlite3.connect('/home/pi/com.plexapp.plugins.library.db')

            # select any movie titles that contain the first word
            sql = "SELECT title, id \
                   FROM metadata_items \
                   WHERE library_section_id=1 \
                   AND title \
                   LIKE \'%" + movie + "%\' ORDER BY title;"
            cur = dbCon.cursor()
            cur.execute(sql)

            tempMovies = cur.fetchall()

            # if only one result found in SQL, return it
            if len(tempMovies) == 1:
                return tempMovies

            # convert words to numbers before checking match
            words = app_utils.convertNumberWords(movie.lower())
            # check for an exact match first
            for x in tempMovies:
                if x[0].lower() == words:
                    it = iter(x)
                    tempMovie = zip(it, it)
                    return tempMovie

            # loop over titles searching for best match one word at a time
            found = 'false'
            counter = 1
            while found == 'false':
                # loop over all movies returned from SQL
                for x in tempMovies:
                    # search for words in the title to find a match
                    # add one word each search
                    m = re.search(' '.join(words[0:counter]),
                                  x[0], re.IGNORECASE)
                    # if title does not match remove it from list
                    if not m:
                        tempMovies.remove(x)
                # if results are narrowed to one match then exit
                if len(tempMovies) == 1:
                    found = 'true'
                # if five words have been checked and
                # loop is still running exit
                if counter >= 5:
                    found = 'true'
                counter = counter + 1

            return tempMovies

        except sqlite3.Error:
            return 'error'

    def playMovie(movie):
        # !! check if TV is connected and turn on if off
        # build URL
        URL = 'http://' + str(profile['PlexClients']["selfIP"]) + ':' + \
              str(profile['PlexClients']["selfPort"]) + \
              '/player/playback/playMedia?key=%2Flibrary%2Fmetadata%2F' + \
              str(movie[0][1]) + '&offset=0&X-Plex-Client-Identifier=' + \
              str(profile['PlexClients']["selfID"]) + \
              '&machineIdentifier=' + \
              str(profile['PlexServerID']) + '&address=' + \
              str(profile['PlexServerIP']) + '&port=' + \
              str(profile['PlexServerPort']) + \
              '&protocol=http&path=http%3A%2F%2F' + \
              str(profile['PlexServerIP']) + '%3A' + \
              str(profile['PlexServerPort']) + '%2Flibrary%2Fmetadata%2F' + \
              str(movie[0][1])

        urllib2.urlopen(URL)

    def theHardWay(profile, text):
        # First determine action
        frustrationCounter = 0
        if 'play' in text.lower():
            action = 'play'
        else:
            mic.say('A', "How would you like to control Plex? \
                    Please say play, pause, or stop.")
            action, text = determineAction(mic.activeListen(),
                                           frustrationCounter)

        if action == 'play':
            # determine if anything was said after play
            if re.search("(play) (.*)", text, re.IGNORECASE):
                x = re.search("(play) (.*)", text, re.IGNORECASE)
                words = x.group(2)
            # if nothing was said after play, prompt for movie name
            else:
                mic.say('A', "What movie would you like to play?")
                words = mic.activeListen()
            # find movie in Plex database
            temp = words.split()
            movie = findMovie(temp[0])
            # play movie if match is found, else notify
            if len(movie) == 1:
                # play the movie
                playMovie(movie)
                # verify movie choice
                mic.say('A', "Would you like to play " +
                        str(movie[0][0]) + "?")
                if app_utils.YesOrNo(mic.activeListen()):
                    mic.say('I', "Now playing " + str(movie[0][0]) + "...")
                else:
                    mic.say('A', "Would you like me to try again or quit?")
                    choice = mic.activeListen()
                    if 'try' in choice.lower() or 'again' in choice.lower():
                        handle('play', mic, profile)
                    else:
                        mic.say('A', "Alright, I'm giving up.")
            elif len(movie) == 0:
                mic.say('A', "I'm sorry. I did not find any movie \
                        matching that name.")
            else:
                # !!add logic to pick movie when mutliples are returned
                mic.say('A', "I found multiple movies matching your request \
                        and am too stupid to know how to handle this. Play \
                        your movie yourself.")

    # play operation
    if 'play' in text.lower():
        # attempt to use wit to determine intent
        intent = app_utils.determineIntent(profile, text)
        # Use intent if found
        if intent:
            # check intent (play, stop, rewind, etc)
            if json.loads(json.dumps(intent))['intent'] == 'query_movie':
                if json.loads(json.dumps(intent))['entities']['title'][0]['suggested']:
                    movie = json.loads(json.dumps(intent))['entities']['title'][0]['value']
                    movieID = findMovie(movie)
                    playMovie(movieID)
                    mic.say('I', "Now playing " + str(movie) + "...")
                else:
                    theHardWay(profile, text)
            else:
                theHardWay(profile, text)
        # if no intent is found, do it the hard way
        else:
            theHardWay(profile, text)
    elif 'pause' in text.lower() or 'paws' in text.lower():
        # send pause command to Plex client
        # !! add ability to control multiple clients
        # !! add intelligence to know if something is actually playing
        urllib2.urlopen('http://' + str(profile['PlexClients']["selfIP"]) +
                        ':' + str(profile['PlexClients']["selfPort"]) +
                        '/player/playback/pause')
    elif 'stop' in text.lower():
        # send stop command to Plex client
        # !! add ability to control multiple clients
        # !! add intelligence to know if something is actually playing
        urllib2.urlopen('http://' + str(profile['PlexClients']["selfIP"]) +
                        ':' + str(profile['PlexClients']["selfPort"]) +
                        '/player/playback/stop')
    elif 'rewind' in text.lower():
        urllib2.urlopen('http://' + str(profile['PlexClients']["selfIP"]) +
                        ':' + str(profile['PlexClients']["selfPort"]) +
                        '/player/playback/stepBack')
    else:
        mic.say('E', "I'm sorry I don't know how to help you with that.")


def isValid(text):
    """
        Returns True if the input is related to plex.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(plex|play|pause|stop|' +
                          r'rewind|paws)\b', text, re.IGNORECASE))
