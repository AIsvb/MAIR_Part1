from transition_handles import *
from preferences import extract_prefs
import pandas as pd


def transition(state_info, dialog_act):
    match state_info["current_state"]:
        case "Welcome":
            state_info = handle_welcome(dialog_act, state_info)
        case "RequestPreferences":
            state_info = handle_request_preferences(dialog_act, state_info)
        case "AskFoodType":
            state_info = handle_ask_food_type(dialog_act, state_info)
        case "AskPriceRange":
            state_info = handle_ask_price_range(dialog_act, state_info)
        case "AskArea":
            state_info = handle_ask_area(dialog_act, state_info)
        case "AskForFurtherPreferences":
            state_info = handle_ask_for_further_preferences(dialog_act, state_info)
        case "TellLookupResults":
            state_info = handle_tell_lookup_results(dialog_act, state_info)
        case "OfferFurtherInformation":
            state_info = handle_offer_further_information(dialog_act, state_info)
        case "AskForAcceptance":
            state_info = handle_ask_for_acceptance(dialog_act, state_info)

    return state_info


def act(data, state_info):
    if state_info["current_state"] == "Welcome":
        state_info = set_initial_state_info(state_info["formalOn"])
    if state_info["current_state"] == "TellLookupResults":
        state_info["results"] = lookup(data, state_info)
    if state_info["current_state"] == "OfferFurtherInformation":
        state_info["current_info"] = retrieve_restaurant_info(state_info)
    if state_info["current_state"] == "Exit":
        print(get_text(state_info))
        state_info["end_conversation"] = True
        return state_info, ""

    state_info["utterance"] = get_text(state_info)
    user_input = input(state_info["utterance"])

    if user_input == "quit":
        state_info["end_conversation"] = True
        return state_info, ""

    state_info = extract_information(state_info, user_input)

    return state_info, user_input


def set_initial_state_info(formalOn):
    info = {"current_state": "Welcome",
            "preferences": {"pricerange": "",
                              "area": "",
                              "food": ""},
            "additional_preferences": {"touristic": False,
                                         "assigned seats": False,
                                         "children": False,
                                         "romantic": False},
            "utterance": "",
            "formalOn": formalOn,
            "results": pd.DataFrame(),
            "current_info": pd.Series(),
            "current_suggestion": 0,
            "end_conversation": False}

    return info


def extract_information(state_info, user_input):
    for pref in state_info["additional_preferences"].keys():
        if pref in user_input:
            state_info["additional_preferences"][pref] = True
            user_input = user_input.replace(pref, "")

    if state_info["current_state"] == "AskFoodType":
        _, food, _ = extract_prefs(user_input, "food")
        if food != "":
            state_info["preferences"]["food"] = food

    elif state_info["current_state"] == "AskPriceRange":
        _, _, price = extract_prefs(user_input, "pricerange")
        if price != "":
            state_info["preferences"]["pricerange"] = price

    elif state_info["current_state"] == "AskArea":
        area, _, _ = extract_prefs(user_input, "area")
        if area != "":
            state_info["preferences"]["area"] = area

    output = extract_prefs(user_input)
    for key, val in zip(["area", "food", "pricerange"], output):
        if val != "":
            state_info["preferences"][key] = val

    return state_info


