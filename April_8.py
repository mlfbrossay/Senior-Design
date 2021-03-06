import serial
import numpy as np
import time
from flask import Flask
from flask_ask import Ask, statement, question, session
from datetime import datetime
from threading import Thread
import queue
import MySQLdb
import random

cnx= {'host': 'ammdb.clhkk5qyeyu2.us-east-1.rds.amazonaws.com',
  'username': 'amm',
  'password': 'Aslani123!',
  'db': 'sdamm'}

db = MySQLdb.connect(cnx['host'],cnx['username'],cnx['password'], cnx['db'])

cur = db.cursor()

cur.execute("DELETE FROM plug1")
cur.execute("DELETE FROM plug2")
cur.execute("DELETE FROM plug3")

db.commit()

q = queue.Queue()
q.put("0.0")

ser = serial.Serial('/dev/rfcomm0', 9600)

ino1 = [0,0,0,0,0,0,0,0,0,0,0,0]
ino2 = [0,0,0,0,0,0,0,0,0,0,0,0]
ino3 = [0,0,0,0,0,0,0,0,0,0,0,0]

app = Flask(__name__)
ask = Ask(app, "/switch")

print('------ ', datetime.now(), ' Program started')   #Will print when program initially runs

print("Waiting for data...")

def switch_on():    #Turns on switch
    print('switch has turned on')
    ser.write('<1>'.encode('utf-8'))

def switch_off():   #Turns off switch
    print('switch has turned off')
    ser.write('<0>'.encode('utf-8'))

@ask.intent("OnFromLaunchIntent")    #If the user says "Off," this will run
def turn_on_from_launch():
    switch_on()            #function called to turn off switch
    print(datetime.now(), " Switch turned on") #Tells user what has happened at current date/time
    on_text = "Okay, I've turned it on"
    return statement(on_text)  #Alexa says the above statement

@ask.intent("OffFromLaunchIntent")    #If the user says "Off," this will run
def turn_off_from_launch():
    switch_off()            #function called to turn off switch
    print(datetime.now(), " Switch turned off") #Tells user what has happened at current date/time
    off_text = "Okay, I've turned it off"
    return statement(off_text)  #Alexa says the above statement

@ask.intent("AskMostRecentOne")
def mostRecentMinute1():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug1 ORDER BY collection_time DESC LIMIT 1) a")
    temp = cur.fetchone()
    recent_text = "Your plug one most recent power usage was " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskMostRecentTwo")
def mostRecentMinute2():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug2 ORDER BY collection_time DESC LIMIT 1) a")
    temp = cur.fetchone()    
    recent_text = "Your plug two most recent power usage was " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskMostRecentThree")
def mostRecentMinute3():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug3 ORDER BY collection_time DESC LIMIT 1) a")
    temp = cur.fetchone()  
    recent_text = "Your plug three most recent power usage was " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskThirtyAverageOne")
def mostRecentHalfHour1():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug1 ORDER BY collection_time DESC LIMIT 30) a")
    temp = cur.fetchone()  
    recent_text = "In the last half hour plug one used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskThirtyAverageTwo")
def mostRecentHalfHour2():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug2 ORDER BY collection_time DESC LIMIT 30) a")
    temp = cur.fetchone()  
    recent_text = "In the last half hour plug two used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskThirtyAverageThree")
def mostRecentHalfHour3():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug3 ORDER BY collection_time DESC LIMIT 30) a")
    temp = cur.fetchone()  
    recent_text = "In the last half hour plug three used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskHourAverageOne")
def mostRecentHour1():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug1 ORDER BY collection_time DESC LIMIT 60) a")
    temp = cur.fetchone()  
    recent_text = "In the last hour plug one used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskHourAverageTwo")
def mostRecentHour2():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug2 ORDER BY collection_time DESC LIMIT 60) a")
    temp = cur.fetchone()  
    recent_text = "In the last hour plug two used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskHourAverageThree")
def mostRecentHour3():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug3 ORDER BY collection_time DESC LIMIT 60) a")
    temp = cur.fetchone()  
    recent_text = "In the last hour plug three used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskDayAverageOne")
def mostRecentDay1():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug1 ORDER BY collection_time DESC LIMIT 1440) a")
    temp = cur.fetchone()  
    recent_text = "In the last day plug one used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskDayAverageTwo")
def mostRecentDay2():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug2 ORDER BY collection_time DESC LIMIT 1440) a")
    temp = cur.fetchone()  
    recent_text = "In the last day plug two used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

@ask.intent("AskDayAverageThree")
def mostRecentDay3():
    cur.execute("SELECT AVG(a.power_data) FROM (SELECT power_data FROM plug3 ORDER BY collection_time DESC LIMIT 1440) a")
    temp = cur.fetchone()  
    recent_text = "In the last day plug three used " + str(temp) + " watts"
    print(recent_text)
    return statement(recent_text)

def saveReading(temp, q):
    power = str(temp)
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
    while (True):
        ino1 = [0,0,0,0,0,0,0,0,0,0,0,0]
        ino2 = [0,0,0,0,0,0,0,0,0,0,0,0]
        ino3 = [0,0,0,0,0,0,0,0,0,0,0,0]

        for i in range(12):
            #REMIND: send signal ready for 1
            #ser.write('<1>'.encode('utf-8')) #to be updated

            #Read one byte at a time
            while(True):
                if(ser.inWaiting() > 0):
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
                                ino1[i] = converted;
                                power = str(converted)
                                saveReading(converted, q)
                                #Acknowledge receipt of data
                                ser.write('<5>'.encode('utf-8'))
                            except Exception as e:
                                print(e)
                        start = False
                        temp = []
                        break

            print(ino1)

            #REMIND: send signal ready for 2
            #ser.write('<2>'.encode('utf-8')) #to be updated

            while(True):
                if(ser.inWaiting() > 0):
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
                                ino2[i] = converted
                                power = str(converted)
                                saveReading(converted, q)
                                #Acknowledge receipt of data
                                ser.write('<5>'.encode('utf-8'))
                            except Exception as e:
                                print(e)
                        start = False
                        temp = []
                        break

            print(ino2)


            #REMIND: send signal ready for 3
            #ser.write('<3>'.encode('utf-8')) #to be updated

            while(True):
                if(ser.inWaiting() > 0):
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
                                ino3[i] = converted
                                power = str(converted)
                                saveReading(converted, q)
                                #Acknowledge receipt of data
                                ser.write('<5>'.encode('utf-8'))
                            except Exception as e:
                                print(e)
                        start = False
                        temp = []
                        break

            print(ino3)

        #temp
        switch1 = random.random()*100
        switch2 = random.random()*50
        switch3 = random.random()*25

        #print(ino1)
        #switch1 = sum(ino1)/len(ino1)
        print(switch1)
        #print(ino2)
        #switch2 = float(sum(ino2)/len(ino2))
        print(switch2)
        #print(ino3)
        #switch3 = float(sum(ino3)/len(ino3))
        print(switch3)


        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        cur.execute("INSERT INTO plug1 (collection_time,power_data) VALUES (%s,%s)", (formatted_date, switch1))
        cur.execute("INSERT INTO plug2 (collection_time,power_data) VALUES (%s,%s)", (formatted_date, switch2))
        cur.execute("INSERT INTO plug3 (collection_time,power_data) VALUES (%s,%s)", (formatted_date, switch3))

        db.commit()


if __name__ == '__main__':
    t1 = Thread(target = readFrom, args = (q,))
    t1.start()
    app.run(debug=False)
