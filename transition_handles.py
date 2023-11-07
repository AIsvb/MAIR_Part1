def handle_welcome(dialog_act, state_info):
    if dialog_act in ("inform", "reqalts"):
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])
    elif dialog_act in ("thankyou", "bye"):
        state_info["current_state"] = "Exit"
    elif dialog_act in ("restart", "repeat"):
        state_info["current_state"] = "Welcome"
    else:
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])

    return state_info


def handle_request_preferences(dialog_act, state_info):
    if dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act in ("inform", "reqalts"):
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])
    elif dialog_act in ("ack", "affirm", "confirm", "deny", "hello", "negate", "null", "repeat", "reqmore", "request"):
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])
    elif dialog_act in ("thankyou", "bye"):
        state_info["current_state"] = "Exit"
    else:
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])

    return state_info


def handle_ask_food_type(dialog_act, state_info):
    if dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act in ("inform", "reqalts"):
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])
    elif dialog_act in ("thankyou", "bye"):
        state_info["current_state"] = "Exit"
    else:
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])

    return state_info


def handle_ask_area(dialog_act, state_info):
    if dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act in ("inform", "reqalts"):
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])
    elif dialog_act in ("thankyou", "bye"):
        state_info["current_state"] = "Exit"
    else:
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])

    return state_info


def handle_ask_price_range(dialog_act, state_info):
    if dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act in ("inform", "reqalts"):
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])
    elif dialog_act in ("thankyou", "bye"):
        state_info["current_state"] = "Exit"
    else:
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])

    return state_info


def handle_ask_for_further_preferences(dialog_act, state_info):
    if dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act == "negate":
        state_info["current_state"] = "TellLookupResults"
    elif dialog_act in ("ack", "affirm"):
        state_info["current_state"] = "RequestPreferences"
    elif dialog_act in ("thankyou", "bye"):
        state_info["current_state"] = "Exit"
    else:
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])

    return state_info


def handle_tell_lookup_results(dialog_act, state_info):
    if dialog_act in ("thankyou", "bye"):
        state_info["current_state"] = "Exit"
    elif dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act in ("inform", "reqalts"):
        state_info["current_state"] = choose_transition(state_info["current_state"],
                                                        state_info["preferences"],
                                                        state_info["additional_preferences"])
    elif len(state_info["results"]) > 0:
        if dialog_act in ("ack", "affirm", "request"):
            state_info["current_state"] = "OfferFurtherInformation"
        if dialog_act == "deny":
            state_info["current_state"] = "RequestPreferences"
        if dialog_act == "reqmore":
            if len(state_info["results"]) - (state_info["current_suggestion"] + 1) > 0:
                state_info["current_suggestion"] += 1
                state_info["current_state"] = "TellLookupResults"
            else:
                state_info["current_state"] = "AskForAcceptance"

    elif len(state_info["results"]) == 0:
        if dialog_act in ("ack", "affirm", "deny"):
            state_info["current_state"] = "RequestPreferences"
    else:
        state_info["current_state"] = "TellLookupResults"

    return state_info


def handle_offer_further_information(dialog_act, state_info):
    if dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act == "deny":
        state_info["current_state"] = "RequestPreferences"
    elif dialog_act == "reqmore":
        if len(state_info["results"]) - (state_info["current_suggestion"] + 1) > 0:
            state_info["current_suggestion"] += 1
            state_info["current_state"] = "TellLookupResults"
        else:
            state_info["current_state"] = "AskForAcceptance"
    elif dialog_act in ("inform", "reqalts", "confirm"):
        state_info["current_state"] = "TellLookupResults"
    elif dialog_act in ("thankyou", "bye", "negate"):
        state_info["current_state"] = "Exit"

    else:
        state_info["current_state"] = "TellLookupResults"

    return state_info


def handle_ask_for_acceptance(dialog_act, state_info):
    if dialog_act == "restart":
        state_info["current_state"] = "Welcome"
    elif dialog_act == "confirm":
        state_info["current_state"] = "TellLookupResults"
    elif dialog_act in ("deny", "negate"):
        state_info["current_suggestion"] = 0
        state_info["additional_preferences"] = {"touristic": False,
                                                "assigned seats": False,
                                                "children": False,
                                                "romantic": False}
        state_info["current_state"] = "RequestPreferences"
    elif dialog_act in ("inform", "reqalts"):
        state_info["current_state"] = "TellLookupResults"
    elif dialog_act in ("thankyou", "bye", "ack", "affirm"):
        state_info["current_state"] = "Exit"
    elif dialog_act == "reqmore":
        return state_info

    else:
        state_info["current_state"] = "TellLookupResults"

    return state_info


def choose_transition(state, preferences, additional_preferences):
    if preferences["pricerange"] == "":
        return "AskPriceRange"
    elif preferences["food"] == "":
        return "AskFoodType"
    elif preferences["area"] == "":
        return "AskArea"
    elif state in ("AskFoodType", "AskArea", "AskPriceRange", "Welcome", "TellLookupResults"):
        return "AskForFurtherPreferences"
    elif state == "RequestPreferences":
        return "AskForFurtherPreferences"
    elif state == "AskForFurtherPreferences"\
            and additional_preferences["touristic"]\
            and additional_preferences["assigned seats"]\
            and additional_preferences["children"]\
            and additional_preferences["romantic"]:
        return "TellLookupResults"
    else:
        return state
