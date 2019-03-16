#include <dht.h>
dht DHT;
#define DHT11_PIN 7
char serialData; 
bool ledstate = 0;
//int LED_BUILTIN = 13;
int period = 3000;
unsigned long time_now = 0;
void setup () {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  int chk = DHT.read11(DHT11_PIN);
  time_now = millis();
}

void loop()
{
   if(millis() > time_now + period){
        //time_now = millis();
        //Serial.println("Hello");
        digitalWrite(LED_BUILTIN, LOW);
    }
  while(Serial.available() > 0){
    serialData = Serial.read();

    if ((serialData == '1') && (ledstate == 0)) {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.print(DHT.temperature);
      ledstate = 1; 
      time_now = millis();
    }
    else if ((serialData == '0') && (ledstate == 1)){
      digitalWrite(LED_BUILTIN, LOW);
      //delay(3000);
      Serial.print(DHT.temperature);
      ledstate = 0; 
    }
     
  }
  //Serial.print("Temperature = ");
  

}
