# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mon_ihm.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(440, 640)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grpBroker = QGroupBox(self.centralwidget)
        self.grpBroker.setObjectName(u"grpBroker")
        self.grpBroker.setStyleSheet(u"")
        self.gridBroker = QGridLayout(self.grpBroker)
        self.gridBroker.setObjectName(u"gridBroker")
        self.lblPort = QLabel(self.grpBroker)
        self.lblPort.setObjectName(u"lblPort")
        font = QFont()
        font.setBold(True)
        self.lblPort.setFont(font)
        self.lblPort.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridBroker.addWidget(self.lblPort, 1, 1, 1, 1)

        self.btnDisconnect = QPushButton(self.grpBroker)
        self.btnDisconnect.setObjectName(u"btnDisconnect")
        self.btnDisconnect.setMinimumSize(QSize(0, 36))

        self.gridBroker.addWidget(self.btnDisconnect, 4, 2, 1, 1)

        self.lnePort = QLineEdit(self.grpBroker)
        self.lnePort.setObjectName(u"lnePort")

        self.gridBroker.addWidget(self.lnePort, 1, 2, 1, 1)

        self.btnConnect = QPushButton(self.grpBroker)
        self.btnConnect.setObjectName(u"btnConnect")
        self.btnConnect.setMinimumSize(QSize(0, 36))

        self.gridBroker.addWidget(self.btnConnect, 4, 1, 1, 1)

        self.lneUser = QLineEdit(self.grpBroker)
        self.lneUser.setObjectName(u"lneUser")

        self.gridBroker.addWidget(self.lneUser, 2, 2, 1, 1)

        self.lblUser = QLabel(self.grpBroker)
        self.lblUser.setObjectName(u"lblUser")
        self.lblUser.setFont(font)
        self.lblUser.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridBroker.addWidget(self.lblUser, 2, 1, 1, 1)

        self.lblIPAddress = QLabel(self.grpBroker)
        self.lblIPAddress.setObjectName(u"lblIPAddress")
        self.lblIPAddress.setFont(font)
        self.lblIPAddress.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridBroker.addWidget(self.lblIPAddress, 0, 1, 1, 1)

        self.lblPassword = QLabel(self.grpBroker)
        self.lblPassword.setObjectName(u"lblPassword")
        self.lblPassword.setFont(font)
        self.lblPassword.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridBroker.addWidget(self.lblPassword, 3, 1, 1, 1)

        self.lneIPAddress = QLineEdit(self.grpBroker)
        self.lneIPAddress.setObjectName(u"lneIPAddress")

        self.gridBroker.addWidget(self.lneIPAddress, 0, 2, 1, 1)

        self.lnePassword = QLineEdit(self.grpBroker)
        self.lnePassword.setObjectName(u"lnePassword")
        self.lnePassword.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridBroker.addWidget(self.lnePassword, 3, 2, 1, 1)

        self.lblLogo = QLabel(self.grpBroker)
        self.lblLogo.setObjectName(u"lblLogo")
        self.lblLogo.setMinimumSize(QSize(180, 70))
        self.lblLogo.setMaximumSize(QSize(180, 70))
        self.lblLogo.setStyleSheet(u"background-color: white; color: #00a3c4; font-weight: bold; border: 1px solid #c0c0c0;")
        self.lblLogo.setPixmap(QPixmap(u"img/logo-noir.png"))
        self.lblLogo.setScaledContents(True)
        self.lblLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblLogo.setWordWrap(True)

        self.gridBroker.addWidget(self.lblLogo, 0, 0, 4, 1)


        self.verticalLayout.addWidget(self.grpBroker)

        self.grpData = QGroupBox(self.centralwidget)
        self.grpData.setObjectName(u"grpData")
        self.gridData = QGridLayout(self.grpData)
        self.gridData.setObjectName(u"gridData")
        self.lblDateTime = QLabel(self.grpData)
        self.lblDateTime.setObjectName(u"lblDateTime")
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(14)
        self.lblDateTime.setFont(font1)
        self.lblDateTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridData.addWidget(self.lblDateTime, 0, 0, 1, 4)

        self.lblTemperatureTitle = QLabel(self.grpData)
        self.lblTemperatureTitle.setObjectName(u"lblTemperatureTitle")
        self.lblTemperatureTitle.setFont(font)

        self.gridData.addWidget(self.lblTemperatureTitle, 1, 0, 1, 1)

        self.lblTemperature = QLabel(self.grpData)
        self.lblTemperature.setObjectName(u"lblTemperature")
        self.lblTemperature.setFont(font1)

        self.gridData.addWidget(self.lblTemperature, 1, 1, 1, 1)

        self.lblHumidityTitle = QLabel(self.grpData)
        self.lblHumidityTitle.setObjectName(u"lblHumidityTitle")
        self.lblHumidityTitle.setFont(font)

        self.gridData.addWidget(self.lblHumidityTitle, 1, 2, 1, 1)

        self.lblHumidity = QLabel(self.grpData)
        self.lblHumidity.setObjectName(u"lblHumidity")
        self.lblHumidity.setFont(font1)

        self.gridData.addWidget(self.lblHumidity, 1, 3, 1, 1)


        self.verticalLayout.addWidget(self.grpData)

        self.grpCommands = QGroupBox(self.centralwidget)
        self.grpCommands.setObjectName(u"grpCommands")
        self.gridCommands = QGridLayout(self.grpCommands)
        self.gridCommands.setObjectName(u"gridCommands")
        self.btnSynchroDateTime = QPushButton(self.grpCommands)
        self.btnSynchroDateTime.setObjectName(u"btnSynchroDateTime")
        self.btnSynchroDateTime.setMinimumSize(QSize(0, 40))

        self.gridCommands.addWidget(self.btnSynchroDateTime, 0, 0, 1, 2)

        self.btnStopMeasure = QPushButton(self.grpCommands)
        self.btnStopMeasure.setObjectName(u"btnStopMeasure")
        self.btnStopMeasure.setMinimumSize(QSize(0, 36))

        self.gridCommands.addWidget(self.btnStopMeasure, 1, 0, 1, 1)

        self.btnStartMeasure = QPushButton(self.grpCommands)
        self.btnStartMeasure.setObjectName(u"btnStartMeasure")
        self.btnStartMeasure.setMinimumSize(QSize(0, 36))

        self.gridCommands.addWidget(self.btnStartMeasure, 1, 1, 1, 1)

        self.btnSlowBlink = QPushButton(self.grpCommands)
        self.btnSlowBlink.setObjectName(u"btnSlowBlink")
        self.btnSlowBlink.setMinimumSize(QSize(0, 36))

        self.gridCommands.addWidget(self.btnSlowBlink, 2, 0, 1, 1)

        self.btnFastBlink = QPushButton(self.grpCommands)
        self.btnFastBlink.setObjectName(u"btnFastBlink")
        self.btnFastBlink.setMinimumSize(QSize(0, 36))

        self.gridCommands.addWidget(self.btnFastBlink, 2, 1, 1, 1)

        self.btnBlink = QPushButton(self.grpCommands)
        self.btnBlink.setObjectName(u"btnBlink")
        self.btnBlink.setMinimumSize(QSize(0, 36))

        self.gridCommands.addWidget(self.btnBlink, 3, 0, 1, 1)

        self.layoutBlinkPeriod = QHBoxLayout()
        self.layoutBlinkPeriod.setObjectName(u"layoutBlinkPeriod")
        self.lneBlinkPeriod = QLineEdit(self.grpCommands)
        self.lneBlinkPeriod.setObjectName(u"lneBlinkPeriod")
        self.lneBlinkPeriod.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.layoutBlinkPeriod.addWidget(self.lneBlinkPeriod)

        self.lblMs = QLabel(self.grpCommands)
        self.lblMs.setObjectName(u"lblMs")
        self.lblMs.setFont(font)

        self.layoutBlinkPeriod.addWidget(self.lblMs)


        self.gridCommands.addLayout(self.layoutBlinkPeriod, 3, 1, 1, 1)

        self.lblBargraph = QLabel(self.grpCommands)
        self.lblBargraph.setObjectName(u"lblBargraph")
        self.lblBargraph.setMinimumSize(QSize(0, 36))
        self.lblBargraph.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridCommands.addWidget(self.lblBargraph, 4, 0, 1, 1)

        self.lneBargraph = QLineEdit(self.grpCommands)
        self.lneBargraph.setObjectName(u"lneBargraph")

        self.gridCommands.addWidget(self.lneBargraph, 4, 1, 1, 1)

        self.gridCommands.setColumnStretch(0, 1)
        self.gridCommands.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.grpCommands)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 440, 33))
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        self.menuAide = QMenu(self.menubar)
        self.menuAide.setObjectName(u"menuAide")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.lneIPAddress, self.lnePort)
        QWidget.setTabOrder(self.lnePort, self.lneUser)
        QWidget.setTabOrder(self.lneUser, self.lnePassword)
        QWidget.setTabOrder(self.lnePassword, self.btnConnect)
        QWidget.setTabOrder(self.btnConnect, self.btnDisconnect)
        QWidget.setTabOrder(self.btnDisconnect, self.btnSynchroDateTime)
        QWidget.setTabOrder(self.btnSynchroDateTime, self.btnStopMeasure)
        QWidget.setTabOrder(self.btnStopMeasure, self.btnStartMeasure)
        QWidget.setTabOrder(self.btnStartMeasure, self.btnSlowBlink)
        QWidget.setTabOrder(self.btnSlowBlink, self.btnFastBlink)
        QWidget.setTabOrder(self.btnFastBlink, self.btnBlink)
        QWidget.setTabOrder(self.btnBlink, self.lneBlinkPeriod)
        QWidget.setTabOrder(self.lneBlinkPeriod, self.lneBargraph)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuAide.menuAction())
        self.menuFichier.addAction(self.actionQuit)
        self.menuAide.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mon capteur IDO via MQTT (c)2026 CERI SN - PPI", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"\u00c0 propos", None))
        self.grpBroker.setTitle(QCoreApplication.translate("MainWindow", u"Param\u00e8tres de communication du Broker MQTT", None))
        self.lblPort.setText(QCoreApplication.translate("MainWindow", u"Port :", None))
        self.btnDisconnect.setText(QCoreApplication.translate("MainWindow", u"D\u00e9connecter", None))
        self.lnePort.setText(QCoreApplication.translate("MainWindow", u"1883", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connecter", None))
        self.lblUser.setText(QCoreApplication.translate("MainWindow", u"Utilisateur :", None))
        self.lblIPAddress.setText(QCoreApplication.translate("MainWindow", u"Adresse IP :", None))
        self.lblPassword.setText(QCoreApplication.translate("MainWindow", u"Mot de passe :", None))
        self.lneIPAddress.setText(QCoreApplication.translate("MainWindow", u"192.168.1.1", None))
        self.lblLogo.setText("")
        self.grpData.setTitle(QCoreApplication.translate("MainWindow", u"Affichage des donn\u00e9es du capteur", None))
        self.lblDateTime.setText(QCoreApplication.translate("MainWindow", u"00/00/0000 00:00:00", None))
        self.lblTemperatureTitle.setText(QCoreApplication.translate("MainWindow", u"Temp\u00e9rature (en \u00b0C) :", None))
        self.lblTemperature.setText(QCoreApplication.translate("MainWindow", u"00.0", None))
        self.lblHumidityTitle.setText(QCoreApplication.translate("MainWindow", u"Humidit\u00e9 (en %) :", None))
        self.lblHumidity.setText(QCoreApplication.translate("MainWindow", u"00.0", None))
        self.grpCommands.setTitle(QCoreApplication.translate("MainWindow", u"Commandes", None))
        self.btnSynchroDateTime.setText(QCoreApplication.translate("MainWindow", u"Synchronisation de la date et heure du capteur (NTP)", None))
        self.btnStopMeasure.setText(QCoreApplication.translate("MainWindow", u"Arr\u00eater les mesures", None))
        self.btnStartMeasure.setText(QCoreApplication.translate("MainWindow", u"D\u00e9marrer les mesures", None))
        self.btnSlowBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement lent", None))
        self.btnFastBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement rapide", None))
        self.btnBlink.setText(QCoreApplication.translate("MainWindow", u"Clignotement personnalis\u00e9", None))
        self.lneBlinkPeriod.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.lblMs.setText(QCoreApplication.translate("MainWindow", u"ms", None))
        self.lblBargraph.setText(QCoreApplication.translate("MainWindow", u"Valeur du bargraphe (0 \u00e0 1023) :", None))
        self.lneBargraph.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Entr\u00e9e pour envoyer", None))
        self.menuFichier.setTitle(QCoreApplication.translate("MainWindow", u"Fichier", None))
        self.menuAide.setTitle(QCoreApplication.translate("MainWindow", u"Aide", None))
    # retranslateUi

