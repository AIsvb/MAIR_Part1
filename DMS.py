from preferences import extract_prefs
import pandas as pd


class DMS:

    def __init__(self, input_classifier, vectorizer, data_dir):
        self.classifier = input_classifier
        self.vectorizer = vectorizer
        self.data = pd.read_csv(data_dir)

        self.state = "Welcome"
        self.end_dialog = False
        self.system_utterance = "Hello, welcome to the restaurant recommendation system. " \
                                "You can ask for restaurants by area, price range or food type. How may I help you?"
        self.results = pd.DataFrame()
        self.current_suggestion = 0
        self.current_info = pd.Series()
        self.preferences = {"pricerange": "", "area": "", "food": ""}

    def transition(self, user_input):
        dialog_act = self.classify(user_input)
        match self.state:
            case "Welcome":
                match dialog_act:
                    case "thankyou" | "bye":
                        self.state = "Exit"
                    case "ack" | "affirm" | "confirm" | "deny" | "hello" | "negate" | "null" | "reqmore" | "request":
                        self.state = "RequestPreferences"
                    case "inform" | "reqalts":
                        self.update_preferences(user_input)
                        self.choose_and_set_state()
                    case "restart" | "repeat":
                        pass

            case "RequestPreferences":
                match dialog_act:
                    case "thankyou" | "bye":
                        self.state = "Exit"
                    case "restart":
                        self.state = "Welcome"
                        self.set_initial_values()
                    case "inform" | "reqalts":
                        self.update_preferences(user_input)
                        self.choose_and_set_state()
                    case "ack" | "affirm" | "confirm" | "deny" | "hello" | "negate" | "null" | "repeat" | "reqmore" | "request":
                        pass

            case "AskFoodType":
                match dialog_act:
                    case "thankyou" | "bye":
                        self.state = "Exit"
                    case "restart":
                        self.state = "Welcome"
                        self.set_initial_values()
                    case "inform" | "reqalts":
                        self.update_preferences(user_input)
                        self.choose_and_set_state()
                    case "ack" | "affirm" | "confirm" | "deny" | "hello" | "negate" | "null" | "repeat" | "reqmore" | "request":
                        pass

            case "AskArea":
                match dialog_act:
                    case "thankyou" | "bye":
                        self.state = "Exit"
                    case "restart":
                        self.state = "Welcome"
                        self.set_initial_values()
                    case "inform" | "reqalts":
                        self.update_preferences(user_input)
                        self.choose_and_set_state()
                    case "ack" | "affirm" | "confirm" | "deny" | "hello" | "negate" | "null" | "repeat" | "reqmore" | "request":
                        pass

            case "AskPriceRange":
                match dialog_act:
                    case "thankyou" | "bye":
                        self.state = "Exit"
                    case "restart":
                        self.state = "Welcome"
                        self.set_initial_values()
                    case "inform" | "reqalts":
                        self.update_preferences(user_input)
                        self.choose_and_set_state()
                    case "ack" | "affirm" | "confirm" | "deny" | "hello" | "negate" | "null" | "repeat" | "reqmore" | "request":
                        pass

            case "TellLookupResults":
                if len(self.results) > 0:
                    match dialog_act:
                        case "thankyou" | "bye":
                            self.state = "Exit"
                        case "restart":
                            self.state = "Welcome"
                            self.set_initial_values()
                        case "ack" | "affirm" | "request":
                            self.retrieve_restaurant_info()
                            self.state = "OfferFurtherInformation"
                        case "deny":
                            self.state = "RequestPreferences"
                        case "inform" | "reqalts":
                            self.update_preferences(user_input)
                            self.results = self.lookup()
                            self.state = "TellLookupResults"
                        case "reqmore":
                            self.choose_and_set_state(reqmore=True)
                        case "confirm" | "hello" | "negate" | "null" | "repeat":
                            return
                else:
                    match dialog_act:
                        case "thankyou" | "bye":
                            self.state = "Exit"
                        case "restart":
                            self.state = "Welcome"
                            self.set_initial_values()
                        case "ack" | "affirm" | "deny":
                            self.state = "RequestPreferences"
                        case "inform" | "reqalts":
                            self.update_preferences(user_input)
                            self.results = self.lookup()
                            self.state = "TellLookupResults"
                        case "confirm" | "hello" | "negate" | "null" | "repeat" | "reqmore" | "request":
                            return

            case "OfferFurtherInformation":
                match dialog_act:
                    case "thankyou" | "bye":
                        self.state = "Exit"
                    case "restart":
                        self.state = "Welcome"
                        self.set_initial_values()
                    case "inform" | "reqalts":
                        self.update_preferences(user_input)
                        self.results = self.lookup()
                        self.state = "TellLookupResults"
                    case "deny":
                        self.state = "RequestPreferences"
                    case "confirm":
                        self.state = "TellLookupResults"
                    case "reqmore":
                        self.choose_and_set_state(reqmore=True)
                    case "ack" | "affirm" | "hello" | "negate" | "null" | "repeat" | "request":
                        pass

            case "AskForAcceptance":
                match dialog_act:
                    case "thankyou" | "bye" | "ack" | "affirm":
                        self.state = "Exit"
                    case "restart":
                        self.state = "Welcome"
                        self.set_initial_values()
                    case "confirm":
                        self.state = "TellLookupResults"
                    case "deny":
                        self.state = "RequestPreferences"
                    case "inform" | "reqalts":
                        self.update_preferences(user_input)
                        self.results = self.lookup()
                        self.state = "TellLookupResults"
                    case "hello" | "negate" | "null" | "repeat" | "reqmore" | "request":
                        pass

        self.update_utterance()
        return

    def classify(self, user_input):
        vectorized_sentence = self.vectorizer.transform([user_input])
        return self.classifier.predict(vectorized_sentence)

    def lookup(self):
        results = self.data.copy()
        masks = [results[column] == value for column, value in self.preferences.items()]
        combined_mask = pd.concat(masks, axis=1).all(axis=1)

        return results[combined_mask]

    def update_preferences(self, user_input):
        foodType, area, priceRange = extract_prefs(user_input)
        if foodType != "":
            self.preferences["food"] = foodType
        if area != "":
            self.preferences["area"] = area
        if priceRange != "":
            self.preferences["pricerange"] = priceRange

    def update_utterance(self):
        match self.state:
            case "Welcome":
                self.system_utterance = "Hello, welcome to the restaurant recommendation system. " \
                                        "You can ask for restaurants by area, price range or food type. " \
                                        "How may I help you?"
            case "RequestPreferences":
                self.system_utterance = "Please tell me your preferences for area, price range and food type."
            case "AskFoodType":
                self.system_utterance = "What kind of food do you prefer?"
            case "AskArea":
                self.system_utterance = "In what part of town would you like the restaurant to be?"
            case "AskPriceRange":
                self.system_utterance = "What prices are you looking for?"
            case "TellLookupResults":
                if len(self.results) > 0:
                    name = self.results.iloc[self.current_suggestion].restaurantname
                    food = self.results.iloc[self.current_suggestion].food
                    area = self.results.iloc[self.current_suggestion].area
                    pricerange = self.results.iloc[self.current_suggestion].pricerange
                    utterance = f"{name} is a restaurant which"
                    if not pd.isna(food):
                        utterance += f" serves {food} food"
                    if not pd.isna(pricerange):
                        utterance += f" has {pricerange} prices"
                    if not pd.isna(area):
                        utterance += f" and is in the {area} of town"
                    utterance += ". This is all known information about food type, price range and area."
                    self.system_utterance = utterance
                else:
                    self.system_utterance = "Sorry, but there is no restaurant that meets your preferences. " \
                                            "Could you please alter your preferences?"
            case "OfferFurtherInformation":
                utterance = "The following information about the restaurant is known:\n"
                for cat, val in self.current_info.items():
                    utterance += f"{cat}: {val}\n"
                utterance += "How can I help you further?"
                self.system_utterance = utterance
            case "AskForAcceptance":
                self.system_utterance = "Sorry, there are no alternatives. Do you accept the current suggestion?"
            case "Exit":
                self.system_utterance = "Okay,thank you for making use of this DMS. Have a nice day!"
                self.end_dialog = True

    def choose_and_set_state(self, reqmore = False):
        if self.preferences["food"] == "":
            self.state = "AskFoodType"
        elif self.preferences["area"] == "":
            self.state = "AskArea"
        elif self.preferences["pricerange"] == "":
            self.state = "AskPriceRange"
        elif reqmore:
            if len(self.results) - (self.current_suggestion + 1) > 0:
                self.current_suggestion += 1
                self.state = "TellLookupResults"
            else:
                self.state = "AskForAcceptance"
        else:
            self.results = self.lookup()
            self.state = "TellLookupResults"

    def set_initial_values(self):
        self.results = pd.DataFrame()
        self.current_suggestion = 0
        self.preferences = {"pricerange": "", "area": "", "food": ""}

    def retrieve_restaurant_info(self):
        info = self.results.iloc[self.current_suggestion][["phone", "addr", "postcode"]]
        for cat, val in info.items():
            if pd.isna(val):
                info[cat] = "unknown"

        self.current_info = info

    def report(self):
        print(self.state)
        print(self.preferences)


