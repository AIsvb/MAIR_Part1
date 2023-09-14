from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump


def get_train_val_data(filename, remove_duplicates = False):
    # Read the contents of the file
    with open(filename) as file:
        lines = file.readlines()

    # Remove duplicates if needed
    if remove_duplicates:
        lines = list(set(lines))

    # Obtain labels and sentences
    labels = [line.split()[0] for line in lines]
    sentences = [" ".join(line.split()[1:]) for line in lines]

    # Split the data in training and validation set
    sentences_train, sentences_val, labels_train, labels_val = train_test_split(sentences, labels, test_size=0.2,
                                                                                random_state=42)

    return sentences_train, sentences_val, labels_train, labels_val


if __name__ == "__main__":
    # Setting adjustable parameters
    rm_duplicates = True
    CLASSIFIER_DIR = "rf_classifier.joblib"
    VECTORIZER_DIR = "vectorizer.joblib"

    # Preparing the training and validation data
    sentences_train, sentences_val, labels_train, labels_val = get_train_val_data("dialog_acts.dat", remove_duplicates=rm_duplicates)
    sentences_train.append("UNKNOWN") # this will add an element to the vectors which can handle unseen words

    # Vectorizing the sentences
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(sentences_train)
    X_val = vectorizer.transform(sentences_val)
    dump(vectorizer, VECTORIZER_DIR) # Save the vectorizer object and its parameter values

    # Initiating and training the RF classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train[:-1], labels_train)
    dump(rf_classifier, CLASSIFIER_DIR) # Save the classifier

    # Validation stage
    val_predictions = rf_classifier.predict(X_val)

    accuracy = accuracy_score(labels_val, val_predictions)
    report = classification_report(labels_val, val_predictions)

    print(f"Validation Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)