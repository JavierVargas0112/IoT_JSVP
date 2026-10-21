// TempHumiX : Arduino UNO R4 WiFi
// LED de vie, lecture DHT22 toutes les 2 s, date/heure fournie par le RTC
// interne, affichage LCD Grove RGB et envoi sur le port série.
// Machine d'état cadencée à 500 ms par delay(500).
#include <Wire.h>
#include <DHT.h>
#include <rgb_lcd.h>
#include <RTC.h>

#define PIN_LED_VIE 2
#define PIN_BARGRAPH 3 // bargraphe sur les broches 3 à 12
#define NB_LEDS 10
#define PIN_DHT A0

rgb_lcd lcd;
DHT dht(PIN_DHT, DHT22);

// Etats de la machine d'état (1 état = 500 ms, cycle complet = 2 s)
enum Etat
{
  LECTURE_CAPTEUR, // t = 0 ms    : lecture DHT22
  ATTENTE_1,       // t = 500 ms
  ATTENTE_2,       // t = 1000 ms
  ATTENTE_3        // t = 1500 ms
};

Etat etat = LECTURE_CAPTEUR;
bool ledVie = false;
float temperature = 0;
float humidite = 0;

void afficherBargraphe()
{
  int nb = humidite / 10; // humidité 0-100 % -> 0-10 LEDs
  for (int i = 0; i < NB_LEDS; i++)
  {
    digitalWrite(PIN_BARGRAPH + i, i < nb ? HIGH : LOW);
  }
}

// Ligne 1 du LCD : date et heure lues dans le RTC
void afficherDate()
{
  char date[21];
  RTCTime maintenant;
  RTC.getTime(maintenant);

  int jour = maintenant.getDayOfMonth();
  int mois = Month2int(maintenant.getMonth());
  // Le LCD fait 16 caractères : pas d'espace si jour et mois ont 2 chiffres
  const char *format = (jour >= 10 && mois >= 10) ? "%d/%d/%02d%02d:%02d:%02d"
                                                  : "%d/%d/%02d %02d:%02d:%02d";
  sprintf(date, format,
          jour,
          mois,
          maintenant.getYear() % 100,
          maintenant.getHour(),
          maintenant.getMinutes(),
          maintenant.getSeconds());
  lcd.setCursor(0, 0);
  lcd.print(date);
}

// Lecture du DHT22, ligne 2 du LCD et envoi sur le port série
void lireCapteur()
{
  char ligne[21];
  char txtT[8];
  char txtH[8];

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

  RTCTime maintenant;
  RTC.getTime(maintenant);
  Serial.println(maintenant.toString()); // format AAAA-MM-JJTHH:MM:SS
  Serial.print("Temperature : ");
  Serial.print(txtT);
  Serial.println(" oC");
  Serial.print("Humidite    : ");
  Serial.print(txtH);
  Serial.println(" %");
  Serial.println();

  sprintf(ligne, "T %soC/H %s%%", txtT, txtH);
  lcd.setCursor(0, 1);
  lcd.print(ligne);
}

void setup()
{
  pinMode(PIN_LED_VIE, OUTPUT);
  for (int i = 0; i < NB_LEDS; i++)
  {
    pinMode(PIN_BARGRAPH + i, OUTPUT);
  }
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 255);
  dht.begin();

  // Initialisation du RTC avec une date de départ
  // (elle sera remplacée par la synchronisation NTP en 6.1.3)
  RTC.begin();
  RTCTime depart(21, Month::OCTOBER, 2026, 14, 0, 0,
                 DayOfWeek::WEDNESDAY, SaveLight::SAVING_TIME_INACTIVE);
  RTC.setTime(depart);
}

void loop()
{
  // LED de vie : change d'état toutes les 500 ms
  ledVie = !ledVie;
  digitalWrite(PIN_LED_VIE, ledVie ? HIGH : LOW);

  // Date/heure rafraîchie à chaque tour (500 ms) pour ne sauter aucune seconde
  afficherDate();

  switch (etat)
  {
  case LECTURE_CAPTEUR:
    lireCapteur();
    etat = ATTENTE_1;
    break;

  case ATTENTE_1:
    etat = ATTENTE_2;
    break;

  case ATTENTE_2:
    etat = ATTENTE_3;
    break;

  case ATTENTE_3:
    etat = LECTURE_CAPTEUR;
    break;
  }

  delay(500);
}