"""
Math module
Name:           math.py
Description:    responds to math related words (add, subtract, divide, multiply, etc)
                performs simple operations, rounds decimals
Dependencies:   none
Author:         Brad Ahlers (github - brad999)
"""

import re, math
from client import app_utils

WORDS = ["ADD", "SUBTRACT", "DIVIDED", "MULTIPLIED", "PLUS", "MINUS", 'TIMES']
ns = vars(math).copy()
ns['__builtins__'] = None

def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text.
        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone number)
    """

    numberWords = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
        "hundred", "thousand", "million", "billion", "trillion"]

    #convert text to lowercase
    text = text.lower()

    #convert operator words to symbols
    text = app_utils.convertOperators(text)

    #find first number word before, between, and after symbols
    #convert everything from first number word to operator to an integar
    splitText = re.split('([\+|\-|\*|\/])',text)
    statement = ''
    #remove everything before first number word
    splitWords = re.split('(\W+)',splitText[0])
    for word in splitWords:
        if word in numberWords:
            break
        else:
            splitWords.remove(word)
    splitText[0] = "".join(splitWords)

    for section in splitText:
        #removing leading and trailing whitespace
        section = section.strip()
        #if operator add to statement
        if '*' in section or '/' in section or '-' in section or '+' in section:
            statement = statement + re.sub(' ','',section,re.IGNORECASE)
        #if not operator convert to number
        else:
            #convert number words to numbers
            statement = statement + str(app_utils.text2int(section))

    #do math
    solution = eval(statement,ns)
    mic.say('I',str(solution))

def isValid(text, intent):
    """
        Returns True if the input is related to math.
        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(add|subtract|divided|multiplied|plus|minus|times)\b', text, re.IGNORECASE))
