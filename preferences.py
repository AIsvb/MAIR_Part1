# Part 1b - preference extraction
# Dirk Vet 
# 4681797
# Methods in AI research 2023
#
# Makes use of the Levenshtein library from https://maxbachmann.github.io/Levenshtein/levenshtein.html 
#
#
#3.  Extract preferences
#  3a. Preprocess user input to lower case and without punctuation marks
#  3b. Implement keyword matching algorithm with Levenshtein edit distance


import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from collections import Counter, defaultdict

import nltk
from nltk.corpus import stopwords
import random
import string
from Levenshtein import distance
import re

PATH = "restaurant_info.csv"


def initialize_db(filename):
    """
    Returns a dataframe from the given CSV file.
    filename: The name of the CSV file.
    """
    return pd.read_csv(filename) 


# def find_pattern_sentence(input_str):
#     """
#     """
#     food_regex = [
#         "go to a(n)? [a-z]+", # I want to go to a bistro
#         "restaurant that serves [a-z]+ food", # I want a restaurant that serves world food
#         "restaurant serving [a-z]+ food", # I want a restaurant serving world food
#     ]
#     return 


def find_pattern(input_str):
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
            #elif word == "north" or word == "west" or word == "south" or word == "east":
            #    area = word
        
        
        # If price preference has not been found yet.
        if price == "":
            # in case of a typo or for example price=any in "any price"
            if (word == "price" or word == "priced") and idx > 0:
                price = input[idx-1]
            #elif word == "cheap" or word == "moderate" or word == "expensive":
            #    price = word

    return food, area, price


def apply_levenshtein(db, food, area, price):
    """
    Apply the levenshtein distance measure to correct spelling mistakes in the
    user preferences. Return the corrected preferences.
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
                if dist <= 3:
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
                food, area, price = find_pattern(user_input)

                food, area, price = apply_levenshtein(db, food, area, price)
                print(f'PREFERENCES: food={food}, area={area}, price={price}')
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Quitting")
 
    
# I'm looking for world food
# I want a restaurant that serves world food
### I want a restaurant serving Swedish food
# I'm looking for a restaurant in the center
# I would like a cheap restaurant in the west part of town
# I'm looking for a moderately priced restaurant in the west part of town
# I'm looking for a restaurant in any area that serves Tuscan food
# Can I have an expensive restaurant
# I'm looking for an expensive restaurant and it should serve international food
# I need a Cuban restaurant that is moderately priced
# I'm looking for a moderately priced restaurant with Catalan food
# What is a cheap restaurant in the south part of town
# What about Chinese food
# I wanna find a cheap restaurant
# I'm looking for Persian food please
# Find a Cuban restaurant in the center
    

    

