import sqlite3
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg

from PySide6.QtCore import QDateTime
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QDialog, QGraphicsPixmapItem, QMessageBox

from graphe import Ui_GraphWindow

id_pc = 44987

database_name = "IOT.db"
table_name = "IOT_DATA"


class CourbeDialog(QDialog, Ui_GraphWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Escena vacía desde el principio (así "Effacer" no falla si se pulsa antes que "Charger")
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        # Intervalo por defecto: la última hora
        dte = QDateTime.currentDateTime()
        dts = dte.addSecs(-3600)
        self.dteStartTime.setDateTime(dts)
        self.dteEndTime.setDateTime(dte)

        self.btnLoadData.clicked.connect(self.afficher_courbe)
        self.btnClearData.clicked.connect(self.effacer_courbe)

    def figure_to_pixmap(self, fig):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        width, height = canvas.get_width_height()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format.Format_RGBA8888)
        return QPixmap.fromImage(image.copy())

    def afficher_courbe(self):
        debut = self.dteStartTime.text()
        fin = self.dteEndTime.text()

        #   abrir la base, ejecutar el SELECT y leer las filas
        conn = sqlite3.connect(database_name)

        #   SELECT Date, Temperature, Humidite FROM {table_name}
        #   WHERE Id_capteur = ? AND Date BETWEEN ? AND ? ORDER BY Date ASC
        #   con los parámetros (id_pc, debut, fin); después conn.close()
        cur = conn.cursor()
        cur.execute(f"SELECT Date, Temperature, Humidite FROM {table_name} "
                    "WHERE Id_capteur = ? AND Date BETWEEN ? AND ? ORDER BY Date ASC",
                    (id_pc, debut, fin))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            # avisar de que no hay datos en ese intervalo (por ejemplo con self.setWindowTitle o un QMessageBox)

                self.scene.clear()
                QMessageBox.information(self, "Aucune donnee",
                                        f"Aucune mesure du capteur {id_pc} entre\n{debut} et {fin}.")
                return
        # Convertir el texto de la base en fechas reales para que el eje X sea temporal
        date_x = [datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S") for r in rows]
        temp_y = [r[1] for r in rows]
        humi_y = [r[2] for r in rows]

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        # dibujar las dos curvas con ax.plot(..., label="Température (°C)") y "Humidité (%)"
        ax.plot(date_x, temp_y, marker="o", markersize=3, label="Température (°C)")
        ax.plot(date_x, humi_y, marker="+", markersize=5, label="Humidité (%)")
        #  título, etiquetas de los ejes, rejilla y leyenda (ax.legend())

        ax.set_title(f"Données capteur IdO {id_pc}")
        ax.set_xlabel("Heure")
        ax.set_ylabel("Valeurs")
        ax.grid(True)
        ax.legend()
        fig.tight_layout()

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        fig.autofmt_xdate()

        pixmap = self.figure_to_pixmap(fig)
        plt.close(fig)                    # liberar la figura

        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(pixmap))

    def effacer_courbe(self):
        self.scene.clear()