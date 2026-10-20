#define PIN_LED5 5
#define PIN_LED6 6
#define PIN_LED7 7
#define PIN_LED8 8
#define PIN_LED9 9 
#define PIN_LED10 10 
#define PIN_LED11 11
#define PIN_LED12 12



void setup()
{
	pinMode(PIN_LED5, OUTPUT);
	pinMode(PIN_LED6, OUTPUT);
	pinMode(PIN_LED7, OUTPUT);
	pinMode(PIN_LED8, OUTPUT);
	pinMode(PIN_LED9, OUTPUT);
	pinMode(PIN_LED10, OUTPUT);
	pinMode(PIN_LED11, OUTPUT);
	pinMode(PIN_LED12, OUTPUT);
}

void loop()
{
	digitalWrite(PIN_LED5, HIGH);
	delay(500);
	digitalWrite(PIN_LED5, LOW);
	digitalWrite(PIN_LED6, HIGH);
	delay(500);
	digitalWrite(PIN_LED6, LOW);
	digitalWrite(PIN_LED7, HIGH);
	delay(500);
	digitalWrite(PIN_LED7, LOW);
	digitalWrite(PIN_LED8, HIGH);
	delay(500);
	digitalWrite(PIN_LED8, LOW);
	digitalWrite(PIN_LED9, HIGH);
	delay(500);
	digitalWrite(PIN_LED9, LOW);
	digitalWrite(PIN_LED10, HIGH);
	delay(500);
	digitalWrite(PIN_LED10, LOW);
	digitalWrite(PIN_LED11, HIGH);
	delay(500);
	digitalWrite(PIN_LED11, LOW);
	digitalWrite(PIN_LED12, HIGH);
	delay(500);
	digitalWrite(PIN_LED12, LOW);
	delay(500);
	
}