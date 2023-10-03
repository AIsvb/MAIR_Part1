from DMS import DMS
from joblib import load
import os
from time import sleep
from gtts import gTTS
from playsound import playsound

speechOn = 0
upperOn = 0
sleepOn = 0 

delay = 2
language = 'en'

if __name__ == "__main__":
    if not os.path.exists("classifier.joblib"):
        os.system("python classifiers.py")

    classifier = load("classifier.joblib")
    vectorizer = load("vectorizer.joblib")
    dms = DMS(classifier, vectorizer, "data/restaurant_info_additionalpref.csv")
    while True and not dms.end_dialog:
        text = dms.system_utterance
        if (sleepOn == 1):
            sleep(delay)
        if (speechOn == 1):
            speech = gTTS(text=text, lang=language)
            speech.save("texttospeech.mp3")
            playsound("texttospeech.mp3")
        else:
            if (upperOn == 1):
                text = dms.system_utterance.upper()
                print(text)
            else:
                print(text)
        user_input = input()
        if user_input == "quit":
            quit()
        else:
            dms.transition(user_input)
            dms.report()

    print(dms.system_utterance)


