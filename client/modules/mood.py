"""
Mood module

Name:           mood.py
Description: 	responds to common ways of asking "How are you?"
		determines mood based on weather, stock market, and wording of top news stories
Dependencies:	Weather Underground API (requires key)
		USA Today API (requires key)
		Google Finance API (no key required)
Author:         Brad Ahlers (github - brad999)
"""

import random, urllib2, json, re
from client import nikitapath

WORDS = ["HOW", "ARE", "YOU", "TODAY", "IS", "IT", "GOING", "HOW\'S"]

# specific statement so can be checked before most all modules
# must be before nikita_module in priority
PRIORITY = 5

def getWeather(profile):
    """
    Gets weather conditions using Weather Underground API and returns rating on a 1-5 scale (1 being the best)
    """
    OKConditions = ['thunderstorm', 'chance of a thunderstorm', 'rain', 'snow']
    GoodConditions = ['partly cloudy', 'overcast', 'chance of rain', 'chance of a thunderstorm', 'cloudy']
    GreatConditions = ['clear']
    AmazingConditions = ['sunny']

    f = urllib2.urlopen('http://api.wunderground.com/api/' + str(profile['keys']["weatherUnderground"]) + '/forecast/q/MI/Portland.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    condition = parsed_json['forecast']['simpleforecast']["forecastday"][0]["conditions"]
    condition = condition.lower()

    if condition in OKConditions:
        weather = 4
    elif condition in GoodConditions:
        weather = 3
    elif condition in GreatConditions:
        weather = 2
    elif condition in AmazingConditions:
        weather = 1
    else:
        weather = 1

    return weather

def getStock():
    """
    Gets stock market condition and returns ratings on a 1-5 scale (1 being the best)
    """
    f = urllib2.urlopen('http://finance.google.com/finance/info?client=ig&q=NASDAQ:.IXIC')
    content = f.read()
    obj = json.loads(content[3:])
    quotePercent = obj[0]['cp']

    if quotePercent == '':
        quotePercent = 0

    if -5.01 >= float(quotePercent) >= -100.00:
        stock = 5
    elif -0.60 >= float(quotePercent) >= -5.00:
        stock = 4
    elif 0.59 >= float(quotePercent) >= -0.59:
        stock = 3
    elif 5.00 >= float(quotePercent) >= 0.60:
        stock = 2
    elif 100.00 >= float(quotePercent) >= 5.01:
        stock = 1
    else:
        stock = 3

    return stock


def getNews(profile):
    """
    Gets news article titles, search them for keywords, and returns ratings on a 1-5 scale (1 being the best)
    """
    badWords = ['bomb', 'destruction', 'death', 'dead', 'war', 'hack', 'casualty', 'woe', 'kill', 'sabotage', 'strike', 'erupt', 'deception', 'abuse', 'abusive', 'ill', 'disease']
    goodWords = ['peace', 'prosper', 'adorable', 'perfect', 'cheer', 'improves', 'happy', 'glad', 'smile', 'joy', 'cure', 'heal', 'best', 'win']
    badCount = 0
    goodCount = 2

    f = urllib2.urlopen('http://api.usatoday.com/open/articles/topnews?encoding=json&api_key=' + str(profile['keys']["USAToday"]))
    content = f.read()
    parsed_json = json.loads(content)

    for x in parsed_json['stories']:
        for y in badWords:
            if y in x['title'].lower():
                badCount = badCount +1
                badArticle = x['title']
        for z in goodWords:
            if z in x['title'].lower():
                goodCount = goodCount +1
                goodArticle = x['title']

    totalCount = (goodCount - badCount)

    if -6 >= totalCount:
        news = 5
    elif -1 >= totalCount >= -5:
        news = 4
    elif 1 >= totalCount >= 0:
        news = 3
    elif 5 >= totalCount >= 2:
        news = 2
    elif totalCount >= 6:
        news = 1
    else:
        news = 3

    return news

def handle(text, mic, profile):
    """
       Responds to user-input, typically speech text, by telling a joke.

       Arguments:
       text -- user-input, typically transcribed speech
       mic -- used to interact with the user (for both input and output)
       profile -- contains information related to the user (e.g., phone number)
    """
    amazingResponses = ['I\'m the best I\'ve ever been!', 'I\'m amazing. Thanks for asking', 'I am better than heaven today!', 'I\'m unbelievable!', 'Happier than a cat in a room full of catnip.', 'I am feeling happier than ever!', 'Splendedly spectacular!', 'If I were any better, there would be two of me.', 'Fabulous!', 'Flying high, man, flying high', 'I am super dee duper!', 'Amazing and happy.', 'This is my lucky day!', 'Feeling lucky and living large.', 'I am doing fabulous today! I can hardly control myself from dancing.', 'Super fantastic!', 'I am currently in a wonderfully chocolate creative mood.', 'I\'m feeling like a good luck magnet today, everything is going my way!', 'I\'m feeling very grateful today.', 'I\'m giving her all she\'s got, captain!']
    greatResponses = ['Even better than the real thing.', 'I\'m doing great. Thanks for asking', 'I\'m just peachy keen', 'Super Duper!', 'I am feeling happy!', 'I\'m decent baby, flier than a pelican as Lil Wayne might say...', 'Purely golden.', 'Living the dream.', 'I am wonderfully giddy.', 'I am sailing the sea of love!', 'Blood pressure 120 over 80, respiration 16, CBC and chem panels normal.', 'If I were any better, Warren Buffet would buy me.', 'Delicious.', 'Wonderful.', 'As fine as a tree with oranges and grapes!', 'I\'m in tip top shape.', 'Just ducky.', 'I am psyching myself up for a load of playdates this week!', 'From what I hear, I am very good.', 'My usual devil may care self.', 'As happy as a clam.', 'Better now that you\'re here.', 'Well I\'m glad to hear from you!']
    goodResponses = ['I\'m good. Thanks for asking.', 'I\'m pretty good', 'Fine and dandy as long as no one else boogers up my day!', 'Cool as a cucumber.', 'Couldn\'t be better.', 'I\'d be better if I won the lottery.', 'peachy.', 'well and fine and good.', 'I must be OK because my name was not in today\'s obituaries.', 'I can\'t complain... I\'ve tried but no one listens.', 'As long as I can keep the kitten I found today I\'ll be fine.', 'Ebullient and full of alacrity.', 'I am better than yesterday, which is better than the day before that!', 'I\'m not unwell, thank you.', 'Quite well.', 'Well I did just swallow a rather large and strange looking insect, but I hear they are full of protein. So I guess I\'m great.', 'I could really go for a back massage.', 'Getting stronger.', 'Somewhere between drab and fab.', 'Learning.']
    okResponses = ['Fair to middling, mostly middling.', 'Thankfully alive and still somewhat young and healthy, in this economy what more can I ask for?', 'Just happy to be above ground.', 'I\'m so so.', 'Upright and still breathing.', 'Not dead yet!', 'I\'m about as excited as a parking spot.', 'Worse than yesterday but better than tomorrow', 'Still among the living!', 'I am still breathing.', 'I am unique and me.', 'I am not doing so well today, my cat went on the roof, my car door won\'t open and my head hurts. Other than that I\'m great.', 'I am doing pretty well since I woke up on this side of the grass instead of under it.' , 'Well, I\'m not in prison. I\'m not in the hospital. I\'m not in the grave. So I reckon I\'m fairing pretty well.', 'Ready for a nap.', 'I could really go for a walk, but first I need some legs.', 'Trying to come out on top.', 'Under construction.', 'Instead of waking up on the wrong side of the bed, I think I woke up underneath it.', 'Woke up on the wrong side of the bed.']
    badResponses = ['I\'m pretty moody today, but thanks for asking', 'I\'m pretty upset today', 'Today isn\'t my best day, but thanks for asking', 'Hopefully not as good as I\'ll ever be.', 'Terrible. Not that you really care.', 'I have my complaints.', 'I am better than yesterday but not as good as I will be tomorrow.', 'Old enough to know better.', 'Standing in the eye of the storm.', 'I still am.', 'I am fine as frogs hair.', 'Worn out from doing things.', 'Strange and getting stranger!', 'Still keeping up with the kids', 'I\'m feeling a little stressed today.', 'With all that\'s going on in the world, things have been better.', 'Oh, you know.', 'I could be better.', 'I could complain, but I\'m not going to.', 'I am.', 'Trying to fit the good in with the bad.', 'Not in the mood to discuss how I feel, but thanks for asking.', 'Just hug me and leave it at that.', 'Ready for my meds.', 'Ready for a beer.', 'Ready for a stiff drink.', 'Get back to me on that.', 'I feel like crap!']

    #Get conditions that determine mood. Values returned are integars (1-5, with 1 being the best)
    weather = getWeather(profile)
    stock = getStock()
    news = getNews(profile)

    #Average conditions
    moodScale = (weather + stock + news)/3

    #Verbalize mood
    if moodScale == 1:
       mood = random.choice(amazingResponses)
    if moodScale == 2:
       mood = random.choice(greatResponses)
    if moodScale == 3:
       mood = random.choice(goodResponses)
    if moodScale == 4:
       mood = random.choice(okResponses)
    if moodScale == 5:
       mood = random.choice(badResponses)

    mic.say('I',mood)


def isValid(text):
    """
        Returns True if the input is related to mood.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(how are you today|how is it going|how are you|how\'s it going)\b', text, re.IGNORECASE))
