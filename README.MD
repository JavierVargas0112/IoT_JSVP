# IoT project – TempHumiX

School project for the IoT course at IMT Nord Europe (CERI Systèmes Numériques). We built a small temperature and humidity sensor, got it talking over WiFi with MQTT, and then wrote a desktop app in Python to watch it, send it commands and save the measurements.

It was done in three lab sessions, and each one builds on the previous one:

1. **Simulation** – design the sensor in SimulIDE with an Arduino UNO R3 (LEDs, bargraph, DHT22, I2C LCD, software clock).
2. **WiFi + MQTT** – port the code to the real box (Arduino UNO R4 WiFi), sync the clock with NTP, publish the readings and listen for commands over MQTT, then look at the packets in Wireshark.
3. **GUI (IHM)** – a PySide6 app that shows the live values, controls the sensor, archives everything in SQLite and plots it with Matplotlib.

The full write-up (in French) is in the lab report.

## How it works

The sensor and the PC never talk to each other directly. Everything goes through the Mosquitto broker on the lab's IoT network. The sensor publishes its readings and subscribes to command topics, and any MQTT client (MQTTX, our console scripts or the GUI) can do the opposite.

```
 TempHumiX (UNO R4)  ──WiFi──►  Mosquitto broker  ◄──  PC: console clients / GUI
   DHT22, LCD, RTC              192.168.1.1:1883          (paho-mqtt)
```

All topics start with `/iot/` and end with our station number, `44987`:

| Topic | Direction | Payload |
|---|---|---|
| `VERSION_44987` | sensor → broker | firmware version, e.g. `1.0` (only sent after command 10) |
| `TEMPERATURE_44987` | sensor → broker | °C with one decimal |
| `HUMIDITY_44987` | sensor → broker | % with one decimal |
| `GET_DATE_44987` | sensor → broker | `DD/MM/YYYY HH:MM:SS` from the RTC |
| `COMMAND_44987` | broker → sensor | `10` NTP sync, `20` start / `30` stop measuring, `40` slow / `50` fast blink, `60` custom blink |
| `BARGRAPH_44987` | broker → sensor | 0 to 1023 (mapped to 0–10 LEDs) |
| `BLINK_44987` | broker → sensor | blink period in ms, must be a multiple of 100 |

Payloads are plain text. We tried JSON from MQTTX once and `atoi()` turned it into 0, so don't do that.

To save bandwidth, the sensor only publishes T, H and the date when the temperature or humidity actually changes (compared to the tenth of a degree / percent).

## Repo layout

```
SIMULIDE/
  clignotement_led/   first circuit, blinking LED
  bargraphe/          LED chaser on the bargraph
  capteur_dht22/      DHT22 reading + two LEDs
  lcd_i2c/            "Hello World" on the I2C LCD
  lcd_i2c_dht22/      LCD + DHT22 together
  TempHumiX/          the real sensor firmware (see note below)
IHM/
  console_mqtt_lecture/   console client that subscribes and prints
  console_mqtt_ecriture/  console client with a command menu + receive thread
  ihm_mqtt_simple/        the PySide6 GUI (main.py), SQLite archive, plots
```

Heads up: `SIMULIDE/TempHumiX/TempHumiX.ino` started as the SimulIDE version and then became the UNO R4 firmware during lab 2, so the current file won't run in SimulIDE anymore. The `.hex` next to it is still the old simulated build. If you want the simulation code, check out commit `bdb9a99`.

## What you need

**Hardware:** Arduino UNO R4 WiFi, DHT22, Grove LCD RGB Backlight (16×2, I2C), a 10-LED bargraph and a "life" LED. The lab gives you this already wired in a box.

**Arduino libraries** (Library Manager in the Arduino IDE):
- `Grove - LCD RGB Backlight` (rgb_lcd)
- `DHT sensor library` by Adafruit
- `NTPClient`
- `ArduinoMqttClient`
- `WiFiS3` and `RTC` come with the UNO R4 board package

**For the simulation:** SimulIDE 1.1.0 and, for the LCD, the `LiquidCrystal AIP31068` library. The header is `LiquidCrystal_AIP31068_I2C.h`, not the name in the docs.

