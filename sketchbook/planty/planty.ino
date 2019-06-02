#include <dht.h>

//I/O
int motorTranPin = A0;
int moisSensorTranPin = A1;
int sensorPin = A2;
int tempSensorPin = A3;
int boardLed = 13;
int interruptPin2 = 0; //switch interrupt

volatile byte state = LOW;
volatile char rec = 'o';
volatile char sen = 'o';

String ets = "";
String debug = "false";
boolean stringComplete = false;
boolean serialFlag = false;
boolean switchFlag = false;

dht DHT;

void setup()
{
  Serial.begin(9600);
  pinMode(motorTranPin, OUTPUT); // A0
  pinMode(moisSensorTranPin, OUTPUT); // A1
  pinMode(boardLed, OUTPUT);
  digitalWrite(motorTranPin, LOW);  // turn off the motor

  pinMode(2, INPUT_PULLUP);
  
  Serial.println("Welcome!");

  if(digitalRead(2) == HIGH)
  {
    debug = "High";
  }else
  {
    debug = "Low";
  }
  
  Serial.println("Pin 2: " + debug);
  attachInterrupt(interruptPin2, switchMode, FALLING);

}

void loop()
{

  switch (state) {
    case HIGH:
      // Auto
      String action = "";
      
//      if (switchFlag)
//      {
//        //Serial.println("Pin 2: " + debug);
//        //digitalWrite(boardLed, LOW);
//        switchFlag = false;
//      }

      if (serialFlag == true && stringComplete == true)
      {
        //If ets = "MOTR"

        if (checkCommand(ets))
        {

          action = ets.substring(0, 4);

          if (ets.endsWith("\n"))
          {
            ets.remove(ets.length() - 1, 1);

          }

          if (action == "MOTR")
          {

            if (ets.substring(5).toInt() == 1)
            {
              digitalWrite(A0, HIGH);
              digitalWrite(boardLed, HIGH);
              Serial.println(ets + ",OK");

            }
            else if (ets.substring(5).toInt() == 0)
            {
              digitalWrite(A0, LOW);
              digitalWrite(boardLed, LOW);
              Serial.println(ets + ",OK");
            }
            else
            {
              Serial.println(ets + ",ERR");
            }

          }
          else if (action == "MOIS")
          {
            //Read mois sensor
            int moisValue = readMoistureSensor();

            if (moisValue == -1)
            {
              Serial.println(action + ",ERR");
            }
            else
            {
              Serial.println(ets + "=" + moisValue + ",OK");
            }

          }
          else if (action == "TEMP")
          {
            float tempHumValue = readHumTempSensor(ets.substring(5).toInt());

            if (tempHumValue == -1)
            {

              Serial.println(ets + ",ERR");
            }
            else
            {

              Serial.print(action + "=");
              Serial.print(tempHumValue);
              Serial.println(",OK");

            }
          }
        }
        else
        {

          Serial.println(ets + ",ERR");

        }

        //Set flag to false
        Serial.flush();
        ets = "";
        serialFlag = false;
        stringComplete = false;
      }

      break;
    case LOW:
      // Manual mode
      digitalWrite(boardLed, HIGH);

//      if (switchFlag)
//      {
//        Serial.println("Pin 2: " + debug);        
//        switchFlag = false;
//      }

      break;
    default:
      // statements
      break;
  }



}

void serialEvent() {
  //statements
 
    while (Serial.available()) {
      // get the new byte:
      char rec = (char)Serial.read();
      // add it to the inputString:
      ets += rec;
      if (rec == '\n') {
        stringComplete = true;
      }
      serialFlag = true;
    }
  

}

boolean checkCommand(String in)
{
  String action = in.substring(0, 4);


  if (action == "MOTR" || action == "MOIS" || action == "TEMP")
  {
    return true;
  }
  else
  {
    return false;
  }

}

int readMoistureSensor()
{
  int moisValue = -1;
  digitalWrite(moisSensorTranPin, HIGH); // moisSensorTranPin HIGH
  delay(200);
  moisValue = analogRead(sensorPin);
  digitalWrite(moisSensorTranPin, LOW); // moisSensorTranPin LOW
  delay(200);

  return moisValue;
}

float readHumTempSensor(int action)
{
  float humTempValue = -1;

  int chk = DHT.read11(tempSensorPin);

  if (action == 1) //If action=1 read temperature
  {
    humTempValue = DHT.temperature;
  }
  else if (action == 2) //if action=2 read humidity
  {
    humTempValue = DHT.humidity;
  }

  return humTempValue;

}

void switchMode() {
  state = digitalRead(2);
  switchFlag = true;

  if(digitalRead(2) == HIGH)
  {
    debug = "High";
  }else
  {
    debug = "Low";
  }

  Serial.println("Pin 2: " + debug);  

}
