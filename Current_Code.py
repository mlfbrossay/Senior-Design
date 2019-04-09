import serial
import numpy as np
import time
from flask import Flask
from flask_ask import Ask, statement, question, session
import datetime
from threading import Thread
import queue

q = queue.Queue()
q.put("0.0")

ser = serial.Serial('/dev/rfcomm0', 9600)

app = Flask(__name__)
ask = Ask(app, "/switch")

print('------ ', datetime.datetime.now(), ' Program started')   #Will print when program initially runs

print("Waiting for data...")
#################
# Change these functions to accommodate each of the 3 switches
# Sends the switch number, then a '-', then a '1' for high or a '0' for low
def switch1_on():    #Turns on switch
    print('switch 1 has turned on')
    ser.write('<1-1>'.encode('utf-8'))

def switch1_off():   #Turns off switch
    print('switch 1 has turned off')
    ser.write('<1-0>'.encode('utf-8'))

def switch2_on():    #Turns on switch
    print('switch 2 has turned on')
    ser.write('<2-1>'.encode('utf-8'))

def switch2_off():   #Turns off switch
    print('switch 2 has turned off')
    ser.write('<2-0>'.encode('utf-8'))

def switch3_on():    #Turns on switch
    print('switch 3 has turned on')
    ser.write('<3-1>'.encode('utf-8'))

def switch3_off():   #Turns off switch
    print('switch 3 has turned off')
    ser.write('<3-0>'.encode('utf-8'))
###############

@ask.launch     #This occurs when the user says "Alexa, launch (...)"
def start_skill():
    welcome_message = 'Hello, would you like to turn your switch on or off?'
    return question(welcome_message)    #Alexa will ask the above question
########
# We dont need these anymore
#@ask.intent("OnIntent")     #If the user says "On," this will run
#def turn_on():
#    switch_on()             #Function called to turn on switch
#    print(datetime.datetime.now(), " Switch turned on") #Tells user what has happened at current date/time
#    on_text = "Okay, I've turned it on"
#    return statement(on_text)   #Alexa says the above statement

#@ask.intent("OffIntent")    #If the user says "Off," this will run
#def turn_off():
#    switch_off()            #function called to turn off switch
#    print(datetime.datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
#    off_text = "Okay, I've turned it off"
#    return statement(off_text)  #Alexa says the above statement
###########
###########
# Added intents for all 3 switches
@ask.intent("OnFromLaunchIntentOne")    #If the user says "Off," this will run
def turn_on1_from_launch():
    switch1_on()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned on") #Tells user what has happened at current date/time
    on_text = "Okay, I've turned it on"
    return statement(on_text)  #Alexa says the above statement

@ask.intent("OffFromLaunchIntentOne")    #If the user says "Off," this will run
def turn_off1_from_launch():
    switch1_off()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
    off_text = "Okay, I've turned it off"
    return statement(off_text)  #Alexa says the above statement

@ask.intent("OnFromLaunchIntentTwo")    #If the user says "Off," this will run
def turn_on2_from_launch():
    switch2_on()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned on") #Tells user what has happened at current date/time
    on_text = "Okay, I've turned it on"
    return statement(on_text)  #Alexa says the above statement

@ask.intent("OffFromLaunchIntentTwo")    #If the user says "Off," this will run
def turn_off2_from_launch():
    switch2_off()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
    off_text = "Okay, I've turned it off"
    return statement(off_text)  #Alexa says the above statement

@ask.intent("OnFromLaunchIntentThree")    #If the user says "Off," this will run
def turn_on3_from_launch():
    switch3_on()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned on") #Tells user what has happened at current date/time
    on_text = "Okay, I've turned it on"
    return statement(on_text)  #Alexa says the above statement

@ask.intent("OffFromLaunchIntentThree")    #If the user says "Off," this will run
def turn_off3_from_launch():
    switch3_off()            #function called to turn off switch
    print(datetime.datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
    off_text = "Okay, I've turned it off"
    return statement(off_text)  #Alexa says the above statement
#########
#########
# Adding in power options for all 3 switches, along with a "total power" option
@ask.intent("AskPowerIntentTotal")    #If the user says "Off," this will run
def reportPower():
    temp = q.get()
    power_text = "Your current power usage is " + temp + " watts"
    q.put(temp)
    print(temp)
    return statement(power_text)  #Alexa says the above statement

@ask.intent("AskPowerIntentOne")    #If the user says "Off," this will run
def reportPower():
    temp = q.get()
    power_text = "Your current power usage is " + temp + " watts"
    q.put(temp)
    print(temp)
    return statement(power_text)  #Alexa says the above statement

@ask.intent("AskPowerIntentTwo")    #If the user says "Off," this will run
def reportPower():
    temp = q.get()
    power_text = "Your current power usage is " + temp + " watts"
    q.put(temp)
    print(temp)
    return statement(power_text)  #Alexa says the above statement

@ask.intent("AskPowerIntentThree")    #If the user says "Off," this will run
def reportPower():
    temp = q.get()
    power_text = "Your current power usage is " + temp + " watts"
    q.put(temp)
    print(temp)
    return statement(power_text)  #Alexa says the above statement
#############
def saveReading(temperature, q):
    power = str(temperature)
    q.get()
    q.put(power)
    newReading = time.strftime("%Y-%m-%d %H:%M:%S") + \
                 ',' + power + '\n'
    print('Saving new reading: ' + newReading)
    with open('/home/pi/Desktop/temperatureReadings.csv', 'ab') as file:
        file.write(newReading.encode('utf-8'))


def readFrom(q):
    start = False
    temp = []
    ser.flushInput()
    #time.sleep(5)
    while (True):
        #Read one byte at a time
        if (ser.inWaiting() > 0):
            character = ser.read()
            asciiOrd = ord(character)
            #If it is a start sequence and we have already started,
            #start over.
            if (asciiOrd == 60 and start == True):
                temp = []
            #If it is a start sequence and we have not started,
            #start now
            elif (asciiOrd == 60 and start == False):
                start = True

            #If it is not a start or a stop, and we have started,
            #simply append.
            elif (asciiOrd != 60 and asciiOrd !=62 and start == True):
                temp.append(character.decode('ascii'))
            #If it is an end character, and we have started then we are done.
            elif (asciiOrd == 62 and start == True):

                #If there is something there, and it is a proper float
                if len(temp) > 0:
                    try:
                        converted = float(''.join(temp))
                        power = str(converted)
                        saveReading(converted, q)
                        #Acknowledge receipt of data
                        ser.write('<5>'.encode('utf-8'))  
                    except Exception as e:
                        print(e)
                start = False
                temp = []           

if __name__ == '__main__':
    t1 = Thread(target = readFrom, args = (q,))
    t1.start()
    app.run(debug=False)
        