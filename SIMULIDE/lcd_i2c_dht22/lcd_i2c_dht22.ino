#include <Wire.h>
#include <LiquidCrystal_AIP31068_I2C.h>

#include <DHT.h>

#define PIN_LED_ROUGE 12
#define PIN_LED_VERT 3

#define DHTPIN A0
#define DHTTYPE DHT22

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);
DHT dht(DHTPIN, DHTTYPE);

void setup()
{

	dht.begin();

	lcd.init();
	lcd.setCursor(2 , 0);
	lcd.print("IMT NE - PPI");


}

void loop()
{

	delay(2000);

	float t = dht.readTemperature();
	float h = dht.readHumidity();
	
	String text = "T " + String(t, 1) + "\xDF" "C/H " + String(h, 1) + "%";
	
	lcd.setCursor(0 , 1);
	lcd.print(text);
	
	

}