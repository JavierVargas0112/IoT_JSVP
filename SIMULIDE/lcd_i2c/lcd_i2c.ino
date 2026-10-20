#include <Wire.h>
#include <LiquidCrystal_AIP31068_I2C.h>

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);

void setup()
{

	lcd.init();
	lcd.setCursor(0 , 0);
	lcd.print("Hello");
	lcd.setCursor(11 , 1);
	lcd.print("World");

}

void loop()
{

}