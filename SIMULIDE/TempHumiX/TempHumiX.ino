// TempHumiX : LED de vie 2 Hz, lecture DHT22 toutes les 2 s,
// dateur, affichage LCD et envoi sur le port série
#include <LiquidCrystal_AIP31068_I2C.h>
#include <DHT.h>

#define PIN_LED_VIE 2
#define PIN_BARGRAPH 3 // bargraphe sur les broches 3 à 12
#define NB_LEDS 10
#define PIN_DHT A0

LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);
DHT dht(PIN_DHT, DHT22);

// Dateur (mois de 30 jours)
int jour = 10, mois = 2, annee = 25;
int heure = 13, minute = 42, seconde = 29;

float temperature = 0;
float humidite = 0;
unsigned int tick = 0; // 1 tick = 100 ms

void avancerDate()
{
  seconde++;
  if (seconde == 60)
  {
    seconde = 0;
    minute++;
  }
  if (minute == 60)
  {
    minute = 0;
    heure++;
  }
  if (heure == 24)
  {
    heure = 0;
    jour++;
  }
  if (jour == 31)
  {
    jour = 1;
    mois++;
  }
  if (mois == 13)
  {
    mois = 1;
    annee++;
  }
}

void afficherBargraphe()
{
  int nb = humidite / 10; // humidité 0-100 % -> 0-10 LEDs
  for (int i = 0; i < NB_LEDS; i++)
  {
    digitalWrite(PIN_BARGRAPH + i, i < nb ? HIGH : LOW);
  }
}

void setup()
{
  pinMode(PIN_LED_VIE, OUTPUT);
  for (int i = 0; i < NB_LEDS; i++)
  {
    pinMode(PIN_BARGRAPH + i, OUTPUT);
  }
  Serial.begin(9600);
  lcd.init();
  dht.begin();
}

void loop()
{
  char date[21];
  char ligne[21];
  char txtT[8];
  char txtH[8];

  // a) LED de vie à 2 Hz : période 500 ms = 5 ticks
  digitalWrite(PIN_LED_VIE, (tick % 5) < 2 ? HIGH : LOW);

  // c) Dateur : +1 seconde tous les 10 ticks
  if (tick % 10 == 0)
  {
    avancerDate();
  }

  // b) Lecture du DHT22 toutes les 2000 ms = 20 ticks
  if (tick % 20 == 0)
  {
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if (!isnan(t) && !isnan(h))
    {
      temperature = t;
      humidite = h;
    }
    afficherBargraphe();

    dtostrf(temperature, 4, 1, txtT);
    dtostrf(humidite, 4, 1, txtH);

    // f) Envoi sur le port série
    sprintf(date, "%d/%d/%02d %02d:%02d:%02d", jour, mois, annee, heure, minute, seconde);
    Serial.println(date);
    Serial.print("Temperature : ");
    Serial.print(txtT);
    Serial.println(" oC");
    Serial.print("Humidite    : ");
    Serial.print(txtH);
    Serial.println(" %");
    Serial.println();

    // e) Ligne 2 du LCD : température et humidité
    sprintf(ligne, "T %soC/H %s%%", txtT, txtH);
    lcd.setCursor(0, 1);
    lcd.print(ligne);
  }

  // d) Ligne 1 du LCD : date et heure (chaque seconde)
  if (tick % 10 == 0)
  {
    sprintf(date, "%d/%d/%02d %02d:%02d:%02d", jour, mois, annee, heure, minute, seconde);
    lcd.setCursor(0, 0);
    lcd.print(date);
  }

  tick++;
  delay(100);
}