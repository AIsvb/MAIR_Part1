# Dirk Vet
# 4681797
# Methods in AI research - part 1c (extends 1b)
#
# (part 1b) This file extracts the food, area, price preferences from user input  
# in a restaurant dialogue system. By keyword matching and calculating the 
# Levenshtein distance the preferences are captured.
# Makes use of the Levenshtein library from https://maxbachmann.github.io/Levenshtein/levenshtein.html 
#
# (part 1c) Part 1b is extended by allowing additional user preferences.
# Restaurants are recommended that satisfy the user preferences based on the 
# implication rules beneath.
#
# id - antedecent - consequent - t/f - description
# 1	- cheap AND good food - touristic - True - a cheap restaurant with good food attracts tourists
# 2	- romanian - touristic - False - Romanian cuisine is unknown for most tourists and they prefer familiar food
# 3	- busy - assigned seats - True - in a busy restaurant the waiter decides where you sit
# 4	- long stay	children - False - spending a long time is not advised when taking children
# 5	- busy - romantic - False - a busy restaurant is not romantic
# 6	- long stay - romantic - True - spending a long time in a restaurant is romantic
#


import numpy as np
import pandas as pd 
import random
from Levenshtein import distance
import re
from collections import defaultdict

# Path to database of restaurants
PATH = "restaurant_info_additionalpref.csv"
# Maximal allowed levenshtein distance
MAX_DISTANCE = 3


def initialize_db(filename):
    """
    Returns a dataframe from the given CSV file.
    filename: The name of the CSV file.
    """
    return pd.read_csv(filename) 


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
    words in the sentence to the preferences in the databse and taking the
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


def get_add_pref(input_str, food, area, price):
    """
    Get the additional preference from the user input.
    input_str: the user input
    food: the food preference of the user
    area: the area preference of the user
    price: the price preference of the user (i.e. cheap, moderate, expensive)
    """
    additional_prefs = ["touristic", "assigned seats", "children", "romantic"]
    add_pref = ""

    for pref in additional_prefs:
        if pref in input_str:
            # Find an restaurant with this additional preference
            add_pref = pref
            add_pref_reasoning(db, add_pref, food, area, price)


def add_pref_string(rule_id):
    """
    Return the string shown to the user based on the rule id. The rule id 
    follows from the additional preference from the user.
    rule_id: the rule id number
    """
    strings = {
        1: "The restaurant is touristic because the food is good and the price is cheap",
        2: "The restaurant is touristic because the food is familiar cuisine",
        3: "The waiter will assign your seats because it is a busy restaurant",
        4: "The restaurant is good for children because it makes you stay for a short time",
        5: "The restaurant is romantic because it is not crowded",
        6: "The restaurant is romantic because it allows you to stay for a long time"  
        }
    
    return strings[rule_id]


def recommend_string(restaurant):
    """
    Returns the string for recommending a restaurant.
    restaurant: pandas dataframe entry
    """
    return (f"I recommend '{restaurant['restaurantname'].values[0]}', "
            f"it is a {restaurant['pricerange'].values[0]} "
            f"{restaurant['food'].values[0]} restaurant in the "
            f"{restaurant['area'].values[0]} part of town.")


def add_pref_reasoning(db, add_pref, food, area, price):
    """
    Find a restaurant in the database based on the additional preference.
    db: the database, csv file
    add_pref: the additional preference type
    price: the price preference of the user (i.e. cheap, moderate, expensive)
    food: the food preference of the user
    """
    # familiar cuisine with 6+ occurences in database.
    familiar_foods = ["chinese", "italian", "european", "indian", "british", "asian oriental"] 
    all_restaurants = defaultdict(list)
    db_main_pref = db

    # Create a database for only the entries that adhere to the main preferences.
    if food != "" and food != "any":
        db_main_pref = db_main_pref[db_main_pref["food"] == food]
    if area != "" and area != "any":
        db_main_pref = db_main_pref[db_main_pref["area"] == area]
    if price != "" and price != "any":
        db_main_pref = db_main_pref[db_main_pref["pricerange"] == price]

    # Collect the restaurants that follow the additional preferences.
    if add_pref == "touristic":
        # rule id = 1
        if price == "cheap" or price == "any" or price == "": 
            if len(db_main_pref.loc[db_main_pref["crowdedness"] == "busy"].values.tolist()) > 0:
                all_restaurants[1] = db_main_pref.loc[(db_main_pref["pricerange"] == "cheap") & (db_main_pref["quality"] == "good")].values.tolist()
        # rule id = 2
        if food in familiar_foods or food == "any" or food == "":
            if len(db_main_pref.loc[db_main_pref["food"].isin(familiar_foods)].values.tolist()) > 0:
                all_restaurants[2] = db_main_pref.loc[db_main_pref["food"].isin(familiar_foods)].values.tolist()
        
    if add_pref == "assigned seats":
        # rule id = 3
        if len(db_main_pref.loc[db_main_pref["crowdedness"] == "busy"].values.tolist()) > 0: 
            all_restaurants[3] = db_main_pref.loc[db_main_pref["crowdedness"] == "busy"].values.tolist()
        
    if add_pref == "children": 
        # rule id = 4
        if len(db_main_pref.loc[db_main_pref["stay"] == "short"].values.tolist()) > 0:
            all_restaurants[4] = db_main_pref.loc[db_main_pref["stay"] == "short"].values.tolist()
        
    if add_pref == "romantic":
        # rule id = 5
        if len(db_main_pref.loc[db_main_pref["crowdedness"] == "not busy"].values.tolist()) > 0:
            all_restaurants[5] = db_main_pref.loc[db_main_pref["crowdedness"] == "not busy"].values.tolist()
        # rule id = 6
        if len(db_main_pref.loc[db_main_pref["stay"] == "long"].values.tolist()) > 0:
            all_restaurants[6] = db_main_pref.loc[db_main_pref["stay"] == "long"].values.tolist()
        

    # all the id's of the rules that apply.
    rule_ids = list(all_restaurants.keys())
    
    # If recommendation has been found.
    if len(rule_ids) > 0:
        # Pick a random rule, because sometimes more rules can be applied to the 
        # given preference.
        id = random.choice(rule_ids)
        # Pick a random restaurant that satisfies the rule that applies.
        restaurant = random.choice(all_restaurants.get(id))
        
        print(recommend_string(db_main_pref.loc[db_main_pref["restaurantname"] == restaurant[0]]))
        print(add_pref_string(id))          
    else:
        print("NO RECOMMENDATIONS FOUND BASED ON MAIN PREFERENCES AND ADDITIONAL PREFERENCES")
    
 


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

                print(f'PREFERENCES: food={food}, area={area}, price={price}')

                # Print a recommended restaurant based on the additional 
                # preference if present.
                get_add_pref(user_input, food, area, price)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Quitting")
   

    

