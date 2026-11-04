# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'graphe.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDateTimeEdit, QDialog,
    QDialogButtonBox, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_GraphWindow(object):
    def setupUi(self, GraphWindow):
        if not GraphWindow.objectName():
            GraphWindow.setObjectName(u"GraphWindow")
        GraphWindow.resize(660, 600)
        self.verticalLayout = QVBoxLayout(GraphWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grpInterval = QGroupBox(GraphWindow)
        self.grpInterval.setObjectName(u"grpInterval")
        self.gridInterval = QGridLayout(self.grpInterval)
        self.gridInterval.setObjectName(u"gridInterval")
        self.lblStartTime = QLabel(self.grpInterval)
        self.lblStartTime.setObjectName(u"lblStartTime")

        self.gridInterval.addWidget(self.lblStartTime, 0, 0, 1, 1)

        self.dteStartTime = QDateTimeEdit(self.grpInterval)
        self.dteStartTime.setObjectName(u"dteStartTime")
        self.dteStartTime.setCalendarPopup(True)

        self.gridInterval.addWidget(self.dteStartTime, 0, 1, 1, 1)

        self.lblEndTime = QLabel(self.grpInterval)
        self.lblEndTime.setObjectName(u"lblEndTime")

        self.gridInterval.addWidget(self.lblEndTime, 1, 0, 1, 1)

        self.dteEndTime = QDateTimeEdit(self.grpInterval)
        self.dteEndTime.setObjectName(u"dteEndTime")
        self.dteEndTime.setCalendarPopup(True)

        self.gridInterval.addWidget(self.dteEndTime, 1, 1, 1, 1)

        self.gridInterval.setColumnStretch(0, 1)
        self.gridInterval.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.grpInterval)

        self.graphicsView = QGraphicsView(GraphWindow)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(620, 420))

        self.verticalLayout.addWidget(self.graphicsView)

        self.layoutButtons = QHBoxLayout()
        self.layoutButtons.setObjectName(u"layoutButtons")
        self.btnClearData = QPushButton(GraphWindow)
        self.btnClearData.setObjectName(u"btnClearData")

        self.layoutButtons.addWidget(self.btnClearData)

        self.btnLoadData = QPushButton(GraphWindow)
        self.btnLoadData.setObjectName(u"btnLoadData")

        self.layoutButtons.addWidget(self.btnLoadData)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutButtons.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(GraphWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.layoutButtons.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.layoutButtons)

        QWidget.setTabOrder(self.dteStartTime, self.dteEndTime)
        QWidget.setTabOrder(self.dteEndTime, self.btnLoadData)
        QWidget.setTabOrder(self.btnLoadData, self.btnClearData)
        QWidget.setTabOrder(self.btnClearData, self.graphicsView)

        self.retranslateUi(GraphWindow)
        self.buttonBox.accepted.connect(GraphWindow.accept)
        self.buttonBox.rejected.connect(GraphWindow.reject)

        QMetaObject.connectSlotsByName(GraphWindow)
    # setupUi

    def retranslateUi(self, GraphWindow):
        GraphWindow.setWindowTitle(QCoreApplication.translate("GraphWindow", u"Graphique des donn\u00e9es de temp\u00e9rature et d'humidit\u00e9", None))
        self.grpInterval.setTitle(QCoreApplication.translate("GraphWindow", u"Param\u00e8tres de l'intervalle temporel", None))
        self.lblStartTime.setText(QCoreApplication.translate("GraphWindow", u"Date et heure de d\u00e9but", None))
        self.dteStartTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.lblEndTime.setText(QCoreApplication.translate("GraphWindow", u"Date et heure de fin", None))
        self.dteEndTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"yyyy-MM-dd HH:mm:ss", None))
        self.btnClearData.setText(QCoreApplication.translate("GraphWindow", u"Effacer les courbes", None))
        self.btnLoadData.setText(QCoreApplication.translate("GraphWindow", u"Charger les donn\u00e9es", None))
    # retranslateUi

