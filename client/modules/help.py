# -*- coding: utf-8-*-
"""
Help module

Name:           help.py
Description:    responds to "help", "what can you do", etc
Dependencies:   N/A
Author:         Brad Ahlers (github - brad999)
"""
import re
import random

WORDS = ["HELP", "WHAT", "CAN", "YOU", "DO"]
PRIORITY = 5


def handle(text, mic, profile):
    helpItems = {
                 "birthday": {
                   "description": "provide facebook birthdays",
                   "words": "birthday",
                   "example": "Who has a birthday today?"
                 },
                 "echo": {
                   "description": "repeat speech",
                   "words": "echo, repeat, say",
                   "example": "Echo one two three four"
                 },
                 "joke": {
                   "description": "tell a joke",
                   "words": "joke, knock knock",
                   "example": "Tell me a joke"
                 },
                 "knowItAll": {
                   "description": "provide answers to varies questions",
                   "words": "who, what, when, how, tell me, define",
                   "example": "How many ounces in a cup?"
                 },
                 "life": {
                   "description": "tell you the meaning of life",
                   "words": "meaning of life",
                   "example": "What is the meaning of life?"
                 },
                 "mood": {
                   "description": "tell what mood I am in",
                   "words": "how are you, how is it going, how's it going",
                   "example": "How are you?"
                 },
                 "movie": {
                   "description": "provide recommendations for movies to watch at home or in the theater",
                   "words": "movie",
                   "example": "Can you recommend a movie for me to watch?"
                 },
                 "news": {
                   "description": "provide news headlines",
                   "words": "news, headlines",
                   "example": "What are the latest news healines?"
                 },
                 "nikita": {
                   "description": "provide information about myself",
                   "words": "you, your, yourself",
                   "example": "When were you born?"
                 },
                 "plex": {
                   "description": "play, pause, stop, or rewind movies in Plex",
                   "words": "plex, play, pause, stop, rewind",
                   "example": "Play Toy Story 3"
                 },
                 "shutdown": {
                   "description": "shut down",
                   "words": "shutdown, shut down",
                   "example": "Shutdown"
                 },
                 "text": {
                   "description": "text people",
                   "words": "text, tell",
                   "example": "Text Brad Hi. How are you?"
                 },
                 "time": {
                   "description": "provide time",
                   "words": "what time is it, what is the time",
                   "example": "What time is it?"
                 },
                 "traffic": {
                   "description": "provide information on traffic incidences and travel times",
                   "words": "traffic, crashes, accidents, commute, how long does it take to get to work",
                   "example": "How is traffic?"
                 },
                 "tv": {
                   "description": "turn on and off TV",
                   "words": "tv, television",
                   "example": "Turn off the TV."
                 },
                 "weather": {
                   "description": "provide weather information",
                   "words": "weather, temperature, forecast",
                   "example": "What is the weather suppose to be like on Friday?"
                 }
               }

    options = []
    for i in helpItems:
         options.append(helpItems[i]['description'])

    if 'what can you do' in text.lower():
        # provide 3 random options
        threeOptions = ', '.join(random.sample(options, 3))
        mic.say('I', "Some of the things I can do include, " + threeOptions +
                ". For more examples ask me again.")

def isValid(text):
    return bool(re.search(r'\bhelp|what can you do\b',
                text, re.IGNORECASE))
