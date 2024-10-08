from dronekit import connect, VehicleMode, LocationGlobalRelative
from PyQt5 import QtCore, QtGui, QtWidgets
import math
import time

class Ui_MainWindow(object):

    def __init__(self):
        self.connection_string = "127.0.0.1:14550"
        self.iha = connect(self.connection_string, wait_ready=False)

        # QTimer oluştur
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda:self.yukseklik())
        self.timer.timeout.connect(lambda:self.hava_hizi())
        self.timer.timeout.connect(lambda:self.gaz())


        self.timer.start(1000)  # 1000 milisaniyede bir (1 saniye) güncelle
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1420, 904)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 30, 196, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.altitude_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.altitude_text.setObjectName("altitude_text")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.altitude_text)
        self.altitude_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.altitude_value.setObjectName("altitude_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.altitude_value)
        self.distance_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.distance_text.setObjectName("distance_text")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.distance_text)
        self.distance_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.distance_value.setObjectName("distance_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.distance_value)
        self.airspeed_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.airspeed_text.setObjectName("airspeed_text")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.airspeed_text)
        self.airspeed_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.airspeed_value.setObjectName("airspeed_value")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.airspeed_value)
        self.gpsspeed_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.gpsspeed_text.setObjectName("gpsspeed_text")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.gpsspeed_text)
        self.gpsspeed_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.gpsspeed_value.setObjectName("gpsspeed_value")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.gpsspeed_value)
        self.throttle_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.throttle_text.setObjectName("throttle_text")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.throttle_text)
        self.roll_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.roll_text.setObjectName("roll_text")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.roll_text)
        self.roll_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.roll_value.setObjectName("roll_value")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.roll_value)
        self.pitch_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.pitch_text.setObjectName("pitch_text")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.pitch_text)
        self.pitch_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.pitch_value.setObjectName("pitch_value")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.pitch_value)
        self.yaw_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.yaw_text.setObjectName("yaw_text")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.yaw_text)
        self.yaw_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.yaw_value.setObjectName("yaw_value")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.yaw_value)
        self.wind_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.wind_text.setObjectName("wind_text")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.wind_text)
        self.wind_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.wind_value.setObjectName("wind_value")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.wind_value)
        self.throttle_value = QtWidgets.QLabel(self.formLayoutWidget)
        self.throttle_value.setObjectName("throttle_value")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.throttle_value)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 520, 401, 301))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.loiter_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.loiter_button.setObjectName("loiter_button")
        self.gridLayout.addWidget(self.loiter_button, 4, 2, 1, 1)
        self.fbwb_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.fbwb_button.setObjectName("fbwb_button")
        self.gridLayout.addWidget(self.fbwb_button, 4, 0, 1, 1)
        self.rtl_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.rtl_button.setObjectName("rtl_button")
        self.gridLayout.addWidget(self.rtl_button, 4, 1, 1, 1)
        self.arm_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.arm_button.setObjectName("arm_button")
        self.gridLayout.addWidget(self.arm_button, 0, 0, 1, 1)
        self.fbwa_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.fbwa_button.setObjectName("fbwa_button")
        self.gridLayout.addWidget(self.fbwa_button, 3, 0, 1, 1)
        self.autotune_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.autotune_button.setObjectName("autotune_button")
        self.gridLayout.addWidget(self.autotune_button, 3, 2, 1, 1)
        self.auto_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.auto_button.setObjectName("auto_button")
        self.gridLayout.addWidget(self.auto_button, 3, 1, 1, 1)
        self.manuel_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.manuel_button.setObjectName("manuel_button")
        self.gridLayout.addWidget(self.manuel_button, 0, 2, 1, 1)
        self.disarm_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.disarm_button.setObjectName("disarm_button")
        self.gridLayout.addWidget(self.disarm_button, 0, 1, 1, 1)
        self.camera = QtWidgets.QLabel(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(660, 490, 391, 331))
        self.camera.setObjectName("camera")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1420, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.arm_button.clicked.connect(self.arm_butonu)
        self.manuel_button.clicked.connect(self.manuel_butonu)
        self.fbwa_button.clicked.connect(self.fbwa_butonu)
        self.auto_button.clicked.connect(self.auto_butonu)
        self.autotune_button.clicked.connect(self.autotune_butonu)
        self.fbwb_button.clicked.connect(self.fbwb_butonu)
        self.rtl_button.clicked.connect(self.rtl_butonu)
        self.loiter_button.clicked.connect(self.loiter_butonu)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.altitude_text.setText(_translate("MainWindow", "YÜKSEKLİK : "))
        self.altitude_value.setText(_translate("MainWindow", "TextLabel"))
        self.distance_text.setText(_translate("MainWindow", "UZAKLIK : "))
        self.distance_value.setText(_translate("MainWindow", "TextLabel"))
        self.airspeed_text.setText(_translate("MainWindow", "HAVA HIZI :"))
        self.airspeed_value.setText(_translate("MainWindow", "TextLabel"))
        self.gpsspeed_text.setText(_translate("MainWindow", "GPS HIZI :"))
        self.gpsspeed_value.setText(_translate("MainWindow", "TextLabel"))
        self.throttle_text.setText(_translate("MainWindow", "GAZ :"))
        self.roll_text.setText(_translate("MainWindow", "YATAY DENGE :"))
        self.roll_value.setText(_translate("MainWindow", "TextLabel"))
        self.pitch_text.setText(_translate("MainWindow", "BOYLAM DENGE :"))
        self.pitch_value.setText(_translate("MainWindow", "TextLabel"))
        self.yaw_text.setText(_translate("MainWindow", "YÖN DENGESİ :"))
        self.yaw_value.setText(_translate("MainWindow", "TextLabel"))
        self.wind_text.setText(_translate("MainWindow", "RÜZGAR :"))
        self.wind_value.setText(_translate("MainWindow", "TextLabel"))
        self.throttle_value.setText(_translate("MainWindow", "TextLabel"))
        self.loiter_button.setText(_translate("MainWindow", "LOITER"))
        self.fbwb_button.setText(_translate("MainWindow", "FBWB"))
        self.rtl_button.setText(_translate("MainWindow", "RTL"))
        self.arm_button.setText(_translate("MainWindow", "ARM"))
        self.fbwa_button.setText(_translate("MainWindow", "FBWA"))
        self.autotune_button.setText(_translate("MainWindow", "AUTOTUNE"))
        self.auto_button.setText(_translate("MainWindow", "AUTO"))
        self.manuel_button.setText(_translate("MainWindow", "MANUEL"))
        self.disarm_button.setText(_translate("MainWindow", "DISARM"))
        self.camera.setText(_translate("MainWindow", "TextLabel"))

    def yukseklik(self):
        altitude1 = self.iha.location.global_relative_frame.alt
        self.altitude_value.setText(str(altitude1))

    #def uzaklik(self):
     #   distance1 = self.iha.location.global_relative_frame.distance
      #  self.distance_value.setText(str(distance1))

    def hava_hizi(self):
        airspeed1 = self.iha.airspeed
        self.airspeed_value.setText(str(airspeed1))

    def gaz(self):
        throttle1 = self.iha.channels['3']
        self.throttle_value.setText(str(throttle1))







    def arm_butonu(self):
        self.iha.arm()
    def manuel_butonu(self):
        self.iha.mode = VehicleMode("MANUAL")

    def fbwa_butonu(self):
        self.iha.mode = VehicleMode("FBWA")

    def auto_butonu(self):
        self.iha.mode = VehicleMode("AUTO")

    def autotune_butonu(self):
        self.iha.mode = VehicleMode("AUTOTUNE")

    def fbwb_butonu(self):
        self.iha.mode = VehicleMode("FBWB")

    def rtl_butonu(self):
        self.iha.mode = VehicleMode("RTL")

    def loiter_butonu(self):
        self.iha.mode = VehicleMode("LOITER")











if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
