#include <dht.h>;

//I/O
int motorTranPin = A0; 
int moisSensorTranPin = A1;
int sensorPin = A2;
int tempSensorPin = A3;
int boardLed = 13;
int interruptPin2 = 0; //switch interrupt

volatile byte state = HIGH;

//Values
int sensorValue;
//double tempValue;
//double humValue;

//Constants
int watertime = 3; // how long to water in seconds
int waittime = 1; // how long to wait between watering, in seconds 
dht DHT;

void setup()
{
 Serial.begin(9600);
 pinMode(motorTranPin, OUTPUT); // A0
 pinMode(moisSensorTranPin, OUTPUT); // A1
 pinMode(boardLed, OUTPUT); 
 digitalWrite(motorTranPin, LOW);  // turn off the motor    
 
 pinMode(2, INPUT_PULLUP);
 attachInterrupt(interruptPin2, turnOn, CHANGE);
 
}

void loop()
{
  
  /*
  digitalWrite(moisSensorTranPin, HIGH); // moisSensorTranPin HIGH
  delay(200);
  sensorValue = analogRead(sensorPin);
  digitalWrite(moisSensorTranPin, LOW); // moisSensorTranPin LOW
  delay(200);
  
  int chk = DHT.read11(tempSensorPin);
  
  Serial.print("Moisture = " );
  Serial.println(sensorValue);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  
  if(sensorValue < 600)
  {
    digitalWrite(boardLed, HIGH); //LED on
    digitalWrite(motorTranPin, HIGH); // turn on the motor
    delay(watertime*1000); 
    digitalWrite(motorTranPin, LOW);  // turn off the motor
    digitalWrite(boardLed, LOW); //LED off
  }  
  
  delay(waittime*1000);
  */
  
  /*
   int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  delay(1000);
  */
  
  /*
  digitalWrite(motorTranPin, HIGH); // turn on the motor
  digitalWrite(blinkPin, HIGH); // turn on the LED
  digitalWrite(moisSensorTranPin, HIGH); // turn on the LED2
  delay(watertime*1000);        // multiply by 1000 to translate seconds to milliseconds

  digitalWrite(motorTranPin, LOW);  // turn off the motor
  //digitalWrite(blinkPin, LOW);  // turn off the LED
  digitalWrite(moisSensorTranPin, LOW); // turn off the LED2
  delay(waittime*60000);        // multiply by 60000 to translate minutes to milliseconds
  */
}

void turnOn() {
  state = digitalRead(2);
  
  if (state == HIGH) {
    digitalWrite(A0, HIGH);
    digitalWrite(boardLed, HIGH);
  } 
  if (state == LOW) {
    digitalWrite(A0, LOW);
    digitalWrite(boardLed, LOW);
  }
}
