import csv

# for now define a user preference, later on this needs to be filled in by getting the info from the user
userpreference = ["expensive", "centre", "asian oriental"]

# function that finds all restaurant recommendations
def findrestaurants():
     restaurants = open('restaurant_info.csv', newline='')                                                     # open the file with all the restaurants 
     restaurantrecs = []                                                                                       # we want to save the restaurant recommendations, initialize it as empty list
     iterator = csv.reader(restaurants)                                                                        # csv.reader() is used to read the file, which returns an iterable reader object
     for currentrestaurant in iterator:                                                                        # loop through each line in the reader object
            if (currentrestaurant[1] == userpreference[0] and currentrestaurant[2] == userpreference[1] and currentrestaurant[3] == userpreference[2]):           # check if the user preferences match the pricerange, area, and type of a restaurant
                 restaurantrecs.append(currentrestaurant)                                                           # if that is the case we want to append the current restaurant to our recommendation list 
     return restaurantrecs                                                                                     # return the list of all possible restaurant options 

def clearuserpreference():
    userpreference = []

# for now set state manually to see if it works, we need to adjust this once the state transition function is complete so that they work together
# such that the state is rec1 when we first recommend a restaurant, after we gathered all the information and set the user preferences
# and the state is anohterrec when the dialog act is reqmore 
state = 'rec1'

currentrest = 0                                                                                                    # counter to keep track of which restaurant we are recommending, start at beginning of list so = 0
restaurantrec = findrestaurants()                                                                                  # store the list of restaurant recommendations in restaurantrec
# in the state transition function this needs to be done once all user information is known and filled in, so then we find the restaurants with the user preferences 
length = len(restaurantrec)                                                                                         # store the length of the list of restaurant recommendations

if state == 'rec1':
    # this state needs to be assigned in the state transition function once we have all our user preferences
    if length == 0:                                                                                                   # check that there are restaurants to recommend, 0 means list is empty
        print("We are sorry, we could not find a restaurant that matches your preferences, try changing some things.")  # case where there are no restaurants available
        clearuserpreference() 
    else:                                                                                      # clear user pref and go back to state that asks for info
        rec = restaurantrec[currentrest][0]                                                                        # sets the recommendation to the first restaurant name in the recommendation list 
        print(rec + " serves " + userpreference[2] + " food in the " + userpreference[0] + " price range.")        # recommend a restaurant   
if state == 'anotherrec':     
    # In the state transition function, in the case where the dialog act is reqmore, propose another restaurant, state needs to be set to 'anotherrec'     
    if currentrest + 1 < length:                                                                                     # check to see if there is anohter recommendation in the list    
        currentrest = currentrest + 1                                                                                # if that is the case, add 1 to the current rest so that we get the info from the next restaurant in the list   
        rec = restaurantrec[currentrest][0]                                                                          # get the name for the current recommendation   
        print(rec + " is another option that serves " + userpreference[2] + " food.")                                # give the recommendation to the user  
            # If user acknowledges this / confirms, we need to move to the state corresponding to that dialog act
            # If the user denies, requests more, we need to enter this state again
            # this depends on which dialog act the user gives us
    else:                                                                                                            # if there are no more options available   
        print("We are sorry, there are no more restaurant recommendations with these preferences available, please try changing some preferences.")        # inform the user of this and go back the to the inform state  
        restaurantrec = []                                                                                           # make the restaurant recommendations list empty again
        clearuserpreference()                                                                                        # clear user pref and go back to state that asks for info   

# function to get the address of the restaurant
def getaddr():
    address = restaurantrec[currentrest][5]
    print("The address is " + address)
    return address

# function to get the postcode of the restaurant
def getpostcode():
    postcode = restaurantrec[currentrest][6]
    print("The postcode is " + postcode)
    return postcode

# function to get the phone number of the restaurant
def getphone():
    phone = restaurantrec[currentrest][4]
    print("The phone number is " + phone)
    return phone

