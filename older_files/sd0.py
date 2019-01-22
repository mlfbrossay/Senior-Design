from flask import Flask
from flask_ask import Ask, statement, question, session
import datetime

app = Flask(__name__)
ask = Ask(app, "/switch")

#def switch_on():	#Turns on switch
#    return NULL


#def switch_off():	#Turns off switch
#    return NULL

print('------ ', datetime.datetime.now(), ' Program started')	#Will print when program initially runs

@app.route('/')
def homepage():
	return "Hi"

@ask.launch		#This occurs when the user says "Alexa, launch (...)"
def start_skill():
	welcome_message = 'Hello there, would you like to turn your switch on or off?'
	return question(welcome_message)	#Alexa will ask the above question

@ask.intent("OnIntent")		#If the user says "On," this will run
def turn_on():
    #	switch_on()				#Function called to turn on switch
	print(datetime.datetime.now(), " Switch turned on")	#Tells user what has happened at current date/time
	on_text = "Okay, I'll turn it on for you"
	return statement(on_text)	#Alexa says the above statement

@ask.intent("OffIntent")	#If the user says "Off," this will run
def turn_off():
    #	switch_off()			#function called to turn off switch
	print(datetime.datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
	off_text = "Okay, I've turned it off"
	return statement(off_text)	#Alexa says the above statement

if __name__ == '__main__':
	app.run(debug = True)



#Things to do:
#
#	Make 'switch_on' and 'switch_off' functions
#
#	Eventually get confirmation message from Arduino that it is turned on,
#	then return statement to Alexa confirming
#
#   Include bluetooth setup, connection etc
#
#

