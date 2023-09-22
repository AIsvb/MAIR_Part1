# Dirk Vet
# 4681797
# Methods in AI research - part 1b
#
# This file extracts the food, area, price preferences from user input in 
# a restaurant dialogue system. By keyword matching and calculating the 
# Levenshtein distance the preferences are captured.
# Makes use of the Levenshtein library from https://maxbachmann.github.io/Levenshtein/levenshtein.html 


import numpy as np
import pandas as pd 
from nltk.corpus import stopwords
import random
from Levenshtein import distance
import re

# Path to database of restaurants
PATH = r'data\restaurant_info.csv'
# Maximal allowed levenshtein distance
MAX_DISTANCE = 3


def initialize_db(filename):
    """
    Returns a dataframe from the given CSV file.
    filename: The name of the CSV file.
    """
    return pd.read_csv(filename) 


def find_pattern(db, input_str):
    """
    Pattern matching based on the input string. Returns the food, area and price
    preference from the user.
    input_str: the user input
    """
    input = input_str.split()
    # The food preference
    food = "" 
    # The area preference
    area = ""
    # The price preference
    price = ""
    
    db_no_nan = db[~db[:].isna()]
    # All the possible preferences in the database for a particular topic.
    possible_areas = list(set(db_no_nan.loc[:, "area"]))
    possible_foods = list(set(db_no_nan.loc[:, "food"]))
    possible_prices = list(set(db_no_nan.loc[:, "pricerange"]))

    for idx, word in enumerate(input):
        # Check if word is in database and assign the preference to the right 
        # class.
        if word in possible_areas or word == "center":
            area = word
            continue
        elif word in possible_foods:
            food = word
            continue
        elif word in possible_prices:
            price = word
            continue

        # If food preference has not been found yet.
        if food == "":
            # in case of a typo or for example food=any in "i want any food"        
            if word == "food" and idx > 0:
                food = input[idx-1]
       
        
        # If area preference has not been found yet.
        if area == "":
            # in case of a typo or for example area=any in "in any part of town"
            if (word == "part" or word == "area") and idx > 0:
                area = input[idx-1]

        
        # If price preference has not been found yet.
        if price == "":
            # in case of a typo or for example price=any in "any price"
            if (word == "price" or word == "priced") and idx > 0:
                price = input[idx-1]


    if food == "" and area == "" and price == "":
        food, area, price = levenshtein_no_pref(db, input)
    else:
        food, area, price = levenshtein_with_pref(db, food, area, price)

    return food, area, price

def levenshtein_no_pref(db, split_sent):
    """
    Apply levenshtein distance measure to correct spelling mistakes in the
    user preferences. Captures any preferences in the sentence by comparing all
    words in the sentence to the preferences in the database and taking the
    best scoring preference per class. Returns the preferences. 
    db: the database with restaurants
    split_sent: list of words forming the sentence
    """
    area, food, price, = "", "", ""
    distances = {"area": [],
                 "food": [],
                 "pricerange": []}
    db_no_nan = db[~db.isnull().any(axis=1)]    
    possible_areas = list(set(db_no_nan.loc[:, "area"]))
    possible_foods = list(set(db_no_nan.loc[:, "food"]))
    possible_prices = list(set(db_no_nan.loc[:, "pricerange"]))

    for word in split_sent:    
        # If a word is smaller than the maximum allowed Levenshtein distance,
        # it will always be used as potential preference. So ignore these 
        # irrelevant words.
        if len(word) > MAX_DISTANCE:
            # A word can have an allowed levenshtein distance for multiple 
            # preference classes, so store them in all that apply.
            distances["area"].extend([(db_word, distance(word, db_word)) for db_word in possible_areas if distance(word, db_word) <= MAX_DISTANCE])
            distances["food"].extend([(db_word, distance(word, db_word)) for db_word in possible_foods if distance(word, db_word) <= MAX_DISTANCE])
            distances["pricerange"].extend([(db_word, distance(word, db_word)) for db_word in possible_prices if distance(word, db_word) <= MAX_DISTANCE])

    # Get the preference with the smallest levenshtein distance
    if len(distances["area"]) > 0:
        area = min(distances["area"], key=lambda x:x[1])[0]
    if len(distances["food"]) > 0:
        food = min(distances["food"], key=lambda x:x[1])[0]
    if len(distances["pricerange"]) > 0:
        price = min(distances["pricerange"], key=lambda x:x[1])[0]

    return area, food, price


def levenshtein_with_pref(db, food, area, price):
    """
    Apply the levenshtein distance measure to correct spelling mistakes in the
    captured user preferences. Return the corrected preferences.
    db: the database with restaurants.
    food: the food preference string
    area: the area preference string
    price: the price preference string
    """
    correct_prefs = [] 
    for (db_label, var) in zip(["food", "area", "pricerange"], [food, area, price]):
        if var == "any" or var == "":
            correct_prefs.append(var)
        else:
            db_no_nan = db[~db[db_label].isna()]
            # List of tuples (Levenshtein distance, db label)
            distances = []
            # All the possible preferences in the database for a particular topic.
            possible_prefs = list(set(db_no_nan.loc[:, db_label]))
     
            for pref in possible_prefs:
                dist = distance(pref, var)
                # i.e. a nearby word
                if dist <= MAX_DISTANCE:
                    distances.append((pref, dist))
            
            
            # No nearby word is found in the database. This means it is a 
            # real unknown word or a word that makes no sense, but keep the 
            # preference anyway.
            if len(distances) == 0:
                correct_prefs.append(var)
                print("LEVENSHTEIN DISTANCE > 3, ASK USER NEW PREFERENCE")
            else:
                min_dist = min(distances, key=lambda x:x[1])[1]
                all_min = [correct_pref for (correct_pref, d) in distances if d == min_dist]
                # Only one preference in database found with Levenshtein 
                # distance one.
                if len(all_min) == 1:
                    correct_prefs.append(all_min[0])
                # If multiple preference with the same minimal Levenshtein 
                # distance is found, pick from these preferences one randomly.
                else:
                    correct_prefs.append(random.choice(all_min))

    return tuple(correct_prefs)

def extract_prefs(input):
    db = initialize_db(PATH)
    user_input = " ".join(re.findall("[a-z0-9 ]+", input.lower()))
    return find_pattern(db, user_input)


if __name__ == '__main__':
    db = initialize_db(PATH)
    user_input = ""
    print("Enter sentence:")
    try:
        while True:
            user_input = input() 
            if user_input == "quit": 
                quit()
            else:                     
                # Allow spaces, lowercase letters and numbers   
                user_input = " ".join(re.findall("[a-z0-9 ]+", user_input.lower()))
                print(f"{user_input}")
                food, area, price = find_pattern(db, user_input)

                print(f'PREFERENCES: food={food}, area={area}, price={price}')
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Quitting")
   

    

