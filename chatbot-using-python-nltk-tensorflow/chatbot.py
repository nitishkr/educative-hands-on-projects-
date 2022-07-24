# code here
import json
import pickle
import random

import nltk
from nltk.stem import WordNetLemmatizer

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Dense, Activation, Dropout

# code here
with open(r'intents.json') as data:
    intents = json.loads(data.read())
	
words = []
classes = []
documents = []


for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        classes.append(intent['tag'])
        documents.append((w, intent['tag']))

lemmatizer = WordNetLemmatizer()
ignore_words = ['?', '!']
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))


pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


# code here
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) 
    for word in pattern_words]
    for w in words:
        if w in pattern_words:
            bag.append(1)
        else: bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])


random.shuffle(training)
training = np.array(training)
X_train = list(training[:, 0])
y_train = list(training[:, 1])

# code here
model = Sequential()
model.add(Dense(128, input_shape=(len(X_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

# code here
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

hist = model.fit(np.array(X_train),
                 np.array(y_train),
                 epochs=200,
                 batch_size=5,
                 verbose=1)

model.save('trained_model.h5', hist)