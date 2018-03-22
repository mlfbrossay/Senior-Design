from flask import Flask
from flask_ask import Ask, statement, question, session
from bs4 import BeautifulSoup #entered
import json
import requests
import time
import unidecode
import urllib3		#entered

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")


def get_headlines():
	http = urllib3.PoolManager()
	url = 'http://www.businessinsider.com/sai'
	response = http.request('GET', url)
	soup = BeautifulSoup(response.data, "html.parser")
	# Take out the <div> of name and get its value
	name_box = soup.findAll('a', attrs={'class': 'title'})
	for each in name_box:
		each1 = each.text.strip()
	return each1

each1 = get_headlines() #changed
print(each1)			#changed

@app.route('/')
def homepage():
	return "Hi"

@ask.launch
def start_skill():
	welcome_message = 'Hello there, would you like to hear the latest article on Tech Insider?'
	return question(welcome_message)


@ask.intent("YesIntent")
def share_headlines():
	headlines = get_headlines()
	headline_msg = 'The most recent article is. {}' .format(headlines)
	return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
	bye_text = 'Okay, bye!'
	return statement(bye_text)

if __name__ == '__main__':
	app.run(debug = False)