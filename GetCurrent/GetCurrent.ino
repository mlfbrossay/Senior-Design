#include <Wire.h>
#include <Adafruit_ADS1015.h>

Adafruit_ADS1115 ads; //(0x48);

const float FACTOR = 30; //30A
const float multiplier = 0.0625F;

void setup() {
  Serial.begin(9600);

  ads.setGain(GAIN_TWO); // +/- 2.048V 1 bit = 0.0624mV
  ads.begin();
}

void printMeasure(String prefix, float value, String postfix)
{
  Serial.print(prefix);
  Serial.print(value, 8); // 3 decimals??
  Serial.print(postfix);
}

void loop() {
  float currentRMS = getCurrent();
  float power = 120 * currentRMS;

  printMeasure("RMS Current: ", currentRMS, "A ,");
  printMeasure("Power: ", power, "W \n");
  delay(1000);

}

float getCurrent()
{
  float voltage;
  float current;
  float sum = 0;
  long Time = millis();
  int counter = 0;

  while(millis() - Time < 1000){
    voltage = ads.readADC_Differential_0_1() * multiplier;
    current = voltage * FACTOR; //Conductance
    current /= 1000.0;

    sum += sq(current);
    counter = counter + 1;
  }
  current = sqrt(sum/counter); //avg
  return(current);
}


