from joblib import load
import pandas as pd
from classifiers import vectorizeUnknown

classifier = load("data/classifier.joblib")
vectorizer = load("data/vectorizer.joblib")

data = {"text": [], "dialog_act": []}

while True:
    user_input = input("type something")
    user_input = user_input.lower()
    if user_input == "quit":
        #df = pd.DataFrame(data)
        #df.to_excel("output.xlsx")
        quit()

    vect = vectorizer.transform([vectorizeUnknown(vectorizer, user_input)])
    dialog_act = classifier.predict(vect)

    data["text"].append(user_input)
    data["dialog_act"].append(dialog_act)

    print(f"Dialog act: {dialog_act}")
