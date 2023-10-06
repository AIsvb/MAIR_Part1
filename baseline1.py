# This file implements a Rule-based Baseline Systems for classifying dialogue acts.
# The system always returns the majority class in the given data.

import pandas as pd

# Read the data into a dataframe and split the data into a training set (85%) and a test set (15%) 
df = pd.read_fwf('data\dialog_acts.dat', colspecs='infer', header=None)
df.insert(0,'dialog_act', 0)                                        # create a column called 'dialog_act' and set all values to 0
trainingdata = df.iloc[:21676]                                      # 85% of the data 
testdata = df.iloc[-3326:]                                          # 15% of the data

# Define the dialog_acts as strings. We compare them later in the for-loop to the first word of each line in the dataframe
dialog_array = ['ack', 'affirm', 'bye', 'confirm', 'deny', 'hello', 'inform', 'negate', 'null', 'rpeat', 'reqalts', 'reqmore', 'request', 'restart', 'thankyou']

# Define the 15 dialog act counts so we can keep track of which one occurs the most
dialog_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# Check which dialog act occurs the most in the training data                                 
for index, row in trainingdata.iterrows():                          # iterate over the trainingdata           
    first_word = row[0].split()                                     # row[0] is the current line that we are at in the dataframe, split makes it so that we can get the first word (dialog_act)
    dialog_act = first_word[0]                                      # define the dialog act as the first word of the current line
    for n in range(15):                                             # values 0 to 14, so we loop over the whole array
        if dialog_act == dialog_array[n]:                           # if the dialog_act of the current line == to the corresponding dialog act in the array
            trainingdata.at[index, 'dialog_act'] = dialog_array[n]  # we insert that dialog act string value into the new column 'dialog_act', so we have the dialog acts in a separate column
            dialog_counts[n]+=1                                     # increment the dialog_act count of the corresponding dialog act  

# Determine which dialog_act is the majority label
iterate = 0                                         # initialize the iterater to 0
majority_label = dialog_array[0]                    # set the majority_label at the beginning of the loop as a default to the first entry of dialog_array ('ack')
for n in range(15):                                 # loop for n values 0 to 14
    if dialog_counts[n] > iterate:                  # check if the value of count at n is bigger than the current value of the iterater
        iterate = dialog_counts[n]                  # if that is the case, set the iterate to that value, so we can compare it to other values
        majority_label = dialog_array[n]            # set the majority_label to the corresponding value in the dialog_array at value n (because that count is the largest thus far)                                      # now we have counted and set the majority label to the dialog act that has occured the most, in this case inform

# baseline function1 that takes in the user input and always assigns it the majority label as the dialog act
def userinput():
    file = open("userinput.txt", "a")                                       # open a file to write user input to
    print("Hi there! Please answer the prompt and type 'exit' to leave.")   # Ask the user for input and tell them how to leave    
    while True:
            user_input = input("Enter your input: ")                        # save the user input in a variable
            if user_input == "exit":                                        # if the input was exit, exit the while loop    
                break                                                                                      
            file.write(user_input)                                          # write the user_input to the file    
            file.write("\n")                                                # write a new line to the file
            print("Predicted class of your input:", majority_label)
    file.close()                                                            # close the file
    df_userinput = pd.read_fwf('userinput.txt', header=None)                # read the textfile with the user input into a dataframe
    df_userinput.insert(0,'dialog_act', majority_label)                     # create a column called dialog_act in the dataframe and give it the value of the majority label
    return df_userinput                                                     # return the dataframe of the userinput with the assigned dialog_act 

userinput()                                                                 # call the function to start asking the user for data