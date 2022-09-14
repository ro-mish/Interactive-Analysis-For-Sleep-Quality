#Rohit Mishra
## GameTime Chatbot

import random
import json
import pickle
import time 

import pandas as pd
import numpy as np

import nltk 
from nltk.stem import WordNetLemmatizer

from keras.models import load_model
import tensorboard

#import NBATest
#import Weather


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('chatbot_training/convo.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbotmodel.h5')

sleep_model = pickle.load(open('sleepEngine/sleep_model.sav', 'rb'))



def clean_up_sentence(sentence):
    
    sentence_words = nltk.word_tokenize(sentence)
    
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    
    return sentence_words

def bag_of_words(sentence):
    
    sentence_words = clean_up_sentence(sentence)
    
    bag = [0]*len(words)
    
    for w in sentence_words:

        for i, word in enumerate(words):
        
            if word == w:
        
                bag[i] = 1
    
    return np.array(bag)

def predict_class(sentence):
    
    bow = bag_of_words(sentence)
    
    res = model.predict(np.array([bow]))[0]
    
    ERROR_THRESHOLD = 0.2
    
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x: x[0], reverse=True)

    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list,intents_json):
    
    tag = intents_list[0]['intent']
    
    list_of_intents = intents_json['intents']
    
    for i in list_of_intents:
    
        if i['tag'] == tag:
    
            result = random.choice(i['responses'])
    
            break
    
    return result

def nba_retrieve(message):
    player_list = NBATest.get_team_players(message)    
    return player_list

def weather_retrieve(location):
    weather_dict = Weather.get_temp(location)
    return dict(weather_dict)




print("Sleep Bot woke up")

file1 = open('img_robot.txt', 'r')
Lines = file1.readlines()


for line in Lines:
    print(line)

check = True

while check:

    
    message = input("[Type here]: ")
    
    if message.lower() in ("done", "bye","end","complete","terminate"):
        
        check = False

    if "sleep" in message.lower():

        print("You can understand how you sleep with a few factors")
        
        
        X = {"Enough":0.0,	
            "PhoneReach":0.0,	
            "PhoneTime":0.0,	
            "Tired":0.0,	
            "Breakfast":0.0}
        
        enough = input("Do you get enough rest? [y/n]: ")
        phone = input("Is your phone within reach? [y/n]: ")
        phoneTime = input("Do you spend time on your phone before sleeping? [y/n]: ")
        tired = input("On a scale of 1-5, how tired are you?: ")
        breakfast = input("Do you eat breakfast? [y/n]: ")

        if not(type(enough) == str and (enough == "y" or enough == "n")):
            print("Please respond with only y or n please!")
        if not(type(phone) == str and (phone == "y" or phone == "n")):
            print("Please respond with only y or n please!")
        if not(type(phoneTime) == str and (phoneTime == "y" or phoneTime == "n")):
            print("Please respond with only y or n please!")
        if not(type(tired) == int and (tired > 5 or tired < 1)):
            print("Please respond with only a number between 1 and 5 please!")
        if not(type(breakfast) == str and (breakfast == "y" or breakfast == "n")):
            print("Please respond with only y or n please!")

        if enough == "y":
            X['Enough'] = 1.0
        if phone == "y":
            X["PhoneReach"] = 1.0
        if phoneTime == "y":
            X["PhoneTime"] = 1.0

        X['Tired'] = float(tired)

        if breakfast == "y":
            X["Breakfast"] = 1.0

        

        
        out = sleep_model.predict([pd.Series(X)])[0]

        print(f"Your predicted number of hours of sleep is: {out}")
        continue


    # if "nba" in message.lower():

    #     print("Enter a team name to see all the players")
    #     team = input()
    #     m = nba_retrieve(str(team))
    #     [print(i) for i in m]
    #     continue
    

    # if "weather" in message.lower():
        
    #     print("Enter a location in form \'City,Country(Abbreviated)\'")
        
    #     print("Ex: Waco, US")
        
    #     loc = input("")
        
    #     m = weather_retrieve(str(loc))
        
    #     new_str = "Temperature (Degrees F): {}, High: {}, Low: {}".format(m['temp'],m['temp_max'],m['temp_min'])
        
    #     if m['feels_like'] < 50:
    #         print("Wear a jacket!")
        
    #     elif m['feels_like'] > 80:
    #         print("Maybe rock that hat!")
        
    #     else:
    #         print("Wonderful weather we're having!")
        
    #     print(new_str)
    #     continue
    
    ints = predict_class(message)
    
    res = get_response(ints,intents)
    
    print("" + res)
    
print("Sleep Bot is successfully asleep...")
    