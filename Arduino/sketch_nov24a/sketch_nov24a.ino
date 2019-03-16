#include <dht.h>

dht DHT;

#define DHT11_PIN 7
int d;   //converting float value into integar
char serialData;
int period = 3000;
unsigned long time_now = 0;
void setup(){
  Serial.begin(9600);
  int chk = DHT.read11(DHT11_PIN);
  d = (int) DHT.temperature;
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);        //Green LED        //Red LED 
  digitalWrite(2,LOW);       //Safe
  time_now = millis();
}

void loop()
{
        //RED ON
  digitalWrite(2,HIGH);
  Serial.print(d);//GREEN OFF
  delay(2000);
  digitalWrite(2,LOW);
  delay(5000);
}
