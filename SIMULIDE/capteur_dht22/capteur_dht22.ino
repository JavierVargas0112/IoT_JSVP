#include <DHT.h>

#define PIN_LED_ROUGE 12
#define PIN_LED_VERT 3

#define DHTPIN A0
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup()
{
	Serial.begin(9600);
	
	
	dht.begin();
	
	pinMode(PIN_LED_ROUGE, OUTPUT);
	pinMode(PIN_LED_VERT, OUTPUT);
	
}

void loop()
{
	delay(2000);
	
	
	
	float t = dht.readTemperature();
	
	if(isnan(t)){
	Serial.println("errooor");
	}
	
	if (t < 20.0){
	digitalWrite(PIN_LED_ROUGE, LOW);
	digitalWrite(PIN_LED_VERT, HIGH);
	}
	
	if (t > 20.0){
	digitalWrite(PIN_LED_ROUGE, HIGH);
	digitalWrite(PIN_LED_VERT, LOW);
	
	}
	

}