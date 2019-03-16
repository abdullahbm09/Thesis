#include <dht.h>
dht DHT;
#define DHT_11 PIN 7;
char serialData; 

void setup () {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  //Serial.print("Temperature = ");
  Serial.print(DHT.temperature);

  
  if(Serial.available() > 0){
    serialData = Serial.read();
    Serial.print(serialData);

    if (serialData == '1'){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if (serialData == '0'){
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
  delay(7000);
}
