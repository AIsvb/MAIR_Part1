from joblib import load

def get_user_input():
    ''' Funtion that runs the program'''

    # Loading the saved vectorizer and random forest classifier
    rf_classifier = load("rf_classifier_no_dup.joblib")
    vectorizer = load("vectorizer_no_dup.joblib")

    # Printing welcome message
    print("HI! I am here to help you find the restaurant you're looking for. Ask me anything. If you are done talking enter 'quit' to stop the program")
    try:
        while True:
            user_input = input("Enter a sentence: ") # asking for user input
            if user_input == "quit": # when the user enters 'quit' the program ends
                quit()
            else:
                vectorized_sentence = vectorizer.transform([user_input]) # vectorizing the input
                label = rf_classifier.predict(vectorized_sentence) # predicting the class label of the input
                print(f"The sentence belongs to class: {label}")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Quitting")

if __name__ == "__main__":
    get_user_input()
