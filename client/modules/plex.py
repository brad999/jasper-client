"""
Plex module
Name:           plex.py
Description:    responds to the word "plex"
                controls plex client (play,pause,stop)
Dependencies:   Plex DB
                    (located at /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db)
                active Plex client, client configured in profile.yaml
Author:         Brad Ahlers (github - brad999)
"""

import random, urllib2, json, re, sqlite3, operator

WORDS = ["PLEX","PLAY","PAUSE","STOP","YES", "NO"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by telling a joke.
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """
    def determineAction(text,frustrationCounter):
        if 'play' in text.lower():
            action = 'play'
        elif 'pause' in text.lower():
            action = 'pause'
        elif 'stop' in text.lower():
            action = 'stop'
        else:
           # If this is the first attempt then ask again, else give up
            if frustrationCounter == 0:
                mic.say("I'm sorry. I don't understand what you would like me to do. Please pick between play, pause, or stop.")
                action = determineAction(mic.activeListen(), 1)
            else:
                mic.say("I'm sorry. I still don't understand you. Please try again later once you learn to speech.")
                action = 'quit'

        return action, text

    def findMovie(words):
        try:
            dbCon = sqlite3.connect('/home/pi/com.plexapp.plugins.library.db')

            #select any movie titles that contain the first word of what was said after "play"
            sql = "SELECT title, id FROM metadata_items WHERE library_section_id=4 AND title LIKE \'%" + words[0] + "%\' ORDER BY title;"
            cur = dbCon.cursor()
            cur.execute(sql)

            tempMovies = cur.fetchall()

            #check for an exact match first
            for x in tempMovies:
                if x[0] == ' '.join(words):
                    return x

            #if only one result found in SQL, return it
            if len(tempMovies) == 1:
                return tempMovies

            #loop over titles searching for best match one word at a time
            found = 'false'
            counter = 1
            while found == 'false':
            #loop over all movies returned from SQL
                for x in tempMovies:
                    #search for words in the title to find a match
                    #add one word each search
                    m = re.search(' '.join(words[0:counter]), x[0], re.IGNORECASE)
                    #if title does not match remove it from list
                    if not m:
                        tempMovies.remove(x)
                #if results are narrowed to one match then exit
                if len(tempMovies) == 1:
                    found = 'true'
                #if five words have been checked and loop is still running exit
                if counter >= 5:
                    found = 'true'
                counter = counter + 1

            return tempMovies

        except sqlite3.Error, e:
            return 'error'

    def playMovie(movie):
        #build URL
        URL = 'http://' + str(profile['PlexClients']["selfIP"]) + ':' + str(profile['PlexClients']["selfPort"]) + \
              '/player/playback/playMedia?key=%2Flibrary%2Fmetadata%2F' + str(movie[0][1]) + \
              '&offset=0&X-Plex-Client-Identifier=' + str(profile['PlexClients']["selfID"]) + \
              '&machineIdentifier=' + str(profile['PlexServerID']) + '&address=' + str(profile['PlexServerIP']) + \
              '&port=' + str(profile['PlexServerPort']) + '&protocol=http&path=http%3A%2F%2F' + \
              str(profile['PlexServerIP']) + '%3A' + str(profile['PlexServerPort']) + '%2Flibrary%2Fmetadata%2F' +\
              str(movie[0][1])

        urllib2.urlopen(URL)

    #First determine action
    frustrationCounter = 0
    if 'play' in text.lower():
        action = 'play'
    elif 'pause' in text.lower():
        action = 'pause'
    elif 'stop' in text.lower():
        action = 'stop'
    else:
        mic.say("How would you like to control Plex? Please say play, pause, or stop.")
        action, text = determineAction(mic.activeListen(),frustrationCounter)

    if action == 'play':
        #determine what user would like to play
        #find anything said after "play"
        x = re.search("play (.*)",text, re.IGNORECASE)
        y = x.group(1)
        words = y.split()
        #parse the list of words to find a matching movie
        #return the name of the movie and information required to play
        movie = findMovie(words)
        #play movie if match is found, else notify
        if len(movie) == 1:
            #play the movie
            playMovie(movie)
            mic.say("Now playing" + str(movie[0][0]) + "...")
        elif len(movie) == 0:
            mic.say("I'm sorry. I did not find any movie matching that name.")
        else:
            # !!add logic to pick movie when mutliples are returned
            mic.say("I found multiple movies matching your request and am too stupid to know how to handle this. Play your movie yourself.")
    elif action == 'pause':
        #send pause command to Plex client
        # !! add ability to control multiple clients
        # !! add intelligence to know if something is actually playing
        urllib2.urlopen('http://' + str(profile['PlexClients']["selfIP"]) + ':' + str(profile['PlexClients']["selfPort"]) + '/player/playback/pause')
    elif action == 'stop':
        #send stop command to Plex client
        # !! add ability to control multiple clients
        # !! add intelligence to know if something is actually playing
        urllib2.urlopen('http://' + str(profile['PlexClients']["selfIP"]) + ':' + str(profile['PlexClients']["selfPort"]) + '/player/playback/stop')

def isValid(text):
    """
        Returns True if the input is related to movie.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(plex|play|pause|stop)\b', text, re.IGNORECASE))
