# This file starts the restaurant recommendation system. It loads the 
# classifier and implements 3 of 4 configurability features: text-to-speech
# output, return uppercase output, and delay system output. The remaining 
# configurability feature is implemented in DMS.py

from DMS import DMS
from joblib import load
import os
from time import sleep
from gtts import gTTS
from playsound import playsound

# Configurabiltiy features: text-to-speech, return upper case output, and 
# delay system's output.
speechOn = 0
upperOn = 0
sleepOn = 0 
# Time delay for configurability feature
delay = 2
language = 'en'

if __name__ == "__main__":
    if not os.path.exists("classifier.joblib"):
        os.system("python classifiers.py")

    # Load the pretrained classifier and vectorizer
    classifier = load("classifier.joblib")
    vectorizer = load("vectorizer.joblib")
    # Create the dialog management system, a state machine to control the
    # conversation.
    dms = DMS(classifier, vectorizer, "data/restaurant_info_additionalpref.csv")
    while True and not dms.end_dialog:
        text = dms.system_utterance
        # system delay feature
        if (sleepOn == 1):
            sleep(delay)
        # Text to speech feature
        if (speechOn == 1):
            speech = gTTS(text=text, lang=language)
            speech.save("texttospeech.mp3")
            playsound("texttospeech.mp3")
        else:
            # Return uppercase output feature
            if (upperOn == 1):
                text = dms.system_utterance.upper()
                print(text)
            else:
                print(text)
        user_input = input()
        if user_input == "quit":
            quit()
        else:
            # Make a transition in the dialog manager system to continue
            # the conversation.
            dms.transition(user_input)

    print(dms.system_utterance)


