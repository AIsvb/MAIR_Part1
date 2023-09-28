from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump


def validate_and_report(classifier, x_val, y_val):
    val_predictions = classifier.predict(x_val)

    accuracy = accuracy_score(y_val, val_predictions)
    report = classification_report(y_val, val_predictions, zero_division=0)

    print(f"Validation Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

    return accuracy, report


def train(classifier, x_train, y_train, clfr_dir):
    classifier.fit(x_train[:-1], y_train)
    dump(classifier, clfr_dir) # Save the classifier

    return classifier


def create_classifier(type = "rf" , n_estimators = 100, random_state = 42):
    if type == "rf":
        classifier = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    elif type == "svm":
        classifier = svm.SVC()
    else:
        return f"First argument must be either 'rf' or 'svm', but was {type}."

    return classifier


def vectorize(sen_train, sen_val, vect_dir):
    sen_train.append("UNKNOWN")  # this will add an element to the vectors which can handle unseen words

    # Vectorizing the sentences
    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(sen_train)
    x_val = vectorizer.transform(sen_val)
    dump(vectorizer, vect_dir)  # Save the vectorizer object and its parameter values

    return x_train, x_val


def get_train_val_data(data_dir, remove_duplicates = False, test_size = .15, random_state = 42):
    # Read the contents of the file
    with open(data_dir) as file:
        lines = file.readlines()

    # Remove duplicates if needed
    if remove_duplicates:
        lines = list(set(lines))

    # Obtain labels and sentences
    labels = [line.split()[0] for line in lines]
    sentences = [" ".join(line.split()[1:]) for line in lines]

    # Split the data in training and validation set
    sen_train, sen_val, lab_train, lab_val = train_test_split(sentences,
                                                              labels,
                                                              test_size=test_size,
                                                              random_state=random_state)

    return sen_train, sen_val, lab_train, lab_val


if __name__ == "__main__":
    # Setting adjustable parameters
    rm_duplicates = False
    DATA_DIR = "data/dialog_acts.dat"
    CLASSIFIER_DIR = "classifier.joblib"
    VECTORIZER_DIR = "vectorizer.joblib"
    mlAlgorithm = "rf"

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




