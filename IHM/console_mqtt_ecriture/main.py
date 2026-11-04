from client_mqtt import ClientMQTT
from secrets_mqtt import MQTT_USER, MQTT_PASSWORD

from thread_mqtt import ThreadMQTT

username = MQTT_USER
password = MQTT_PASSWORD

id_pc = 44987
broker = "192.168.1.1"
port = 1883

topic_commande = f"/iot/COMMAND_{id_pc}"
topic_bargraphe = f"/iot/BARGRAPH_{id_pc}"
topic_periode = f"/iot/BLINK_{id_pc}"


if __name__ == '__main__':
    print("Démarrage de l'application")
    print("==========================")
    print("Instanciation de votre ClientMQTT")
    mqtt = ClientMQTT(broker, port, f"Client_E{id_pc}", username, password)
    mqtt.connect_mqtt()
    thread_mqtt = ThreadMQTT(mqtt)
    thread_mqtt.start()

    car = ' '
    while car.upper() != 'Q':
        print("Console capteur IdO")
        print("-------------------")
        print("1 - Mise à l'heure du capteur")
        print("2 - Démarrage des mesures")
        print("3 - Arrêt des mesures")
        print("4 - Clignotement lent")
        print("5 - Clignotement rapide")
        print("6 - Clignotement personnalisé")
        print("7 - Ecriture du bargraphe")
        print("8 - Afficher les mesures")
        print("Q - Quitter")
        car = input("Votre choix : ")
        match car.upper():
            case '1':
                mqtt.publish_mqtt(topic_commande, "10")
                print(f"Synchronisation du capteur : {id_pc}")

            case '2':
                mqtt.publish_mqtt(topic_commande, "20")
                print(f"Démarrage des mesures sur le capteur : {id_pc}")
                mqtt.publish_mqtt(topic_commande, "50")

            case '3':
                mqtt.publish_mqtt(topic_commande, "30")
                print(f"Arrêt des mesures sur le capteur : {id_pc}")
                mqtt.publish_mqtt(topic_commande, "40")

            case '4':
                mqtt.publish_mqtt(topic_commande, "40")
                print(f"Clignotement lent de la led de vie du capteur : {id_pc}")

            case '5':
                mqtt.publish_mqtt(topic_commande, "50")
                print(f"Clignotement rapide de la led de vie du capteur : {id_pc}")

            case '6':
                periode = input("Période du clignotement (en ms) : ")
                if periode.isdigit():
                    mqtt.publish_mqtt(topic_periode, periode)
                    mqtt.publish_mqtt(topic_commande, "60")
                    print(f"Clignotement personnalisé à {periode} ms sur le capteur : {id_pc}")
                else:
                    print("Valeur invalide")

            case '7':
                valeur = input("Choisir la valeur à écrire sur le bargraphe (0 à 1023) : ")
                if valeur.isdigit() and 0 <= int(valeur) <= 1023:
                    mqtt.publish_mqtt(topic_bargraphe, valeur)
                    print(f"Ecriture de la valeur {valeur} sur le bargraphe du capteur : {id_pc}")
                else:
                    print("Valeur invalide (0 à 1023)")
            case '8':
                print(f"Version : {mqtt.version}  Date : {mqtt.date_IdO}")
                print(f"Température : {mqtt.temperature} °C  Humidité : {mqtt.humidite} %")
            case 'Q':
                print("Arrêt du client MQTT")
                thread_mqtt.stopthread()
                thread_mqtt.join()
                mqtt.disconnect_mqtt()

            case _:
                print("Choix inconnu")

    print("Fin de l'application")