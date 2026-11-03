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

#include "arduino_secrets.h"

#include <ArduinoMqttClient.h>

#define VERSION "1.0"

#define PIN_LED_VIE 2
#define PIN_BARGRAPH 3 // bargraphe sur les broches 3 à 12
#define NB_LEDS 10
#define PIN_DHT A0

#define WIFI_SSID SECRET_WIFI_SSID
#define WIFI_MDP SECRET_WIFI_MDP  

#define WIFI_NB_ESSAIS 3

// Serveur NTP de IMT Nord Europe
#define NTP_SERVEUR "192.168.1.254" 
#define FUSEAU_HORAIRE 3600   // UTC+2 (heure d'été), 3600 en heure d'hiver
#define NTP_CYCLES_RELANCE 30 // nouvel essai NTP toutes les 30 x 2 s = 1 min

//MQTT
#define ID_PC "44987"
#define MQTT_BROKER "192.168.1.1"
#define MQTT_PORT 1883
#define MQTT_ID "IDO_Client_" ID_PC
#define MQTT_CYCLES_RELANCE 5


// Topics publiés (paragraphe 3.2)
#define TOPIC_VERSION "/iot/VERSION_" ID_PC
#define TOPIC_TEMPERATURE "/iot/TEMPERATURE_" ID_PC
#define TOPIC_HUMIDITE "/iot/HUMIDITY_" ID_PC
#define TOPIC_DATE "/iot/GET_DATE_" ID_PC


//TOPIC Souscrit
#define TOPIC_COMMANDE "/iot/COMMAND_" ID_PC
#define TOPIC_BARGRAPHE "/iot/BARGRAPH_" ID_PC
#define TOPIC_BLINK "/iot/BLINK_" ID_PC

// Codes commande
#define CMD_MISE_A_L_HEURE 10
#define CMD_DEMARRAGE_MESURE 20
#define CMD_ARRET_MESURE 30
#define CMD_CLIGNOTEMENT_LENT 40
#define CMD_CLIGNOTEMENT_RAPIDE 50
#define CMD_CLIGNOTEMENT_PERSO 60


// Périodes de la LED de vie (ms)
#define PERIODE_LED_NORMALE 500 // 2 Hz
#define PERIODE_LED_LENTE 2000
#define PERIODE_LED_RAPIDE 200

#define TICK_MS 100      // base de temps de la boucle
#define TICKS_PAR_ETAT 5 // 5 x 100 ms = 500 ms par état



rgb_lcd lcd;
DHT dht(PIN_DHT, DHT22);
WiFiUDP ntpUDP;
NTPClient ntpClient(ntpUDP, NTP_SERVEUR, FUSEAU_HORAIRE);

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);


// Etats de la machine d'état (1 état = 500 ms, cycle complet = 2 s)
enum Etat
{
  LECTURE_CAPTEUR, // t = 0 ms    : lecture DHT22
  ATTENTE_1,       // t = 500 ms
  ATTENTE_2,       // t = 1000 ms
  ATTENTE_3        // t = 1500 ms
};

Etat etat = LECTURE_CAPTEUR;

unsigned int tick = 0;
unsigned long tempsLed = 0;             // temps écoulé pour le clignotement (ms)
int periodeLed = PERIODE_LED_NORMALE;   // période courante de la LED de vie
int periodePerso = PERIODE_LED_NORMALE; // période reçue sur BLINK_
bool mesureActive = true;               // commandes 20 / 30
bool demandeMiseALHeure = false;        // commande 10
int valeurBargraphe = -1;               // 0-1023 reçu sur BARGRAPH_, -1 = humidité

float temperature = 0;
float humidite = 0;
bool wifiOk = false;
bool ntpOk = false;
int cyclesSansNtp = 0;
int cyclesSansMqtt = 0;



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


// Connexion au broker MQTT : retourne 0 si OK, code erreur MQTT sinon
int setup_mqtt()
{
  if (!wifiOk)
  {
    return MQTT_CONNECTION_REFUSED;
  }

  mqttClient.setId(MQTT_ID);
  mqttClient.setUsernamePassword(SECRET_MQTT_USER, SECRET_MQTT_MDP);
  Serial.print("Connexion au broker MQTT en tant que ");
  Serial.println(MQTT_ID);

  if (!mqttClient.connect(MQTT_BROKER, MQTT_PORT))
  {
    int erreur = mqttClient.connectError();
    Serial.print("Echec connexion MQTT, code erreur : ");
    Serial.println(erreur);
    return erreur;
  }
  Serial.println("Connecte au broker MQTT");

  // Souscription aux 3 topics (refaite à chaque reconnexion)
  mqttClient.subscribe(TOPIC_COMMANDE);
  mqttClient.subscribe(TOPIC_BARGRAPHE);
  mqttClient.subscribe(TOPIC_BLINK);
  return 0;
}

