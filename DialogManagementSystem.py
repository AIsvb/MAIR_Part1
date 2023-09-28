from enum import Enum, unique
from statemachine import StateMachine, State
from statemachine.states import States
# from preferences import extract_prefs
# from restaurantfinder import restaurantrec

@unique
class DialogStates(Enum):
    # Numerating as we encounter but te ordering is not relevant.
    welcome = 1
    ask_foodtype = 2
    ask_area = 3 
    ask_pricerange = 4
    lookup_restaurant_suggestion = 5
    offer_suggestion = 6
    retrieve_address = 7
    retrieve_phonenumber = 8
    retrieve_postcode = 9
    return_information = 10 
    ask_newpreferences = 11 
    system_exit = 12 # Adding an end state supposing the dialog system terminates once the user get a reccomendation

class DialogManagementSystem(StateMachine):
    """ 
    Using a Finite State Machine to create a rule-based dialog system.
    The main components of the machine are States, Transitions, Events and Actions.
    A state is the representation of system's current condition or behaviour and 
    its transition to another State is triggered by an Event with the Action as side-effect.
    """

    # STATES
    _ = States.from_enum(DialogStates, initial=1, final=12)
    
    def __init__(self):
        # BUSINESS LOGIC
        self.user_input = ""
        self.preferences = ["south", "expensive", "chinese"] # should be: extract_prefs(user_input) 
        super(DialogManagementSystem,self).__init__()

    # TRANSITIONS
    # Listed all the transitions. Each group of transitions is starting from a different state.
    # A transition is "passing by" a dialog act. E.g. welcome_to_foodtype is passing by the inform (User expresses preferences)

    # Welcome-transitions (all transitions originated from Welcome State)
    welcome_to_foodtype = _.welcome.to(_.ask_foodtype, cond="food_not_provided")
    welcome_to_area = _.welcome.to(_.ask_area, cond="area_not_provided")
    welcome_to_pricerange = _.welcome.to(_.ask_pricerange, cond="price_not_provided")
    welcome_to_lookup = _.welcome.to(_.lookup_restaurant_suggestion, cond="preferences_provided")

    # Foodtype-transitions
    foodtype_to_area = _.ask_foodtype.to(_.ask_area, cond="area_not_provided")
    foodtype_to_pricerange = _.ask_foodtype.to(_.ask_pricerange, cond="price_not_provided")
    foodtype_to_lookup = _.ask_foodtype.to(_.lookup_restaurant_suggestion, cond="preferences_provided")

    # Area-transitions
    area_to_pricerange = _.ask_area.to(_.ask_pricerange, cond="price_not_provided")
    area_to_lookup = _.ask_area.to(_.lookup_restaurant_suggestion, cond="preferences_provided")

    # Pricerange-transitions
    pricerange_to_lookup = _.ask_pricerange.to(_.lookup_restaurant_suggestion, cond="preferences_provided") 

    # Offer-transitions
    offer_to_address = _.offer_suggestion.to(_.retrieve_address, cond="address_requested")
    offer_to_phone = _.offer_suggestion.to(_.retrieve_phonenumber, cond="phone_requested")
    offer_to_postcode = _.offer_suggestion.to(_.retrieve_postcode, cond="postcode_requested")
    offert_to_returninfo = _.offer_suggestion.to(_.return_information, cond="no_requests")

    address_to_phone = _.retrieve_address.to(_.retrieve_phone, cond="phone_requested")
    address_to_postcode = _.retrieve_address.to(_.retrieve_postcode, cond="postcode_requested")
    address_to_returninfo =_.retrieve_address.to(_.return_information, cond="address_request_only")
    phone_to_postcode = _.retrieve_phone.to(_.retrieve_postcode, cond="postcode_requested")
    postcode_to_returninfo = _.retrieve_postcode.to(_.return_information, cond="postcode_requested")

    # Lookup-transitions
    lookup_to_offer = _.lookup_restaurant_suggestion.to(_.offer_suggestion, cond="suggestion_found")
    lookup_to_new_preferences = _.lookup_restaurant_suggestion.to(_.ask_newpreferences, cond="suggestion_not_found")

    returninfo_to_exit = _.return_information.to(_.system_exit, cond="information_returned")    
    offer_to_exit = _.offer_suggestion.to(_.system_exit, cond="offer_accepted")

    # ACTIONS
    # Defining the decisional paths 
    start_dialog = welcome_to_foodtype | foodtype_to_area | area_to_pricerange | pricerange_to_lookup
    end_no_suggestion = lookup_to_new_preferences
    end_straight_dialog = offer_to_exit
    end_request_dialog = offer_to_address | address_to_phone | phone_to_postcode | postcode_to_returninfo | returninfo_to_exit

    

    # 1) Defining the "Guards" function. We use it to validate the transitions conditions
    def food_not_provided(self):
        return self.preferences[2] == ""

    def area_not_provided(self):
        return self.preferences[0] == ""
    
    def price_not_provided(self):
        return self.preferences[1] == ""
    
    def preferences_provided(self):
        return not any(pref == "" for pref in self.preferences)
    
    def address_requested():
        #checking current state and user utterance
        return self.current_state.id == _.offer_suggestion \
                    and act(self.user_input) == "request" \
                        and "address" in self.user_input
    
    def phone_requested():
        return self.current_state.id in {_.offer_suggestion, _.retrieve_address} \
                    and act(self.user_input) == "request" \
                        and "phone" in self.user_input

    def postcode_requested():
        return self.current_state.id in {_.offer_suggestion, _.retrieve_address, _.retrieve_phone} \
                    and act(self.user_input) == "request" \
                        and "postcode" in self.user_input

    def no_requests():
        return self.current_state.id == _.offer_suggestion \
                    and act(self.user_input) == "affirm" \
                        and "yes" in self.user_input
    
    def address_requested_only():
        return self.current_state.id == _.retrieve_address \
                    and act(self.user_input) == "thankyou" \
                        and "thank you" or "goodbye" in self.user_input

    # 2) Defining other actions
        """
            Missing custom-functions applied befor/after and when entering/exiting each state
        """ 

    # 3) External functions
        """
            Functions that use the user input to alter the state of the FSM
        """
    
    def update_input(self, input):
        self.user_input = input
    
    def update_preferences(self):
        update_food, update_area, update_price = extract_prefs(self.user_input)
        if update_food != "":
            self.food = update_food
        if update_area != "":
            self.area = update_area
        if update_price != "":
            self.price = update_price  

    def classify_act():
        #placeholder for the main.py classify_act() function
        return "inform"

    if __name__  == "__main__":
        #EVENT
        dms = StateMachine.DialogManagementSystem()
        # check(dms)
        dms.send(start_dialog)
        # dms.send(end_no_suggestion)
        # dms.send(end_straight_dialog)
        # dms.send(end_request_dialog)
        # dms._graph().write_png("docs/images/test_dialog_management_system.png") # we can use this function to plot what's the diagram thas has been executed.
        # dms.calls.clear()
        # machine.current_state.id

