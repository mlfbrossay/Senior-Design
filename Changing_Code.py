import serial
import numpy as np
import time
from threading import Thread

ser = serial.Serial('/dev/rfcomm0', 9600)

from flask import Flask
from flask_ask import Ask, statement, question, session
import datetime

app = Flask(__name__)
ask = Ask(app, "/switch")

startbool = False

def receive_data():
    while (True):
        #Read one byte at a time
        if (ser.inWaiting() > 0):
            character = ser.read()
            asciiOrd = ord(character)
            #If it is a start sequence and we have already started,
            #start over.
            if (asciiOrd == 60 and startbool == True):
                temp = []
            #If it is a start sequence and we have not started,
            #start now
            elif (asciiOrd == 60 and startbool == False):
                startbool = True

            #If it is not a start or a stop, and we have started,
            #simply append.
            elif (asciiOrd != 60 and asciiOrd !=62 and startbool == True):
                temp.append(character.decode('ascii'))
            #If it is an end character, and we have started then we are done.
            elif (asciiOrd == 62 and startbool == True):

                #If there is something there, and it is a proper float
                if len(temp) > 0:
                    try:
                        converted = float(''.join(temp))
                        saveReading(converted)
                        #Acknowledge receipt of data
                        ser.write('<5>'.encode('utf-8'))
                    except Exception as e:
                        print(e)
                startbool = False
                temp = []

def switch_on():    #Turns on switch
    print('switch has turned on')
    ser.write('<1>'.encode('utf-8'))

def switch_off():   #Turns off switch
    print('switch has turned off')
    ser.write('<0>'.encode('utf-8'))

print('------ ', datetime.datetime.now(), ' Program started')   #Will print when program initially runs

@app.route('/')
def homepage():
    return "Hi"

@ask.launch     #This occurs when the user says "Alexa, launch (...)"
def start_skill():
    t = Thread(target = receive_data)
    t.setDaemon(True)
    t.start()
    print('yes?')
    welcome_message = 'Hello, would you like to turn your switch on or off?'
    return question(welcome_message)    #Alexa will ask the above question

@ask.intent("OnIntent")     #If the user says "On," this will run
def turn_on():
    switch_on()             #Function called to turn on switch
    print(datetime.datetime.now(), " Switch turned on") #Tells user what has happened at current date/time
    on_text = "Okay, I've turned it on"
    return statement(on_text)   #Alexa says the above statement

@ask.intent("OffIntent")    #If the user says "Off," this will run
def turn_off():
    switch_off()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
    off_text = "Okay, I've turned it off"
    return statement(off_text)  #Alexa says the above statement

######## NEW ###########
@ask.intent("OnFromLaunchIntent")    #If the user says "Off," this will run
def turn_on_from_launch():
    switch_on()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned on") #Tells user what has happened at current date/time
    on_text = "Okay, I've turned it on"
    return statement(on_text)  #Alexa says the above statement

@ask.intent("OffFromLaunchIntent")    #If the user says "Off," this will run
def turn_off_from_launch():
    switch_off()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
    off_text = "Okay, I've turned it off"
    return statement(off_text)  #Alexa says the above statement
######### NEW ##########

def saveReading(temperature):
    newReading = time.strftime("%Y-%m-%d %H:%M:%S") + \
                 ',' + str(temperature) + '\n'
    
    print('Saving new reading: ' + newReading)
    with open('/home/pi/Desktop/temperatureReadings.csv', 'ab') as file:
        file.write(newReading.encode('utf-8'))

print("Waiting for data...")
temp = []
startbool = False

            
if __name__ == '__main__':
    app.run(debug = True)
    