void traiterCommande(int code)
{
  switch (code)
  {
  case CMD_MISE_A_L_HEURE:
    demandeMiseALHeure = true; // traitée dans loop() (hors du callback)
    break;
  case CMD_DEMARRAGE_MESURE:
    mesureActive = true;
    break;
  case CMD_ARRET_MESURE:
    mesureActive = false;
    lcd.setCursor(0, 1);
    lcd.print("Mesure arretee  ");
    break;
  case CMD_CLIGNOTEMENT_LENT:
    periodeLed = PERIODE_LED_LENTE;
    break;
  case CMD_CLIGNOTEMENT_RAPIDE:
    periodeLed = PERIODE_LED_RAPIDE;
    break;
  case CMD_CLIGNOTEMENT_PERSO:
    periodeLed = periodePerso;
    break;
  default:
    Serial.println("Code commande inconnu");
    break;
  }
}


void onMqttMessage(int tailleMessage)
{
  char message[16];
  int i = 0;

  // Acquisition du topic et du message
  String topic = mqttClient.messageTopic();
  while (mqttClient.available())
  {
    char c = mqttClient.read();
    if (i < (int)sizeof(message) - 1)
    {
      message[i++] = c;
    }
  }
  message[i] = '\0';

  // Conversion du message en entier
  int valeur = atoi(message);
  Serial.print("Recu ");
  Serial.print(topic);
  Serial.print(" : ");
  Serial.println(valeur);

  if (topic.indexOf("COMMAND") >= 0)
  {
    traiterCommande(valeur);
  }
  else if (topic.indexOf("BARGRAPH") >= 0)
  {
    valeurBargraphe = constrain(valeur, 0, 1023);
    afficherBargraphe();
  }
  else if (topic.indexOf("BLINK") >= 0)
  {
    // La période doit être un multiple de 100 ms
    if (valeur >= TICK_MS && valeur % TICK_MS == 0)
    {
      periodePerso = valeur;
    }
    else
    {
      Serial.println("Periode refusee : multiple de 100 ms attendu");
    }
  }
}

void formaterDate(char *texte)
{
   RTCTime maintenant;
  RTC.getTime(maintenant);
  sprintf(texte, "%02d/%02d/%04d %02d:%02d:%02d",
          maintenant.getDayOfMonth(),
          Month2int(maintenant.getMonth()),
          maintenant.getYear(),
          maintenant.getHour(),
          maintenant.getMinutes(),
          maintenant.getSeconds());
}



void publierMessage(const char *topic, const char *valeur)
{
  mqttClient.beginMessage(topic);
  mqttClient.print(valeur);
  mqttClient.endMessage();
}

void publierDonnees()
{
  char texte[24];
  if (!mqttClient.connected())
  {
    return;
  }

  publierMessage(TOPIC_VERSION, VERSION);
  dtostrf(temperature, 0, 1, texte); 

  publierMessage(TOPIC_TEMPERATURE, texte);
  dtostrf(humidite, 0, 1, texte);
  publierMessage(TOPIC_HUMIDITE, texte);

  formaterDate(texte);

  publierMessage(TOPIC_DATE, texte);
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

  int nb;
  if (valeurBargraphe >= 0)
  {
    nb = map(valeurBargraphe, 0, 1023, 0, NB_LEDS); // valeur reçue par MQTT
  }
  else
  {
    nb = humidite / 10; // humidité 0-100 % -> 0-10 LEDs
  }

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
  setup_mqtt();
  mqttClient.onMessage(onMqttMessage);

  // d) Ecran d'accueil pendant 3 s
  afficherAccueil();
  delay(3000);
  lcd.clear();
}

void loop()
{
  mqttClient.poll();
    // LED de vie : allumée la première moitié de la période (pas de 100 ms)
  digitalWrite(PIN_LED_VIE, (tempsLed % periodeLed) < (unsigned long)periodeLed / 2 ? HIGH : LOW);
  tempsLed += TICK_MS;

  // Commande 10 : forcer la mise à l'heure
  if (demandeMiseALHeure)
  {
    demandeMiseALHeure = false;
    ntpOk = synchroniserNTP();
  }

  // La machine d'état n'avance qu'une fois tous les 5 ticks (500 ms)
  tick++;
  if (tick < TICKS_PAR_ETAT)
  {
    delay(TICK_MS);
    return;
  }
  tick = 0;

  // Date/heure rafraîchie à chaque tour (500 ms) pour ne sauter aucune seconde
  afficherDate();

  switch (etat)
  {
  case LECTURE_CAPTEUR:

  if (mesureActive)
  {
      lireCapteur();
      publierDonnees();
  }
    

     if (!mqttClient.connected() && ++cyclesSansMqtt >= MQTT_CYCLES_RELANCE)
    {
      cyclesSansMqtt = 0;
      setup_mqtt();
    }
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
  }

  delay(TICK_MS);
}