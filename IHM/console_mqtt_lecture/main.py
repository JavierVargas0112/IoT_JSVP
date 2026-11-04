from client_mqtt import ClientMQTT
from secrets_mqtt import MQTT_USER, MQTT_PASSWORD

username = MQTT_USER
password = MQTT_PASSWORD


id_pc = 44987
broker = "192.168.1.1"
port = 1883


if __name__ == '__main__':
    print("Démarrage de l'application")
    print("==========================")
    print("Instanciation de votre ClientMQTT")
    mqtt =  ClientMQTT(broker, port, f"Client_{id_pc}", username, password)
    mqtt.connect_mqtt()

    print(f"Souscription aux données du capteur : 'Client_{id_pc}'")
    mqtt.subscribe_mqtt(f'/iot/VERSION_{id_pc}')
    mqtt.subscribe_mqtt(f'/iot/TEMPERATURE_{id_pc}')
    mqtt.subscribe_mqtt(f'/iot/HUMIDITY_{id_pc}')
    mqtt.subscribe_mqtt(f'/iot/GET_DATE_{id_pc}')

    # Attente des valeurs souscrites avec timeout=0
    mqtt.wait_mqtt()

    print("Fin de l'application")