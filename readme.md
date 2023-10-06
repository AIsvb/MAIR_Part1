## Group data
Part 1b, by
Group 24:
Riccardo Campanella
Dirk Vet
Sander van Bennekom
Emma van Rossum
Pieter van der Werff

## Files
This folder includes the files:
- `program.py` initializes the chatbot
- `baseline1.py` classifies utterances based on the majority dialog act
- `baseline2.py` classifies the utterances based on keyword matching
- `DMS.py` implements the statemachine to control the dialog with the user
- `preferences.py` extracts preferenecs from user input for restaurant recommender
- `restaurantfinder.py` implements configurability features to the dialog manager. These four features are printing all in uppercase, use delay before system response, give formal or informal response from system, and output speech for system utterances
- `classifiers.py` trains an ML model to classify the dialog act from a user's utterance. The trained model is stored in a separate file
- `classifier.joblib` contains the trained classifier
- `vectorizer.joblib` contains a vectorizer objects that allows for a bag-of-words representation of user utterances
- `data\dialog_acts.dat` contains labeled user utterances. Used to train the dialog act classifier
- `data\restaurant_info.csv` is the database of restaurants available for the restaurant recommender (part 1b)
- `data\restaurant_info_additionalpref.csv` is the database of restaurants available for the restaurant recommender containing extra information for additional preferences (part 1c)

## How to use
For the complete implementation of the chatbot, `program.py` can be run in a terminal. An interactive dialog will be opened in which the user can interact with the restaurant recommender chatbot.

Each `.py` file can also be run independently, if one is only interested in a certain part of the code.

`classifiers.py` can be run in order to train the dialog act classifier by using either Support Vector Machine or Decision Forest techniques. However, a trained model is already stored in `classifier.joblib`. So, unless one is particularly interested in how the model is trained wants to change the ML technique used to train the classifier, there is no need to train the classifier again.

## Libraries
Pandas, os, numpy, scikit, nltk, collections, joblib, time, gtts, playsound, sklearn, Levenshtein, re