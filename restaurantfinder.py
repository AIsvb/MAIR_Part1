import csv
from time import sleep
from gtts import gTTS
from playsound import playsound

# Add 4 types of configurability: all uppercase, delay before system response, formal or informal response from system, and the system outputs speech
# Each of these can be turned on by assinging it the value 1  

upperOn = 0
sleepOn = 1
formalOn = 0
speechOn = 0
delay = 2

language = 'en'

state = 'anotherrec'
currentrest = 1                                                                                                                                 # counter to keep track of which restaurant we are looking at in the list of recommendations

userpreference = ["expensive", "centre", "asian oriental"]

def clearuserpreference():
    userpreference = []
    currentrest = 0
    return userpreference, currentrest

# function that finds all restaurant recommendations for given preferences
def findrestaurants():
     restaurants = open('restaurant_info.csv', newline='')                                                     
     restaurantrecs = []                                                                                       
     iterator = csv.reader(restaurants)                                                                        
     for currentrestaurant in iterator:                                                                       
            if (currentrestaurant[1] == userpreference[0] and currentrestaurant[2] == userpreference[1] and currentrestaurant[3] == userpreference[2]):           
                 restaurantrecs.append(currentrestaurant)                                                           
     return restaurantrecs                                                                                     

                                                                                            
restaurantrec = findrestaurants()                                                                                                           # store the list of restaurant recommendations in restaurantrec
length = len(restaurantrec)                                                                                                                 # store the length of the list of restaurant recommendations

if state == 'rec1':
    # recommend the first option
    if length == 0:
        mytext = ["There is no match, change some things", 
                   "We are sorry, we could not find a restaurant that matches your preferences, try changing some things."][formalOn]
        if (sleepOn == 1):
            sleep(delay)  
        if (speechOn == 1):
            speech = gTTS(text=mytext, lang=language)
            speech.save("texttospeech.mp3")
            playsound("texttospeech.mp3")
        else:
            if (upperOn == 1):
                print(mytext.upper())
            else:
                print(mytext)
    else:                                                                                     
        rec = restaurantrec[currentrest][0]                                                                         # sets the recommendation to the first restaurant name in the recommendation list 
        mytext = [rec + " is an option. ", 
                   rec + " serves " + userpreference[2] + " food in the " + userpreference[0] + " price range."][formalOn]
        if (sleepOn == 1):
            sleep(delay)
        if (speechOn == 1):
            speech = gTTS(text=mytext, lang=language)
            speech.save("texttospeech.mp3")
            playsound("texttospeech.mp3")
        else:
            if (upperOn == 1):
                print(mytext.upper())
            else:
                print(mytext)   

if state == 'anotherrec':     
    # Case where they requested another recommendation     
    if currentrest + 1 < length:                                                                                     # check to see if there is anohter recommendation in the list    
        currentrest = currentrest + 1                                                                                # if that is the case, add 1 to the current rest so that we get the info from the next restaurant in the list   
        rec = restaurantrec[currentrest][0] 
        mytext = [rec + " is another option. ",
                   rec + " is another option that serves " + userpreference[2] + " food."][formalOn]                                                                           
        if (sleepOn == 1):
            sleep(delay)
        if (speechOn == 1):
            speech = gTTS(text=mytext, lang=language)
            speech.save("texttospeech.mp3")
            playsound("texttospeech.mp3")
        else:
            if (upperOn == 1):
                print(mytext.upper())
            else:
                print(mytext)                             
    
    else:
        mytext = ["No more recommendations, change preferences. ",
                   "We are sorry, there are no more restaurant recommendations with these preferences available, please try changing some preferences."][formalOn]                                                                                                              
        if (sleepOn == 1):
            sleep(delay)
        if (speechOn == 1):
            speech = gTTS(text=mytext, lang=language)
            speech.save("texttospeech.mp3")
            playsound("texttospeech.mp3")
        else:
            if (upperOn == 1):
                print(mytext.upper())
            else:
                print(mytext)
        restaurantrec = []                                                                                           # make the restaurant recommendations list empty
        clearuserpreference()                                                                                        # clear user preferences to start over 

def getaddr():
    address = restaurantrec[currentrest][5]
    mytext = ["Address: " + address, 
               "The address is " + address][formalOn]
    if (sleepOn == 1):
        sleep(delay)
    if (speechOn == 1):
        speech = gTTS(text=mytext, lang=language)
        speech.save("texttospeech.mp3")
        playsound("texttospeech.mp3")
    else:
        if (upperOn == 1):
            print(mytext.upper())
        else:
            print(mytext)
    return address
        
def getpostcode():
    postcode = restaurantrec[currentrest][6]
    mytext = ["Postcode: " + postcode, 
               "The postcode is " + postcode][formalOn]
    if (sleepOn == 1):
        sleep(delay)
    if (speechOn == 1):
        speech = gTTS(text=mytext, lang=language)
        speech.save("texttospeech.mp3")
        playsound("texttospeech.mp3")
    else:
        if (upperOn == 1):
            print(mytext.upper())
        else:
            print(mytext)
    return postcode
        
def getphone():
    phone = restaurantrec[currentrest][4]
    mytext = ["Phone number: " + phone, 
                "The phone number is " + phone][formalOn]
    if (sleepOn == 1):
        sleep(delay)
    if (speechOn == 1):
        speech = gTTS(text=mytext, lang=language)
        speech.save("texttospeech.mp3")
        playsound("texttospeech.mp3")
    else:
        if (upperOn == 1):
            print(mytext.upper())
        else:
            print(mytext)
    return phone
