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

    def publish_mqtt(self, topic, message, qos=0):
        self.client.publish(topic,message,qos)
        print(f"Publication : {message} on {topic}")

        return 0

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
        self.client.subscribe(topic, qos)
        self.client.on_message = on_message
        print(f"Waiting for topic : `{topic}`")

    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            self.client.loop_forever()
        else:
            self.client.loop(timeout=timeout)


