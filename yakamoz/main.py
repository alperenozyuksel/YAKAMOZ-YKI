from PyQt5 import QtCore, QtGui, QtWidgets
from dronekit import connect, VehicleMode
import time
import ButtonManager
import iha

#connection_string="127.0.0.1:14550"
#iha=connect(connection_string,wait_ready=False)

iha1 = iha.iha("127.0.0.1:14550")
buttonManager= ButtonManager.ButtonManager(iha1)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1442, 645)
        MainWindow.setStyleSheet("background-color: rgb(218, 218, 218);\n""background-color: rgb(0, 0, 0);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 20, 461, 131))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../../Downloads/WhatsApp Image 2024-04-28 at 14.40.14.jpeg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.KAMERA_2 = QtWidgets.QLabel(self.centralwidget)
        self.KAMERA_2.setGeometry(QtCore.QRect(10, 160, 461, 211))
        self.KAMERA_2.setText("")
        self.KAMERA_2.setPixmap(QtGui.QPixmap("../../../Downloads/Ekran görüntüsü 2024-05-05 134556.png"))
        self.KAMERA_2.setScaledContents(True)
        self.KAMERA_2.setObjectName("KAMERA_2")

        self.KONTROLPANELI_2 = QtWidgets.QListWidget(self.centralwidget)
        self.KONTROLPANELI_2.setGeometry(QtCore.QRect(10, 380, 461, 191))
        self.KONTROLPANELI_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.KONTROLPANELI_2.setObjectName("KONTROLPANELI_2")

        self.KAMERA = QtWidgets.QTextEdit(self.centralwidget)
        self.KAMERA.setGeometry(QtCore.QRect(10, 160, 113, 22))
        self.KAMERA.setStyleSheet("background-color: rgb(206, 206, 206);")
        self.KAMERA.setObjectName("KAMERA")

        self.KONTROLPANELI = QtWidgets.QTextEdit(self.centralwidget)
        self.KONTROLPANELI.setGeometry(QtCore.QRect(10, 380, 113, 22))
        self.KONTROLPANELI.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.KONTROLPANELI.setObjectName("KONTROLPANELI")

        self.ZAMAN_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.ZAMAN_2.setGeometry(QtCore.QRect(10, 20, 201, 131))
        self.ZAMAN_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ZAMAN_2.setPlainText("")
        self.ZAMAN_2.setObjectName("ZAMAN_2")

        self.UCUSBAGLANTISI_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.UCUSBAGLANTISI_2.setGeometry(QtCore.QRect(690, 20, 221, 131))
        self.UCUSBAGLANTISI_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UCUSBAGLANTISI_2.setObjectName("UCUSBAGLANTISI_2")

        self.KILITLENME_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.KILITLENME_2.setGeometry(QtCore.QRect(480, 380, 431, 191))
        self.KILITLENME_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.KILITLENME_2.setObjectName("KILITLENME_2")

        self.ZAMAN = QtWidgets.QTextEdit(self.centralwidget)
        self.ZAMAN.setGeometry(QtCore.QRect(10, 20, 113, 22))
        self.ZAMAN.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.ZAMAN.setObjectName("ZAMAN")

        self.UCUSBAGLANTISI = QtWidgets.QLineEdit(self.centralwidget)
        self.UCUSBAGLANTISI.setGeometry(QtCore.QRect(690, 20, 113, 22))
        self.UCUSBAGLANTISI.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.UCUSBAGLANTISI.setObjectName("UCUSBAGLANTISI")

        self.KILITLENME = QtWidgets.QTextEdit(self.centralwidget)
        self.KILITLENME.setGeometry(QtCore.QRect(480, 380, 113, 22))
        self.KILITLENME.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.KILITLENME.setObjectName("KILITLENME")

        self.UCUSSURESI = QtWidgets.QTextEdit(self.centralwidget)
        self.UCUSSURESI.setGeometry(QtCore.QRect(10, 100, 131, 22))
        self.UCUSSURESI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.UCUSSURESI.setObjectName("UCUSSURESI")

        self.PORT = QtWidgets.QTextEdit(self.centralwidget)
        self.PORT.setGeometry(QtCore.QRect(780, 60, 81, 22))
        self.PORT.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.PORT.setText("")
        self.PORT.setObjectName("PORT")

        self.BAUD = QtWidgets.QTextEdit(self.centralwidget)
        self.BAUD.setGeometry(QtCore.QRect(780, 80, 81, 22))
        self.BAUD.setStyleSheet("color: rgb(255, 255, 255);\n""background-color: rgb(255, 255, 255);")
        self.BAUD.setObjectName("BAUD")

        self.KILITLENMEDURUMU = QtWidgets.QTextEdit(self.centralwidget)
        self.KILITLENMEDURUMU.setGeometry(QtCore.QRect(640, 450, 113, 22))
        self.KILITLENMEDURUMU.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.KILITLENMEDURUMU.setObjectName("KILITLENMEDURUMU")

        self.KILITLENMESAYISI = QtWidgets.QTextEdit(self.centralwidget)
        self.KILITLENMESAYISI.setGeometry(QtCore.QRect(640, 480, 113, 22))
        self.KILITLENMESAYISI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.KILITLENMESAYISI.setObjectName("KILITLENMESAYISI")

        self.KILITLENMESURESI = QtWidgets.QTextEdit(self.centralwidget)
        self.KILITLENMESURESI.setGeometry(QtCore.QRect(640, 510, 113, 22))
        self.KILITLENMESURESI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.KILITLENMESURESI.setObjectName("KILITLENMESURESI")

        self.ROLLACISI = QtWidgets.QTextEdit(self.centralwidget)
        self.ROLLACISI.setGeometry(QtCore.QRect(40, 420, 121, 22))
        self.ROLLACISI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ROLLACISI.setObjectName("ROLLACISI")

        self.PITCHACISI = QtWidgets.QTextEdit(self.centralwidget)
        self.PITCHACISI.setGeometry(QtCore.QRect(40, 450, 121, 22))
        self.PITCHACISI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.PITCHACISI.setObjectName("PITCHACISI")

        self.YAWACISI = QtWidgets.QTextEdit(self.centralwidget)
        self.YAWACISI.setGeometry(QtCore.QRect(40, 480, 121, 22))
        self.YAWACISI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.YAWACISI.setObjectName("YAWACISI")

        self.ARACHIZI = QtWidgets.QTextEdit(self.centralwidget)
        self.ARACHIZI.setGeometry(QtCore.QRect(170, 420, 121, 22))
        self.ARACHIZI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ARACHIZI.setObjectName("ARACHIZI")

        self.HAVAHIZI = QtWidgets.QTextEdit(self.centralwidget)
        self.HAVAHIZI.setGeometry(QtCore.QRect(170, 450, 121, 22))
        self.HAVAHIZI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.HAVAHIZI.setObjectName("HAVAHIZI")

        self.YERHIZI = QtWidgets.QTextEdit(self.centralwidget)
        self.YERHIZI.setGeometry(QtCore.QRect(170, 480, 121, 22))
        self.YERHIZI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.YERHIZI.setObjectName("YERHIZI")

        self.BATARYADURUMU = QtWidgets.QTextEdit(self.centralwidget)
        self.BATARYADURUMU.setGeometry(QtCore.QRect(300, 420, 131, 22))
        self.BATARYADURUMU.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.BATARYADURUMU.setObjectName("BATARYADURUMU")

        self.ARACYUKSEKLIGI = QtWidgets.QTextEdit(self.centralwidget)
        self.ARACYUKSEKLIGI.setGeometry(QtCore.QRect(300, 450, 131, 22))
        self.ARACYUKSEKLIGI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ARACYUKSEKLIGI.setObjectName("ARACYUKSEKLIGI")

        self.MODDURUMU = QtWidgets.QTextEdit(self.centralwidget)
        self.MODDURUMU.setGeometry(QtCore.QRect(300, 480, 131, 22))
        self.MODDURUMU.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.MODDURUMU.setObjectName("MODDURUMU")

        self.SAAT = QtWidgets.QTextEdit(self.centralwidget)
        self.SAAT.setGeometry(QtCore.QRect(10, 80, 131, 22))
        self.SAAT.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SAAT.setObjectName("SAAT")

        self.TARIH = QtWidgets.QTextEdit(self.centralwidget)
        self.TARIH.setGeometry(QtCore.QRect(10, 60, 131, 22))
        self.TARIH.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.TARIH.setObjectName("TARIH")

        self.lineEdit_24 = QtWidgets.QTextEdit(self.centralwidget)
        self.lineEdit_24.setGeometry(QtCore.QRect(20, 510, 91, 22))
        self.lineEdit_24.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_24.setObjectName("lineEdit_24")

        self.FBWA = QtWidgets.QPushButton(self.centralwidget)
        self.FBWA.setGeometry(QtCore.QRect(120, 510, 71, 28))
        self.FBWA.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FBWA.setObjectName("FBWA")

        self.FBWB = QtWidgets.QPushButton(self.centralwidget)
        self.FBWB.setGeometry(QtCore.QRect(120, 540, 71, 28))
        self.FBWB.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.FBWB.setObjectName("FBWB")

        self.MANUEL = QtWidgets.QPushButton(self.centralwidget)
        self.MANUEL.setGeometry(QtCore.QRect(200, 510, 71, 28))
        self.MANUEL.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.MANUEL.setObjectName("MANUEL")

        self.AUTO = QtWidgets.QPushButton(self.centralwidget)
        self.AUTO.setGeometry(QtCore.QRect(200, 540, 71, 28))
        self.AUTO.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.AUTO.setObjectName("AUTO")

        self.RTL = QtWidgets.QPushButton(self.centralwidget)
        self.RTL.setGeometry(QtCore.QRect(280, 510, 71, 28))
        self.RTL.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.RTL.setObjectName("RTL")

        self.BAGLAN = QtWidgets.QPushButton(self.centralwidget)
        self.BAGLAN.setGeometry(QtCore.QRect(700, 110, 51, 28))
        self.BAGLAN.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.BAGLAN.setObjectName("BAGLAN")

        self.KES = QtWidgets.QPushButton(self.centralwidget)
        self.KES.setGeometry(QtCore.QRect(850, 110, 51, 28))
        self.KES.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.KES.setObjectName("KES")

        self.DISARMED = QtWidgets.QPushButton(self.centralwidget)
        self.DISARMED.setGeometry(QtCore.QRect(800, 500, 93, 28))
        self.DISARMED.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.DISARMED.setObjectName("DISARMED")

        self.ARMED = QtWidgets.QPushButton(self.centralwidget)
        self.ARMED.setGeometry(QtCore.QRect(800, 450, 93, 28))
        self.ARMED.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ARMED.setObjectName("ARMED")

        self.HUD_2 = QtWidgets.QLabel(self.centralwidget)
        self.HUD_2.setGeometry(QtCore.QRect(480, 160, 211, 211))
        self.HUD_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.HUD_2.setText("")
        self.HUD_2.setPixmap(QtGui.QPixmap("../../Resimler/Ekran Görüntüleri/Ekran görüntüsü 2024-05-04 152255.png"))
        self.HUD_2.setScaledContents(True)
        self.HUD_2.setObjectName("HUD_2")

        self.HUD = QtWidgets.QTextEdit(self.centralwidget)
        self.HUD.setGeometry(QtCore.QRect(480, 160, 113, 22))
        self.HUD.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.HUD.setObjectName("HUD")

        self.HARITA_2 = QtWidgets.QLabel(self.centralwidget)
        self.HARITA_2.setGeometry(QtCore.QRect(690, 160, 221, 211))
        self.HARITA_2.setText("")
        self.HARITA_2.setPixmap(QtGui.QPixmap("../../Resimler/Ekran Görüntüleri/Ekran görüntüsü 2024-05-04 152320.png"))
        self.HARITA_2.setScaledContents(True)
        self.HARITA_2.setObjectName("HARITA_2")

        self.HARITA = QtWidgets.QTextEdit(self.centralwidget)
        self.HARITA.setGeometry(QtCore.QRect(690, 160, 113, 22))
        self.HARITA.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.HARITA.setObjectName("HARITA")

        self.ITDALASI = QtWidgets.QPushButton(self.centralwidget)
        self.ITDALASI.setGeometry(QtCore.QRect(360, 510, 81, 28))
        self.ITDALASI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ITDALASI.setObjectName("ITDALASI")

        self.KAMIKAZE = QtWidgets.QPushButton(self.centralwidget)
        self.KAMIKAZE.setGeometry(QtCore.QRect(360, 540, 81, 28))
        self.KAMIKAZE.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.KAMIKAZE.setObjectName("KAMIKAZE")

        self.AUTOTUNE = QtWidgets.QPushButton(self.centralwidget)
        self.AUTOTUNE.setGeometry(QtCore.QRect(280, 540, 71, 28))
        self.AUTOTUNE.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.AUTOTUNE.setObjectName("AUTOTUNE")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1442, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.BAGLAN.clicked.connect(self.BAGLAN_butonu)
        self.ARMED.clicked.connect((self.ARMED_butonu))
        self.DISARMED.clicked.connect(self.DISARMED_butonu)
        self.FBWA.clicked.connect(self.FBWA_butonu)
        self.FBWB.clicked.connect(self.FBWB_butonu)
        self.RTL.clicked.connect(self.RTL_butonu)
        self.MANUEL.clicked.connect(self.MANUEL_butonu)
        self.AUTO.clicked.connect(self.AUTO_butonu)





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.KONTROLPANELI_2.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>pıjıojıo</p></body></html>"))
        self.KAMERA.setText(_translate("MainWindow", "KAMERA"))
        self.KONTROLPANELI.setText(_translate("MainWindow", "KONTROL PANELİ"))
        self.UCUSBAGLANTISI_2.setPlainText(_translate("MainWindow", "\n"
"\n"
"          PORT:\n"
"          BAUD:\n"
""))
        self.KILITLENME_2.setPlainText(_translate("MainWindow", "  \n"
"\n"
"\n"
"\n"
"    KİLİTLENME DURUMU:\n"
"  \n"
"    KİLİTLENME SAYISI:\n"
"\n"
"    KİLİTLENME SÜRESİ:"))
        self.ZAMAN.setText(_translate("MainWindow", "ZAMAN"))
        self.UCUSBAGLANTISI.setText(_translate("MainWindow", "UÇUŞ BAĞLANTISI"))
        self.KILITLENME.setText(_translate("MainWindow", "KİLİTLENME"))
        self.UCUSSURESI.setText(_translate("MainWindow", "Uçuş süresi:12dk"))
        self.BAUD.setText(_translate("MainWindow", "Baud:"))
        self.KILITLENMEDURUMU.setText(_translate("MainWindow", "YOK"))
        self.KILITLENMESAYISI.setText(_translate("MainWindow", "0"))
        self.KILITLENMESURESI.setText(_translate("MainWindow", "0"))
        self.ROLLACISI.setText(_translate("MainWindow", "Roll açısı:0.18"))
        self.PITCHACISI.setText(_translate("MainWindow", "Pitch açısı:-1.14"))
        self.YAWACISI.setText(_translate("MainWindow", "Yaw açısı:0.02"))
        self.ARACHIZI.setText(_translate("MainWindow", "Araç hızı:14m/s"))
        self.HAVAHIZI.setText(_translate("MainWindow", "Hava hızı:10m/s"))
        self.YERHIZI.setText(_translate("MainWindow", "Yer Hızı:9m/s"))
        self.BATARYADURUMU.setText(_translate("MainWindow", "Batarya Durumu:48"))
        self.ARACYUKSEKLIGI.setText(_translate("MainWindow", "Araç Yüksekliği:0.86"))
        self.MODDURUMU.setText(_translate("MainWindow", "Mod Durumu:AUTO"))
        self.SAAT.setText(_translate("MainWindow", "Saat:16.47"))
        self.TARIH.setText(_translate("MainWindow", "Tarih:13.04.2024"))
        self.lineEdit_24.setText(_translate("MainWindow", "Mod değiştir:"))
        self.FBWA.setText(_translate("MainWindow", "FBWA"))
        self.FBWB.setText(_translate("MainWindow", "FBWB"))
        self.MANUEL.setText(_translate("MainWindow", "MANUEL"))
        self.AUTO.setText(_translate("MainWindow", "AUTO"))
        self.RTL.setText(_translate("MainWindow", "RTL"))
        self.BAGLAN.setText(_translate("MainWindow", "BAĞLAN"))
        self.KES.setText(_translate("MainWindow", "KES"))
        self.DISARMED.setText(_translate("MainWindow", "DİSARMED"))
        self.ARMED.setText(_translate("MainWindow", "ARMED"))
        self.HUD.setText(_translate("MainWindow", "HUD"))
        self.HARITA.setText(_translate("MainWindow", "HARİTA"))
        self.ITDALASI.setText(_translate("MainWindow", "İT DALAŞI"))
        self.KAMIKAZE.setText(_translate("MainWindow", "KAMİKAZE"))
        self.AUTOTUNE.setText(_translate("MainWindow", "AUTOTUNE"))


    def BAGLAN_butonu(self):
       buttonManager.BAGLAN_butonu()

    def ARMED_butonu(self):
        buttonManager.ARMED_butonu()

    def DISARMED_butonu(self):
        buttonManager.DISARMED_butonu()

    def FBWA_butonu(self):
        buttonManager.FBWA_butonu()

    def FBWB_butonu(self):
        buttonManager.FBWB_butonu()

    def RTL_butonu(self):
        buttonManager.RTL_butonu()

    def MANUEL_butonu(self):
        buttonManager.MANUEL_butonu()

    def AUTO_butonu(self):
        buttonManager.AUTO_butonu()

    def ROOL_acisi(self):
        self.ROLLACISI.setText(self,buttonManager.ROOL_acisi())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())