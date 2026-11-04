import sys

from PySide6.QtCore import QTimer, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QMainWindow

from client_mqtt import ClientMQTT

from thread_mqtt import ThreadMQTT
from mon_ihm import Ui_MainWindow
from secrets_mqtt import MQTT_USER, MQTT_PASSWORD

import _sqlite3
from dialogue_courbe import CourbeDialog

id_pc = 44987

topic_commande = f"/iot/COMMAND_{id_pc}"
topic_bargraphe = f"/iot/BARGRAPH_{id_pc}"
topic_periode = f"/iot/BLINK_{id_pc}"


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):


        super(MainWindow, self).__init__()
        self.setupUi(self)


        self.mqtt: ClientMQTT | None = None
        self.thread_mqtt: ThreadMQTT | None = None
        self.debug = True

        self.timer = QTimer()

        # Valores por defecto de los campos de usuario y contraseña
        self.lneUser.setText(MQTT_USER)
        self.lnePassword.setText(MQTT_PASSWORD)

        #  validadores
        octet = r"(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)" #numero de 0 a 255
        self.lneIPAddress.setValidator(QRegularExpressionValidator(QRegularExpression(rf"{octet}(\.{octet}){{3}}")))
        self.lnePort.setValidator(QRegularExpressionValidator(QRegularExpression(r"\d{1,5}")))
        self.lneBlinkPeriod.setValidator(QRegularExpressionValidator(QRegularExpression(r"[1-9]\d{0,2}00")))
        self.lneBargraph.setValidator(QRegularExpressionValidator(QRegularExpression(r"\d{1,3}|10[01]\d|102[0-3]")))

        self.timer.timeout.connect(self.display)
        self.btnConnect.clicked.connect(self.connectMQTT)
        self.btnDisconnect.clicked.connect(self.disconnectMQTT)
        self.btnSynchroDateTime.clicked.connect(self.synchroDateTime)
        self.btnStartMeasure.clicked.connect(self.startMeasure)
        self.btnStopMeasure.clicked.connect(self.stopMeasure)
        self.btnFastBlink.clicked.connect(self.fastBlink)
        self.btnSlowBlink.clicked.connect(self.slowBlink)
        self.btnBlink.clicked.connect(self.customBlink)
        self.lneBargraph.returnPressed.connect(self.setBargraph)
        self.actionQuit.triggered.connect(self.quit)
        self.actionGraph.triggered.connect(self.showGraph)

    def display(self):
        # Llamada cada 1000 ms por el timer
        # copiar self.mqtt.date_IdO, temperature, humidite en
        #       lblDateTime, lblTemperature, lblHumidity (con setText)
        if self.mqtt is None:
            return
        if self.mqtt.date_IdO:
            self.lblDateTime.setText(self.mqtt.date_IdO)
        if self.mqtt.temperature:
            self.lblTemperature.setText(f"{self.mqtt.temperature} °C")
        if self.mqtt.humidite:
            self.lblHumidity.setText(f"{self.mqtt.humidite} %")

    def connectMQTT(self):

        #COmprobaciones
        if self.mqtt is not None:
            self.statusbar.showMessage("Déjà connecté au broker MQTT")
            return
        if not (self.lneIPAddress.hasAcceptableInput() and self.lnePort.hasAcceptableInput()):
            self.statusbar.showMessage("Adresse IP ou port invalide")
            return

        #leer lneIPAddress, lnePort (int), lneUser, lnePassword
        broker = self.lneIPAddress.text()
        port = int(self.lnePort.text())
        username = self.lneUser.text()
        password = self.lnePassword.text()
        # crear self.mqtt  y connect_mqtt()

        self.mqtt = ClientMQTT(broker, port, f"Client_IHM{id_pc}",username,password)


        try:
            self.mqtt.connect_mqtt()
        except Exception as e:
            self.statusbar.showMessage(f"Erreur de connexion : {e}")
            self.mqtt = None
            return

        #crear self.thread_mqtt y start()

        self.thread_mqtt = ThreadMQTT(self.mqtt)
        self.thread_mqtt.start()

        self.timer.start(1000)
        self.statusbar.showMessage("Connection au broker MQTT OK")

    def disconnectMQTT(self):
        if self.mqtt is None:
            self.statusbar.showMessage("Pas connecté au broker MQTT")
            return
        self.timer.stop()
        self.thread_mqtt.stopthread()
        self.thread_mqtt.join()
        self.mqtt.disconnect_mqtt()
        self.mqtt = None
        self.thread_mqtt = None
        self.statusbar.showMessage("Déconnecté du broker MQTT")


    def envoyer(self, topic,message):
        if self.mqtt is None:
            self.statusbar.showMessage("Pas connecte au broker MQTT")
            return False
        self.mqtt.publish_mqtt(topic, message)
        return True

    def synchroDateTime(self):
        #publicar "10" en topic_commande
        if self.envoyer(topic_commande, "10"):
            self.statusbar.showMessage("Synchronisation NTO du capteur demandee")


    def startMeasure(self):
        # "20" y luego "50" (como la opción 2 de la consola)
        if self.envoyer(topic_commande, "20"):
            self.envoyer(topic_commande, "50")
            self.statusbar.showMessage("Demarrage des mesures")

    def stopMeasure(self):
        # "30" y luego "40"
        if self.envoyer(topic_commande, "30"):
            self.envoyer(topic_commande, "40")
            self.statusbar.showMessage("Arrte des mesures")

    def fastBlink(self):
        #"50"

        if self.envoyer(topic_commande, "50"):
            self.statusbar.showMessage("Clignotement rapide")

    def slowBlink(self):
        if self.envoyer(topic_commande, "40"):
            self.statusbar.showMessage("Clignotement lent")

    def customBlink(self):
        #leer lneBlinkPeriod, publicar en topic_periode, luego "60" en topic_commande
        if not self.lneBlinkPeriod.hasAcceptableInput():
            self.statusbar.showMessage("Periode invalide")
            return
        periode = self.lneBlinkPeriod.text()
        if self.envoyer(topic_periode, periode):
            self.envoyer(topic_commande, "60")
            self.statusbar.showMessage(f"Clignoment personnalise: {periode} ms")

    def setBargraph(self):
        # leer lneBargraph, comprobar 0..1023, publicar en topic_bargraphe
        valeur = self.lneBargraph.text()
        if self.envoyer(topic_bargraphe,valeur):
            self.statusbar.showMessage((f"baragraphe: {valeur}"))

    def quit(self):
        #si está conectado, desconectar; luego self.close()
        self.close()


    #Que hacer despues de cerrar la ventana
    def closeEvent(self, event):
        if self.mqtt is not None:
            self.disconnectMQTT()
        event.accept()

    def showGraph(self):
        dialog = CourbeDialog()
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())