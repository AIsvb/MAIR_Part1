from joblib import load
import DialogManagementSystem

def get_user_input():
    ''' Function that runs the program'''

    # Loading the saved vectorizer and preferred classifier
    classifier = load("data/classifier.joblib")
    vectorizer = load("data/vectorizer.joblib")

    # Initializes the Finite State Machine that keeps track of the states and transitions
    # fsm = DialogManagementSystem()

    # Printing welcome message
    print("HI! I am here to help you find the restaurant you're looking for. Ask me anything. If you are done talking enter 'quit' to stop the program")
    dialogManager = DialogManagementSystem()
    try:
        while True:
            user_input = input("Enter a sentence: ") # asking for user input
            if user_input == "quit": # when the user enters 'quit' the program ends
                quit()
            else:
                act = classify_act(classifier, vectorizer, user_input) # classifying the dialog act
                if(act == 'inform'):
                    dialogManager.update_preferences()
                    if(dialogManager.food_not_provided()):
                        act = 'informFood'                      #User expresses preferences, but not food type 
                    elif(dialogManager.area_not_provided()):
                        act = 'informArea'                      #User expresses preferences, but not area 
                    elif(dialogManager.price_not_provided()):
                        act = 'informPrice'                     #User expresses preferences, but not price range 
                    else:
                        act = 'informAll'                       #User expresses preferences, and all are known 
                
                transition = dialogManager.transitionFunction[dialogManager.current_state.id][act]
                dialogManager.send(transition)

                print(f"The sentence belongs to class: {act}")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Quitting")

def classify_act(c, v, input):
    vectorized_sentence = v.transform([input])      # vectorizing the input
    return c.predict(vectorized_sentence)           # predicting the class label of the input

if __name__ == "__main__":
    get_user_input()
