from DMS import DMS
from joblib import load
import os

if __name__ == "__main__":
    if not os.path.exists("classifier.joblib"):
        os.system("python classifiers.py")

    classifier = load("classifier.joblib")
    vectorizer = load("vectorizer.joblib")
    dms = DMS(classifier, vectorizer, "data/restaurant_info.csv")
    while True and not dms.end_dialog:
        text = dms.system_utterance
        user_input = input(text)
        if user_input == "quit":
            quit()
        else:
            dms.transition(user_input)
            #dms.report()

    print(dms.system_utterance)


