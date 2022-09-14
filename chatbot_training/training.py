#Rohit Mishra

import random
import json
import pickle
import time

import numpy as np
import pandas as pd

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD


#Begin
print("Model training beginning...")

for i in range(5):
    time.sleep(1)
    print("...")

#Initializes the lemmatizer based on Word Net
lemmatizer = WordNetLemmatizer()

#Loads the 
intents = json.loads(open('convo.json').read())

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

#Populates the respective words, classes, documents arrays with the relevant json pattern data
for intent in intents['intents']:
    
    for pattern in intent['patterns']:
    
        word_list = nltk.word_tokenize(pattern)
    
        words.extend(word_list)
    
        documents.append((word_list,intent['tag']))
    
        if intent['tag'] not in classes:
    
            classes.append(intent['tag'])



#Lemmatizes the individual words in the words list. Filters out ignored characters

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]


words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words,open('words.pkl', 'wb'))
pickle.dump(classes,open('classes.pkl', 'wb'))


train = []
output_empty = [0] * len(classes)

for document in documents:

    bag = []
    
    word_patterns = document[0]
    
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    
    #embeddings
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    train.append([bag, output_row])



random.shuffle(train)


train = np.array(train)

X_train,y_train = list(train[:, 0]), list(train[:, 1])


#Dense layer architecture
model = Sequential()

model.add(Dense(128, input_shape=(len(X_train[0]), ), activation = 'relu'))

#dropout probability adjusted
model.add(Dropout(0.5))

model.add(Dense(64, activation = 'relu'))

model.add(Dropout(0.6))

model.add(Dense(len(y_train[0]), activation= 'softmax'))

#Stochastic Gradient Descent
#learning rate set at 0.01 for higher accuracy
sgd = SGD(lr=0.01, decay=1e-6, momentum = 0.9, nesterov = True)


model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

hist = model.fit(np.array(X_train), np.array(y_train), epochs = 300, batch_size = 5, verbose = 1)

model.save('chatbotmodel.h5', hist)

print("Training Complete")