def get_text(state_info):
    match state_info["current_state"]:
        case "Welcome":
            line = ["Welcome to the system, enter your preferences for a restaurant. ",
            "Hello, welcome to the restaurant recommendation system. "
            "You can ask for restaurants by area, price range or food type. How may I help you? "][state_info["formalOn"]]
        case "RequestPreferences":
            line = ["Tell me your preferences. ", "Please tell me your preferences. "][state_info["formalOn"]]
        case "AskFoodType":
            line = ["What kind of food? ", "What kind of food do you prefer?"][state_info["formalOn"]]
        case "AskPriceRange":
            line = ["What pricerange? ", "What prices are you looking for?"][state_info["formalOn"]]
        case "AskArea":
            line = ["What part of town? ", "In what part of town would you like the restaurant to be? "][state_info["formalOn"]]
        case "AskForFurtherPreferences":
            line = ["Any other preferences? ", "Do you have additional preferences? "][state_info["formalOn"]]
        case "TellLookupResults":
            if len(state_info["results"]) > 0:
                name = state_info["results"].iloc[state_info["current_suggestion"]].restaurantname
                food = state_info["results"].iloc[state_info["current_suggestion"]].food
                area = state_info["results"].iloc[state_info["current_suggestion"]].area
                pricerange = state_info["results"].iloc[state_info["current_suggestion"]].pricerange
                utterance = f"{name} is a restaurant which"
                if not pd.isna(food):
                    utterance += f" serves {food} food"
                if not pd.isna(pricerange):
                    utterance += f" has {pricerange} prices"
                if not pd.isna(area):
                    utterance += f" and is in the {area} of town"
                utterance += ". This is all known information about food type, price range and area."
                line = utterance + get_string_for_additional_requirements(
                    state_info["results"].iloc[state_info["current_suggestion"]], state_info)
            else:
                line = ["No restaurant meets your preferences. Change them. ",
                        "Sorry, but there is no restaurant that meets your preferences. "
                        "Could you please alter your preferences? "][state_info["formalOn"]]
        case "OfferFurtherInformation":
            utterance = ["This is all the info known:\n",
                 "The following information about the restaurant is known:\n"][state_info["formalOn"]]
            for cat, val in state_info["current_info"].items():
                utterance += f"{cat}: {val}\n"
            utterance += ["Anything else I can do? ",
                  "How can I help you further? "][state_info["formalOn"]]
            line = utterance
        case "AskForAcceptance":
            line = ["There are no alternatives. Do you want the current suggestion? ",
                    "Sorry, there are no alternatives. Do you accept the current suggestion?"][state_info["formalOn"]]
        case "Exit":
            line = ["Ok. Thanks for using this DMS.",
                    "Okay,thank you for making use of this DMS. Have a nice day!"][state_info["formalOn"]]
    return line

def retrieve_restaurant_info(state_info):
    info = state_info["results"].iloc[state_info["current_suggestion"]][["phone", "addr", "postcode"]]
    for cat, val in info.items():
        if pd.isna(val):
            info[cat] = "unknown"

    return info


def lookup(data, state_info):
    """
    Lookup the restaurants that satisfy the preferences of the user.
    """
    results = data.copy()
    masks = [results[column] == value for column, value in state_info["preferences"].items() if value != "any"]
    if len(masks) > 0:
        combined_mask = pd.concat(masks, axis=1).all(axis=1)
        return filter_on_additional_requirements(results[combined_mask], state_info)
    else:
        return results


def filter_on_additional_requirements(df, state_info):

    if state_info["additional_preferences"]["touristic"]:
        return df[((df["pricerange"] == "cheap") & (df["quality"] == "good")) | (df["food"].isin(["chinese", "italian", "european", "indian", "british", "asian oriental"]))]
    elif state_info["additional_preferences"]["assigned seats"]:
        return df[df["crowdedness"] == "busy"]
    elif state_info["additional_preferences"]["children"]:
        return df[df["stay"] == "short"]
    elif state_info["additional_preferences"]["romantic"]:
        return df[(df["stay"] == "long") | (df["crowdedness"] == "not busy")]
    else:
        return df


def get_string_for_additional_requirements(df, state_info):
    if state_info["additional_preferences"]["touristic"]:
        if df.pricerange == "cheap" and df.quality == "good":
            return [" This is touristic because it is cheap and has good food. ",
                    " This restaurant is touristic, because it is cheap and has good food quality."][state_info["formalOn"]]
        elif df.food in ["chinese", "italian", "european", "indian", "british", "asian oriental"]:
            return [f" This is touristic because the {df.food} food is popular. ",
                    f" This restaurant is touristic, because the {df.food} food it serves is popular."][state_info["formalOn"]]
    elif df.crowdedness == "busy" and state_info["additional_preferences"]["assigned seats"]:
        return [" It is very busy so it has assigned seats. ",
                " This restaurant most likely has assigned seats, because it is a busy restaurant."][state_info["formalOn"]]
    elif df.stay == "short" and state_info["additional_preferences"]["children"]:
        return [" Perfect for kids since they do not allow you to stay long. ",
                " Because this restaurant does not allow you to stay long, it is perfect for children."][state_info["formalOn"]]
    elif state_info["additional_preferences"]["romantic"]:
        if df.stay == "long":
            return [" This is a romantic place because you can stay longer. ",
                    " This restaurant is romantic, because it allows you to stay long."][state_info["formalOn"]]
        elif df.crowdedness == "not busy":
            return ["Since it is not busy it is romantic. ",
                    " Because this restaurant is not busy, it is a good place for a romantic night out."][state_info["formalOn"]]
    else:
        return ""