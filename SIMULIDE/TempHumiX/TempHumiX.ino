// TempHumiX : Arduino UNO R4 WiFi
// LED de vie, lecture DHT22 toutes les 2 s, date/heure fournie par le RTC
// interne synchronisé par NTP, affichage LCD Grove RGB et port série.
// Machine d'état cadencée à 500 ms par delay(500).
#include <Wire.h>
#include <DHT.h>
#include <rgb_lcd.h>
#include <RTC.h>
#include <WiFiS3.h>   // WiFi du module ESP32-S3 du UNO R4 WiFi
#include <WiFiUdp.h>
#include <NTPClient.h>

#define VERSION "1.0"

#define PIN_LED_VIE 2
#define PIN_BARGRAPH 3 // bargraphe sur les broches 3 à 12
#define NB_LEDS 10
#define PIN_DHT A0

// Paramètres WIFI (paragraphe 5.1.1)
// Le réseau "IoT IMT Nord Europe 5G" ne fonctionne pas : le module
// ESP32-S3 du UNO R4 ne gère que la bande 2,4 GHz.
#define WIFI_SSID "IoT IMT Nord Europe"
#define WIFI_MDP "<mot de passe 5.1.1>"
#define WIFI_NB_ESSAIS 3

// Serveur NTP de IMT Nord Europe
#define NTP_SERVEUR "10.12.130.1"
#define FUSEAU_HORAIRE 7200   // UTC+2 (heure d'été), 3600 en heure d'hiver
#define NTP_CYCLES_RELANCE 30 // nouvel essai NTP toutes les 30 x 2 s = 1 min

rgb_lcd lcd;
DHT dht(PIN_DHT, DHT22);
WiFiUDP ntpUDP;
NTPClient ntpClient(ntpUDP, NTP_SERVEUR, FUSEAU_HORAIRE);

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
bool wifiOk = false;
bool ntpOk = false;
int cyclesSansNtp = 0;

// a) Connexion au réseau WIFI : retourne true si OK, false sinon
bool setup_wifi()
{
  if (WiFi.status() == WL_NO_MODULE)
  {
    Serial.println("Module WIFI absent");
    return false;
  }

  for (int essai = 1; essai <= WIFI_NB_ESSAIS; essai++)
  {
    Serial.print("Connexion a ");
    Serial.print(WIFI_SSID);
    Serial.print(" (essai ");
    Serial.print(essai);
    Serial.println(")");
    if (WiFi.begin(WIFI_SSID, WIFI_MDP) == WL_CONNECTED)
    {
      // l'adresse IP (DHCP) peut arriver un peu après la connexion
      for (int i = 0; i < 20 && WiFi.localIP() == IPAddress(0, 0, 0, 0); i++)
      {
        delay(100);
      }
      return true;
    }
    delay(1000);
  }
  return false;
}

// e) Mise à l'heure du RTC depuis le serveur NTP : retourne true si OK
// forceUpdate() attend au plus 1 s la réponse : le programme n'est pas bloqué
bool synchroniserNTP()
{
  if (!wifiOk || !ntpClient.forceUpdate())
  {
    Serial.println("Synchronisation NTP impossible");
    return false;
  }
  RTCTime maintenant((time_t)ntpClient.getEpochTime());
  RTC.setTime(maintenant);
  Serial.print("RTC synchronise : ");
  Serial.println(maintenant.toString());
  return true;
}

// d) Ecran d'accueil : version + date sur la ligne 1, adresse IP sur la ligne 2
void afficherAccueil()
{
  char ligne[21];
  RTCTime maintenant;
  RTC.getTime(maintenant);

  sprintf(ligne, "V%s  %02d/%02d/%04d", VERSION,
          maintenant.getDayOfMonth(),
          Month2int(maintenant.getMonth()),
          maintenant.getYear());
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(ligne);
  lcd.setCursor(0, 1);
  if (wifiOk)
  {
    lcd.print(WiFi.localIP());
  }
  else
  {
    lcd.print("WIFI deconnecte");
  }

  Serial.println(ligne);
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.localIP());
}

void afficherBargraphe()
{
  int nb = humidite / 10; // humidité 0-100 % -> 0-10 LEDs
  for (int i = 0; i < NB_LEDS; i++)
  {
    digitalWrite(PIN_BARGRAPH + i, i < nb ? HIGH : LOW);
  }
}

// Ligne 1 du LCD : date et heure lues dans le RTC
// (ou message d'erreur si le RTC n'a pas pu être synchronisé)
void afficherDate()
{
  char date[21];
  if (!ntpOk)
  {
    lcd.setCursor(0, 0);
    lcd.print("Pas synchro NTP ");
    return;
  }

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

  RTC.begin();

  // b) Initialisation du WIFI puis synchronisation NTP
  lcd.print("Connexion WIFI..");
  wifiOk = setup_wifi();
  if (wifiOk)
  {
    ntpClient.begin();
  }
  ntpOk = synchroniserNTP();

  // d) Ecran d'accueil pendant 3 s
  afficherAccueil();
  delay(3000);
  lcd.clear();
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
    // e) Nouvel essai de synchronisation NTP toutes les minutes en cas d'échec
    if (!ntpOk && ++cyclesSansNtp >= NTP_CYCLES_RELANCE)
    {
      cyclesSansNtp = 0;
      ntpOk = synchroniserNTP();
    }
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