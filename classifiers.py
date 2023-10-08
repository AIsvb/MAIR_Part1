# This file creates a classifier and a vectorizer. The classifier is then 
# validated and its accuracy is being reported.
# The possible classifiers to be learned are random forest or support vector
# machine.

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump
# import statistics


def validate_and_report(classifier, x_val, y_val):
    """
    Validate the accuracy and report the accuracy of the classifier.
    classifier: The classifier being used.
    x_val: input values used for prediction
    y_val: labeled output values
    """
    val_predictions = classifier.predict(x_val)

    # Compare the predictions to the real labeled output values and calculate 
    # the accuracy.
    accuracy = accuracy_score(y_val, val_predictions)
    report = classification_report(y_val, val_predictions, zero_division=0)

    print(f"Validation Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

    return accuracy, report


def train(classifier, x_train, y_train, clfr_dir):
    """
    Train the model
    classifier: the classifier
    x_train: the input to predict on 
    y_train: the correctly labeled output
    clfr_dir: the path to the classifier file.
    """
    classifier.fit(x_train[:-1], y_train)
    dump(classifier, clfr_dir) # Save the classifier

    return classifier


def create_classifier(type = "rf" , n_estimators = 100, random_state = 42):
    """
    Create a Random Forest classifier or support vector machine classifier.
    type: type of classifier
    n_estimators: amount of trees in random forest algorithm
    random_state: random state to control randomness of the bootstrapping in 
    random forest algorithm
    """
    if type == "rf":
        classifier = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    elif type == "svm":
        classifier = svm.SVC()
    else:
        return f"First argument must be either 'rf' or 'svm', but was {type}."

    return classifier


def vectorize(sen_train, sen_val, vect_dir):
    """
    Vectorize the data
    sen_train: training set of sentences
    sen_val: validation set of sentences
    vect_dir: path to the vectorizer
    """
    sen_train.append("UNKNOWN")  # this will add an element to the vectors which can handle unseen words

    # Vectorizing the sentences
    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(sen_train)
    
    #sen_val = [vectorizeUnknown(vectorizer, sentence) for sentence in sen_val]
    x_val = vectorizer.transform(sen_val) 
   
    
    
    
    # Dirk: shows index of each word in the vector
    print(vectorizer.vocabulary_)
    # Pieter: the index of the "unknown" label
    unknownIndex = next(i for i, word in enumerate(vectorizer.get_feature_names_out()) if word == "unknown")
    print("idx= ", unknownIndex)
    print("Pieter - out-of-vocabulary words: " + str(x_val.toarray()[unknownIndex].sum(axis = 0))) # Pieter
    print("Dirk - out-of-vocabulary words: " + str(x_val.toarray().sum(axis = 0)[unknownIndex])) # Dirk https://stackoverflow.com/questions/27488446/how-do-i-get-word-frequency-in-a-corpus-using-scikit-learn-countvectorizer
    dump(vectorizer, vect_dir)  # Save the vectorizer object and its parameter values

    return x_train, x_val


def get_train_val_data(data_dir, remove_duplicates = False, test_size = .15, random_state = 42):
    """
    Get the training and validation set by splitting the data
    data_dir: data file
    remove_duplicates: boolean, remove duplicates yer or no
    test_size: fraction of the data being used for the test set.
    random_state: random state for random forest algorithm 
    """
    # Read the contents of the file
    with open(data_dir) as file:
        lines = file.readlines()

    # Remove duplicates if needed
    if remove_duplicates:
        lines = list(set(lines))

    # Obtain labels and sentences
    labels = [line.split()[0] for line in lines]
    sentences = [" ".join(line.split()[1:]) for line in lines]

    # # Extra lines of code to print the label distribution of the utterances
    # cv = CountVectorizer()
    # labelCount = cv.fit_transform(labels)
    # print(cv.get_feature_names_out())
    # print(labelCount.toarray().sum(axis=0))

    # # Extra lines of code to print statistics for the utterance length of the labeled data
    # print("The mean utterance length is " + str(statistics.mean([len(line.split()) for line in sentences])) + " words")
    # print("The median utterance length is " + str(statistics.median([len(line.split()) for line in sentences])) + " words")
    # print("The mode utterance length is " + str(statistics.mode([len(line.split()) for line in sentences])) + " word")

    # Split the data in training and validation set
    sen_train, sen_val, lab_train, lab_val = train_test_split(sentences,
                                                              labels,
                                                              test_size=test_size,
                                                              random_state=random_state)

    return sen_train, sen_val, lab_train, lab_val

def vectorizeUnknown(vectorizer, sentence):
    words = sentence.split(" ")
    for i, word in enumerate(words):
        if word not in vectorizer.get_feature_names_out():
            words[i] = "UNKNOWN"
    return " ".join(words)

if __name__ == "__main__":
    # Setting adjustable parameters
    rm_duplicates = True
    DATA_DIR = "data/dialog_acts.dat"
    CLASSIFIER_DIR = "classifier.joblib"
    VECTORIZER_DIR = "vectorizer.joblib"
    mlAlgorithm = "svm"

    # Collect training and validation data
    sen_train, sen_val, lab_train, lab_val = get_train_val_data(DATA_DIR,
                                                                remove_duplicates=rm_duplicates,
                                                                test_size=.15,
                                                                random_state=42)

    # Vectorize the sentences
    x_train, x_val = vectorize(sen_train, sen_val, VECTORIZER_DIR)

    # Create a classifier object
    model = create_classifier(mlAlgorithm, n_estimators=100, random_state=42)

    # Train the classifier
    trained_model = train(model, x_train, lab_train, CLASSIFIER_DIR)

    # Validate the classifier and report its accuracy
    accuracy, report = validate_and_report(trained_model, x_val, lab_val)




