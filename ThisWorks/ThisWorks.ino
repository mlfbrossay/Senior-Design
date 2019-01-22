#include <SoftwareSerial.h>

SoftwareSerial btSerial(10, 11); // RX, TX

//Tells us we are sending over Serial
const int senderPin = 7;

//Tells us we are receiving confirmation over Serial
const int receiverPin = 8;
const int sendSwitch = 2;

float degreesC;
unsigned long timer = 0;
int sendStatus = 0;

void setup() {
  
  pinMode(senderPin, OUTPUT);
  pinMode(receiverPin, OUTPUT);
  pinMode(sendSwitch, INPUT_PULLUP);
  pinMode(7, OUTPUT);
  
  //Setup and flush the serials to begin
  btSerial.begin(9600);
  Serial.begin(9600);
  btSerial.flush();
  Serial.flush();
  digitalWrite(7, HIGH);
  delay(50);
  digitalWrite(7, LOW);
  delay(50);
  digitalWrite(7, HIGH);
  delay(50);
  digitalWrite(7, LOW);
}

void loop() {
    
  //I want to send the temperature, I want the Raspberry PI to grab it, process it
  //and send back a message. I don't want to continue spamming the raspberry pi, so
  //I will only send a signal every 1 seconds.
  
  //Non-blocking every 10 seconds.
  if ((timer == 0 || millis() >= timer) && sendStatus == 1){
    
    //Grab the current temperature in celsius
    float val = getVoltage();
    
    //Send the current temperature. Didn't use readline to avoid blocking problem
    String sendDegrees = "<" + String(val, 2) + ">";
    
    //Convert to byte array
    char charArray[sendDegrees.length() + 1];
    sendDegrees.toCharArray(charArray, sendDegrees.length()+1);
    
    btSerial.write(charArray);
    
    //Reset the timer for another 1 seconds.
    timer = millis() + 3000;
      
  }
  
  checkButton();
 

  //Received message back from Raspberry.
  //RPI sends back messages in the form of <5>.
  //We only check for the numerical.
  while (btSerial.available()) {
    //Numbers are between 48 and 57
    char rpiMessage = btSerial.read();
    if(rpiMessage == '1'){
      digitalWrite(7, HIGH);
    }
    if(rpiMessage == '0'){
      digitalWrite(7, LOW);
    }
    Serial.println(rpiMessage); //Shows message from RPi
    
  }
    
}

//Checks to see if the user wants to keep sending messages.
void checkButton() {
  sendStatus = 1;
}

float getVoltage() {
    return 120;
}

