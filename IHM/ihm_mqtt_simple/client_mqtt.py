from datetime import datetime
import sqlite3

from paho.mqtt import client as mqtt_client

class ClientMQTT:
    def __init__(self, ip_address, port, client_id, username, password):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, self.client_id)
        self.version = ""
        self.temperature = ""
        self.humidite = ""
        self.date_IdO = ""

        self.conn = None
        self.tablename = None

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc, properties):
            if rc.is_failure:
                print(f"Failed to connect: {rc}")
            else:
                print(f"Connected to MQTT broker: {self.ip_address} {self.port}")

        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect
        self.client.connect(self.ip_address, self.port,60)
        return self.client

    def disconnect_mqtt(self):
        return  self.client.disconnect()

    def connect_sqlite(self):
        self.conn = sqlite3.connect("IOT.db")
        self.tablename = "IOT_DATA"
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {self.tablename} "
                          "(Id_capteur integer, Date text, Version text, Temperature real, Humidite real)")
        self.conn.commit()
        print(f"Base SQLite ouverte ")

    def disconnect_sqlite(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            print("Base SQLite fermée")


    def publish_mqtt(self, topic, message, qos=0):
        self.client.publish(topic,message,qos)
        print(f"Publication : {message} on {topic}")

        return 0


    def archiver(self, id_capteur):
        if self.conn is None or not self.temperature or not self.humidite:
            return
        date_iso = datetime.strptime(self.date_IdO, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(f"INSERT INTO {self.tablename} VALUES (?,?,?,?,?)", (id_capteur, date_iso, self.version, float(self.temperature), float(self.humidite)))
        self.conn.commit()
        print(f"Archivé : {id_capteur} {date_iso} {self.temperature} °C {self.humidite} %")

    def subscribe_mqtt(self, topic, qos= 0):
        def on_message(client,userdata, msg):
            if "VERSION_" in msg.topic:
                self.version = msg.payload.decode()
            elif "TEMPERATURE_" in msg.topic:
                self.temperature = msg.payload.decode()
            elif "HUMIDITY_" in msg.topic:
                self.humidite = msg.payload.decode()
            elif "GET_DATE_" in msg.topic:
                self.date_IdO = msg.payload.decode()
                self.archiver(int(msg.topic[-5:]))
        self.client.subscribe(topic, qos)
        self.client.on_message = on_message
        print(f"Waiting for topic : `{topic}`")

    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            self.client.loop_forever()
        else:
            self.client.loop(timeout=timeout)


