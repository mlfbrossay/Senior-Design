  #include <SoftwareSerial.h>

  #define RxD 10
  #define TxD 11

  SoftwareSerial BTSerial(RxD, TxD);

  void setup()
  {
    BTSerial.flush();
    delay(500);
    BTSerial.begin(9600);
    Serial.begin(9600);
    Serial.print("The controller has successfuly connected to the PC\n");
    delay(100);
  }

  void loop()
  {
    while(BTSerial.available() == 0);
    char val = BTSerial.read();
    if(val == '#'){
      Serial.print('\n');
    }
    else{
      Serial.print(val);
      BTSerial.write(val);
    }
  }