**Python side:** Python 3.12 (that's what the lab asks for; PyCharm first gave us 3.15 and we had to recreate the venv), then:

```bash
pip install paho-mqtt PySide6 matplotlib
```

## Setup

### Secrets

Passwords are not in the repo. You need to create two files yourself.

`SIMULIDE/TempHumiX/arduino_secrets.h`:

```cpp
#define SECRET_WIFI_SSID "your-ssid"
#define SECRET_WIFI_MDP  "your-wifi-password"
#define SECRET_MQTT_USER "your-mqtt-user"
#define SECRET_MQTT_MDP  "your-mqtt-password"
```

Careful with the Arduino IDE: if you create it as a new tab it may save it as `arduino_secrets.h.ino`. Rename it to `.h`.

`secrets_mqtt.py`, one copy in each folder under `IHM/` that you want to run:

```python
MQTT_USER = "your-mqtt-user"
MQTT_PASSWORD = "your-mqtt-password"
```

Both are listed in `.gitignore`, along with `.venv/`, `.idea/` and `*.db`.

### Network

Your PC has to be on the same network as the sensor, otherwise you won't reach the broker. On our setup:

| | |
|---|---|
| WiFi | `IoT IMT Nord Europe` (2.4 GHz only, the UNO R4 can't see the 5 GHz one) |
| MQTT broker | `192.168.1.1:1883`, no TLS |
| NTP server | `192.168.1.254` |

The NTP address in the lab sheet (`10.12.130.1`) didn't respond from the IoT network, which took us a while to figure out. Use the local one.

If you're not in the same lab, change `ID_PC`, `MQTT_BROKER` and `NTP_SERVEUR` at the top of the `.ino`, and `id_pc` in the Python files.

## Running it

**Sensor:** open `SIMULIDE/TempHumiX/TempHumiX.ino` in the Arduino IDE, select "Arduino UNO R4 WiFi", upload. The LCD shows the version and the IP for 3 seconds, then the date on line 1 and T/H on line 2. Serial monitor is at 9600 baud.

**Console clients** (from the `IHM` folder, with the venv active):

```bash
python console_mqtt_lecture/main.py
```
```bash
python console_mqtt_ecriture/main.py
```

The reader just prints what comes in. The writer has a menu (1–7 for commands, 8 to show the last values, Q to quit). They use different client IDs (`Client_44987` and `Client_E44987`) so you can run both at the same time. The broker kicks out one of them if two clients share an ID.

**GUI:** run it from inside its folder, otherwise the logo path breaks:

```bash
cd ihm_mqtt_simple
python main.py
```

Click *Connecter*, wait a couple of seconds and the values show up. The status bar tells you if the connection failed. *Fichier → Afficher les courbes* (Ctrl+G) opens the plot window, where you pick a start and end time and click *Charger les données*.

If you change the `.ui` files in Qt Designer, regenerate the Python:

```bash
pyside6-uic mon_ihm.ui -o mon_ihm.py
pyside6-uic graphe.ui -o graphe.py
```

## Data archive

Every time `GET_DATE` arrives (it's the last topic the sensor sends in each cycle), the GUI writes a row to `IOT.db`:

```sql
IOT_DATA (Id_capteur integer, Date text, Version text, Temperature real, Humidite real)
```

Dates are stored as `YYYY-MM-DD HH:MM:SS`. We first kept the French format, but SQLite compares dates as text, so `05/10` ends up "after" `04/11`. ISO format sorts properly and makes the `BETWEEN` query in the plot window work.

The database is opened inside the MQTT thread on purpose. sqlite3 won't let you use a connection from a different thread than the one that created it.

## Known issues / things we'd fix

- **No security.** MQTT runs on port 1883 without TLS, and Wireshark shows the username and password in clear text in the CONNECT packet. All users also share the same ACL, so anyone can publish on someone else's topics. We actually saw this happen: our plots showed two sets of values alternating on our topics, which means a second device was publishing with our station number.
- **Reconnection.** paho-mqtt reconnects on its own after a network drop, but our subscriptions are made once at startup and not in `on_connect`, so after a reconnect nothing comes in anymore. Moving the subscribes into `on_connect` would fix it.
- **RTC drift.** The UNO R4's clock drifts quite a lot (we saw it more than 2 minutes ahead). Sending command 10 resyncs it, but it should probably be done automatically every so often.
- **Not done:** the QoS / retain / wildcard tests from part 6.2.2, and the "challenge" (single `DATA_` topic with serialized values, subscribing to `/iot/#` to see every sensor in the room).

## Authors

Javier Santiago Vargas Parra, IMT Nord Europe, 2026.
Supervisor: Abdellah Bouchama.
Lab sheets by J.F. Béguin, A. Guilloteau, D. Juge-Hubert and A. Bouchama.
