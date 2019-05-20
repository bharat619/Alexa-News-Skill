# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app,"/reddit_reader")

def getheadlines():
    user_pass_dict = {'user': 'USERNAME', 'passwd': 'PASSWORD', 'api_type': 'JSON'}
    sess = requests.Session()
    sess.headers.update({'User-Agent':'I am testing Alexa'})
    sess.post('https://www.reddit.com/api/login',data=user_pass_dict)
    time.sleep(1)
    url = "https://www.reddit.com/r/indianews/.json?limit=10"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = "...".join([i for i in titles])
    return titles

#titles = getheadlines()
#print(titles)
    

@app.route('/')
def homepage():
    return statement("Hi there. How are you doing?")

@ask.launch
def start_skill():
    welcome_message = "Hello you idiot!! Would like to hear the news?"
    return question(welcome_message)

@ask.intent('YesIntent')
def share_headlines():
    headlines = getheadlines()
    headline_message = "The current Indian headlines are as follows {}".format(headlines)
    return statement(headline_message)

@ask.intent('NoIntent')
def no_intent():
    bye_text = "Okay sure. Seems like you prefer not to be enlightened with the news. Okay..... Bye"
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)