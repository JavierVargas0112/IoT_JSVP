from threading import Thread

id_pc = 44987

topic_version = f"/iot/VERSION_{id_pc}"
topic_temperature = f"/iot/TEMPERATURE_{id_pc}"
topic_humidite = f"/iot/HUMIDITY_{id_pc}"
topic_datetime = f"/iot/GET_DATE_{id_pc}"

class ThreadMQTT(Thread):
    def __init__(self, client_mqtt):
        Thread.__init__(self)
        self.mqtt = client_mqtt
        self.stop = False

    def run(self):

        self.mqtt.connect_sqlite()
        try:
            self.mqtt.subscribe_mqtt(topic_version)
            self.mqtt.subscribe_mqtt(topic_temperature)
            self.mqtt.subscribe_mqtt(topic_humidite)
            self.mqtt.subscribe_mqtt(topic_datetime)
            while not self.stop:
                self.mqtt.wait_mqtt(timeout=1.0)
        finally:
            self.mqtt.disconnect_sqlite()


    def stopthread(self):
        self.stop = True