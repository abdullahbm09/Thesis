#include <dht.h>
dht DHT;
#define DHT11_PIN 7  //sensor pin
char serialData;
int d;   //converting float value into integar
bool ledstate = 1;
int period = 3000;
unsigned long time_now = 0;


void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);        //Green LED
  pinMode(4, OUTPUT);        //Red LED 
  digitalWrite(2,LOW);       //Safe 
  digitalWrite(4,HIGH);      //Dangerous
  int chk = DHT.read11(DHT11_PIN);
  time_now = millis();
  d = (int) DHT.temperature;
}


void loop() 
{
  if(millis() > time_now + period)
  {
    digitalWrite(2, HIGH);
    digitalWrite(4, LOW);
    }

  
  if(Serial.available() > 0)   //check for Incoming serial data
  {
    serialData = Serial.read();     //find the state
    if ((serialData == '1')            // if above 30 then turn RED LED ON and GREEN LED OFF
    {
      digitalWrite(4, HIGH);       //RED ON
      digitalWrite(2,LOW);         //GREEN OFF
      Serial.print(d);             //Sending Sensor data 
      //delay(2000);                 //Transation for 2 seconds
      time_now = millis();   
      //digitalWrite(2, HIGH);       //Green ON
      //digitalWrite(4, LOW);        //Red OFF   
    }
    
    else if ((serialData == '0') && (ledstate == 1))     //if less than 30 then turn Green LED ON and Red LED OFF
    {
      digitalWrite(2, HIGH);       //Green ON
      digitalWrite(4, LOW);        //Red OFF
      Serial.print(d);
      //ledstate = 0; 
      //delay(2000);                 //Transation for 2 seconds
      //digitalWrite(4, HIGH);       //RED ON
      digitalWrite(2,LOW);         //GREEN OFF
    }
     
  }
}
  
  //d = (int) DHT.temperature;
  //Serial.print(d);
  //digitalWrite(2, HIGH);   // turn the LED on (HIGH is the voltage level)
  //digitalWrite(4, LOW);   // turn the LED on (HIGH is the voltage level)
  //delay(2000);                       // wait for a second
  //digitalWrite(2, LOW);    // turn the LED off by making the voltage LOW
  //digitalWrite(4, HIGH);   // turn the LED on (HIGH is the voltage level)
  //delay(2000);                       // wait for a second
