"""
Mood module
Name: movie.py 
Description:    responds to the word "movie" 
                recommends top rated movies to watch based on user input (home vs. theater, genre)
Dependencies:    Plex DB for home recommendations
                           (located at /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/com.plexapp.plugins.library.db)
                 sqlite 3 installed
                 Rotten Tomatoes API (requires key)
"""
import random, urllib2, json, re, sqlite3, operator

WORDS = ["MOVIE", "HOME", "THEATER", "COMEDY", "DRAMA", "ROMANTIC", "LOVE", "ROMANCE", "ACTION", "THRILLER", "SCARY", "MYSTERY", "CRIME", "FUNNY", "YES", "NO"]


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """
    
    def movieGenre(text, frustrationCounter):
        """
            Determines and returns movie genre based on user input
        """
        genreOptions = ['comedy', 'drama', 'action', 'crime', 'thriller', 'mystery', 'romantic']
        
        if 'comedy' in text.lower() or 'funny' in text.lower():
            genre = 'comedy'
        elif 'drama' in text.lower():
            genre = 'drama'
        elif 'romantic' in text.lower() or 'love' in text.lower() or 'romance' in text.lower():
            genre = 'romantic'
        elif 'action' in text.lower():
            genre = 'action'
        elif 'crime' in text.lower():
            genre = 'crime'
        elif 'thriller' in text.lower() or 'scary' in text.lower():
            genre = 'thriller'
        elif 'mystery' in text.lower():
            genre = 'mystery'
        else:
           # If this is the first attempt then ask again, else system picks genre
           # !! add any genre option and make it default
            if frustrationCounter == 0:
                mic.say("I'm sorry. I don't understand the type of movie you're looking for. Please say a genre such as comedy, action, romance, et cetera.")
                genre = movieGenre(mic.activeListen(), 1)
            else:
                mic.say("I'm sorry. I can't find the genre you're inquiring about. I'm going to pick a genre for you.")
                genre = 'comedy' #default to comedy, random currently not working str(random.choice(genreOptions))
 
        return genre
    
    def whereToWatch(text, frustrationCounter):
        """
            Determines and returns location to watch movie based on user input
        """
        if 'home' in text.lower():
            location = 'home'
        elif 'theater' in text.lower():
            location = 'theater'
        else:
            if frustrationCounter == 0:
                mic.say("I didn't catch that. Do you want to find a movie to watch at home or at the movie theater?")
                location = whereToWatch(mic.activeListen(), 1)
            # If this is the first attempt then ask again, else assume movie will be watched at home
            else:
                mic.say("I'm sorry. We seem to be having trouble getting on the same page. I'm going to assume you're looking for a movie to watch at home.")
                location = 'home'
        
        return location
        
    def queryPlex(genre):
        try:
            dbCon = sqlite3.connect('/home/pi/com.plexapp.plugins.library.db')
            
            #select all movie titles in the chosen genre
            # !! change to select movies unwatched in the last year
            sql = "SELECT title FROM metadata_items WHERE library_section_id=4 AND tags_genre LIKE \'%" + genre + "%\'  ORDER BY rating;"
            
            cur = dbCon.cursor()
            cur.execute(sql)
            
            tempMovies = cur.fetchall()
            movies = [x[0] for x in tempMovies]
            
            #provide 3 random movies from the selection
            selections = random.sample(movies,3)

        except sqlite3.Error, e:
            selections = 'error'
            
        return selections
        
        
    def queryTheater():
        # Retrieves top rated and most recently released movies
        f = urllib2.urlopen('http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?apikey=' + str(profile['keys']["rottenTomatoes"]))
        content = f.read()
        parsed_json = json.loads(content)
        
        moviesRated = {x['title'] : x['ratings']['audience_score'] for x in parsed_json['movies']}
        highestRated = sorted(moviesRated.items(), key=operator.itemgetter(1), reverse=True)
        moviesReleased = {x['title'] : x['release_dates']['theater'] for x in parsed_json['movies']}
        recentRelease = sorted(moviesReleased.items(), key=operator.itemgetter(1), reverse=True)

        return highestRated, recentRelease
            
    #First determine whether to find a movie to watch at home (Plex) or at the movie theater
    frustrationCounter = 0
    mic.say("Are you looking for a movie to watch at home or at the theater?")
    location = whereToWatch(mic.activeListen(), frustrationCounter)
    
    if location == 'home':
        #Determine movie genre
        frustrationCounter = 0
        mic.say("What type of movie would you like to watch?")
        genre = movieGenre(mic.activeListen(), frustrationCounter)
        
        selections = queryPlex(genre)
        if selections == 'error':
            mic.say("I'm sorry the Plex server is currenty unavailable. Please try again later.")
        else:
            mic.say("I recommend either " + selections[0] + ", " + selections[1] + ", or " + selections[2] + ". Do any of these sound good?")
            YorN = mic.activeListen()
            if 'no' in YorN.lower() or 'nope' in YorN.lower() or 'nah' in YorN.lower():
                selections = queryPlex(genre)
                mic.say("I think " + selections[0] + ", " + selections[1] + ", or " + selections[2] + " would also be good. I hope this was helpful.")
            else:
                mic.say("Happy to be of help. Enjoy your movie!")
    elif location == 'theater':
        highestRated, recentRelease = queryTheater()
        words = "The top three rated movies currently showing in theaters are " + highestRated[0][0] + ", " + highestRated[1][0] + ", and " + highestRated[2][0] + ". The most recently released movies are " + recentRelease[0][0] + ", " + recentRelease[1][0] + ", and " + recentRelease[2][0] + "."
        mic.say(words)
        mic.say("Would you like me to repeat those listings?")
        YorN = mic.activeListen()
        if 'no' in YorN.lower() or 'nope' in YorN.lower() or 'nah' in YorN.lower():
            mic.say("OK, enjoy the show!")
        else:
            mic.say("OK, try to pay attention this time.")
            mic.say(words + "Enjoy the show!")
    
def isValid(text):
    """
        Returns True if the input is related to movie.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(movie)\b', text, re.IGNORECASE))

