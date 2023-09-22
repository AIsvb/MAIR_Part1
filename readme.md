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
- `main.py` initializes the chatbot
- `DialogManagementSystem.py` 
- `preferences.py` 
- `restaurantfinder.py`
- `classifiers.py` trains an ML model to classify the dialog act from a user's utterance. The trained model is stored in a separate file
- `classifier.joblib` contains the trained classifier
- `vectorizer.joblib` contains a vectorizer objects that allows for a bag-of-words representation of user utterances
- `data\dialog_acts.dat` contains labeled user utterances. Used to train the dialog act classifier
- `data\restaurant_info.csv` is the database of restaurants available for the restaurant recommender

## How to use
For the most complete implementation of the chatbot, `main.py` can be run in a terminal. An interactive dialog will be opened in which the user can interact with the restaurant recommender chatbot.

Each `.py` file can also be run independently, if one is only interested in a certain part of the code.

`classifiers.py` can be run in order to train the dialog act classifier by using either Support Vector Machine or Decision Forest techniques. However, a trained model is already stored in `classifier.joblib`. So, unless one is particularly interested in how the model is trained wants to change the ML technique used to train the classifier, there is no need to train the classifier again.