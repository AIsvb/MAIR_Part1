import time
from utils import *
import pandas as pd
from joblib import load
from classifiers import vectorizeUnknown

intro_text = "PLEASE READ THE INFORMATION BELOW\n\nThank you in advance for using this chatbot. Below are a couple of instructions that will help you understand what the chatbot is capable of:\n" \
             "  a. The chatbot will start by asking for your restaurant preferences. You can mention three types of preferences, namely food type, price range and area.\n" \
             "  b. For price range, the chatbot can only distinguish between cheap, moderate, and expensive.\n" \
             "  c. For area, the chatbot can only distinguish between north, east, south, west, and centre.\n" \
             "  d. When the chatbot asks for additional preferences, you can tell 4 additional preferences:\n" \
             "      - Whether or not you want to bring children. If so, mention 'children' in your response;\n" \
             "      - Whether or not you want assigned seats. If so, mention 'assigned seats' in your response;\n" \
             "      - Whether or not you want a touristic restaurant. If so, mention 'touristic' in your response;\n" \
             "      - Whether or not you want a romantic restaurant. If so, mention 'romantic' in your reponse.\n" \
             "  e. When the chatbot suggests a restaurant, you can asks for a phone number, post code, and address if you would like to have this information.\n" \
             "  f. You can ask the chatbot for alternatives if the suggestion it makes, does not appeal to you. Use the word 'more' in your response.\n" \
             "  g. It is possible that the chatbot repeats itself, or that you end up stuck in a loop of chatbot responses. In both cases, try using different phrasing of your responses.\n" \
             "  h. You can restart you conversation with the chatbot by saying something like 'start over'.\n" \
             "  i. If you want to quit completely, enter'quit' followed by the 'enter' key.\n\n" \
             "======================================================================\n" \
             "Assignment: You are looking for a romantic restaurant in the north of town, where they serve indian food for moderate prices. " \
             "Have a chat with the chatbot to find such\na restaurant and the corresponding address. " \
             "You are free to ask for alternatives if these exist.\n" \
             "======================================================================\n\n" \
             "You are asked to do the assignment twice, each time with a different version of the chatbot. You will start with version A. " \
             "Upon finishing, the\ntext 'TRANSITIONING TO THE NEXT VERSION' will appear on the screen. " \
             "The chatbot will than transition to version B and start the conversation again.\nJust repeat the assignment as described above. " \
             "When having finished your second conversation, the program will shut down.\n"

print(intro_text)
time.sleep(3)
print("VERSION A\n")
def classify(vectorizer, classifier, user_input):
    user_input = vectorizeUnknown(vectorizer, user_input)

    vectorized_sentence =vectorizer.transform([user_input])
    return classifier.predict(vectorized_sentence)

DIR = "data/restaurant_info_additionalpref.csv"
data = pd.read_csv(DIR)
classifier = load("data/classifier.joblib")
vectorizer = load("data/vectorizer.joblib")

state_info = {"current_state": "Welcome", "end_conversation": False, "formalOn": 0}
while True and not state_info["end_conversation"]:
    state_info, user_input = act(data, state_info)
    dialog_act = classify(vectorizer, classifier, user_input)
    state_info = transition(state_info, dialog_act)

time.sleep(1)
print("\nTRANSITIONING TO THE NEXT VERSION (VERSION B)\n")
time.sleep(2)

state_info = {"current_state": "Welcome", "end_conversation": False, "formalOn": 1}
while True and not state_info["end_conversation"]:
    state_info, user_input = act(data, state_info)
    dialog_act = classify(vectorizer, classifier, user_input)
    state_info = transition(state_info, dialog_act)

print("Thank you again for taking part in this research. You are now asked to fill out a questionnaire. Have a nice day!")
time.sleep(5)