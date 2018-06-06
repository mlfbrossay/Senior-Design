#Senior Design Project


6/5/18 (MT)

Added an Arduino program that basically receives the data sent to the HC-05 
module and prints it in serial monitor (can be found in the "tools" tab on
Arduino). On the Raspberry pi I used the bluez library along with minicon with the help of this 
blog (https://www.dfrobot.com/blog-901.html) and managed to pair the HC-05
module to the Raspberry Pi and send data one character at a time. The 
Arduino Code has an if statement so that basically if the data sent is a '1',
then pin 13 on the Arduino is HIGH. It will remain HIGH until a 0 is sent.
If we can put all of this stuff in a python script instead of typing out commands
in the terminal then ultimately we can control a relay through Alexa with very
minimal setting up. Will try to write it in the 'bluetooth0' file. 


6/4/18 (MT)

Added a pyton file called bluetooth0. Basically playing around with the HC-05
and trying to send one signal at a time.


6/3/18 (MT)

Thought we could use this as an update log? Let me know what you guys think.
Just add descriptions of whatever file you have added/changed. Make sure you
add your updates to the TOP of the log so the most latest changes are up there.

