# Rule-based Baseline Systems 
#
# The classifier looks at the words from the utterances that are not stopwords 
# (Nltk). It takes the class that has the highest frequency of a given word.
# The classifier scores around 0.85 accuracy on the test set.

import numpy as np
from collections import Counter, defaultdict

import nltk
from nltk.corpus import stopwords
 

PATH = "data\dialog_acts.dat"
TRAIN_PERC = 0.85


# Dictionary of most common words with their dialog act. If a word is in the 
# dictionary, the utterance is of that corresponding act. 
rules = {}
duplicates = []

def extract_data(path):
    """
    Extract the data from the given path.
    Return the set of possible dialog acts, lists of dialog act and utterance
    path: the path to the data file.
    """
    with open(path) as f:
        data = f.readlines()

        # Split once on a space.
        split_data = [s.split(' ', 1) for s in data]
        dialog_act = [sentence[0] for sentence in split_data]
        utterance = [sentence[1] for sentence in split_data]

    return set(dialog_act), np.array(dialog_act), np.array(utterance)


def total_act_word_counter(dialog_act, utterance):
    """
    return a Counter object of dialog_act and utterance pair occurences.
    dialog_act: the list of dialog acts of all utterances
    utterance: the list of corresponding utterances
    """
    act_utt_list = []

    for (act, sent) in zip(dialog_act, utterance):
        for u in sent.split():
            act_utt_list.append((act, u))

    count_act_utt = Counter(act_utt_list)
    return count_act_utt


def act_word_dict(total_count_act_utt):
    """
    Returns a dictionary of Counter objects of the word for a given act as
    dict[act][word]
    total_count_act_utt: Counter object with counts for all (act, word) pairs.
    """
    # Nested dictionary. count_dict[act][word] will give the occurences for the
    # given act and word
    count_dict = defaultdict(lambda: Counter())

    for ((act, word), cnt) in total_count_act_utt.items():
        # Inserts for the given act and word the corresponsing count.
        count_dict[act][word] += cnt

    return count_dict



# def get_duplicate_words(count_act_word):
#     """
#     count_act_word: Counter of all act and word pairs
#     """
#     global duplicates
#     words = [word for (_, word) in count_act_word.keys()]
#     # if the word is no longer in the set, is has been seen once before.
#     set_words = set(words)
#     #duplicates = []
#     dp = []

#     for word in words:
#         if word in set_words:
#             set_words.remove(word)
#         else:
#             dp.append(word)
#     duplicates = list(set(dp))

def create_rule(act_word_cnt_dict, act_set):
    """
    Create the keyword rules
    act_word_cnt_dict: dictionary of every act with their possible words and 
    corresponding counts.
    act_set: The set of possible dialog acts.
    """
    # Download the collection of stopwords from nltk.
    nltk.download('stopwords')
    
    for act in act_set:
        for (word, cnt) in act_word_cnt_dict[act].items():
            # Leave out any stopwords.
            if word not in stopwords.words('english'):
                if word in rules:
                    rules[word].append((act, cnt))
                else:
                    rules[word] = [(act, cnt)]

    
def train(act_set, dialog_act, utterance):
    """
    Get the keyword rules by using the train set
    act_set: The set of dialog acts seen in the training set
    dialog_act: The dialog acts from the training set
    utterance: The utterances from the training set.
    """
    
    # Counter object of all dialog act and word pairs. Counter[(act, word)]
    total_count_act_word = total_act_word_counter(dialog_act, utterance)
    #get_duplicate_words(total_count_act_word)
    
    # Dictionary of Counter objects for a given act and word. Dict[act][word]    
    act_word_cnt_dict = act_word_dict(total_count_act_word)

    create_rule(act_word_cnt_dict, act_set)


def predict(utt):
    """
    Predict the dialog act for the given utterance
    utt: the given utterance
    """
    predict_act = "NONE"
    possible_acts = []
    
    # For every word in the utterance
    for word in utt.split():
        if word in rules:                                
            possible_acts.extend(rules[word])
            # The word is in the dictionary, so it can be classified. 
            # End the forloop for this sentence.
            break

    if len(possible_acts) > 0:                        
        predict_act = max(possible_acts, key=lambda item: item[1])[0]

    return predict_act


if __name__ == '__main__':
    # Set of possible dialog acts, lists of dialog acts and utterances.
    act_set, dialog_act, utterance = extract_data(PATH)
    
    # Split the data set into a train set and test set.
    train_act = dialog_act[:int(TRAIN_PERC * len(dialog_act))]
    train_utt = utterance[:int(TRAIN_PERC * len(utterance))]
    train(act_set, train_act, train_utt)

    test_act = dialog_act[int(TRAIN_PERC * len(dialog_act)):]
    test_utt = utterance[int(TRAIN_PERC * len(utterance)):]

    # The list of predicted dialog acts
    predictions = []
    ratio_list = []
    for utt in test_utt:
        predict_act = "NONE"
        possible_acts = []
        
        # For every word in the utterance
        for word in utt.split():
            if word in rules:                                
                possible_acts.extend(rules[word])
                # The word is in the dictionary, so it can be classified. 
                # End the forloop for this sentence.
                break
        
        if len(possible_acts) > 0:                        
            predict_act = max(possible_acts, key=lambda item: item[1])[0]
                
        predictions.append(predict_act)

    # To print the accuracy of the predictions on the test set.
    print(sum([True for (ref_act, pred) in zip(test_act, predictions) if ref_act == pred]) / len(test_act))


    print("Enter sentence:")
    try:
        while True:
            utt = input() 
            if utt == "quit": 
                quit()
            else:                
                print(f"{predict(utt)} {utt}")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt. Quitting")
 
    
    
    

    

