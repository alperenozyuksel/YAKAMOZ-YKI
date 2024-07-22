import pickle
import struct
import cv2
from dronekit import connect, VehicleMode, LocationGlobalRelative
from PyQt5 import QtCore, QtGui, QtWidgets
import math
import time
import serial
import socket

class Ui_MainWindow(object):


    def __init__(self):
        """""
        HOST = '192.168.1.7'
        PORT = 8485
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        self.s.bind((HOST, PORT))
        print('Socket bind complete')
        self.s.listen(10)
        print('Socket now listening')

        self.conn, self.addr = self.s.accept()
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(self.payload_size))
        """
        self.cap = cv2.VideoCapture(0)


        self.connection_string = 'COM13'
        self.iha = connect(self.connection_string, baud=9600, wait_ready=False)

        # QTimer oluştur
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda:self.yukseklik())
        self.timer.timeout.connect(lambda:self.hava_hizi())
        self.timer.timeout.connect(lambda:self.gps_hizi())
        self.timer.timeout.connect(lambda:self.gaz_yuzdesi())
        self.timer.timeout.connect(lambda:self.yatay_denge())
        self.timer.timeout.connect(lambda:self.boylam_denge())
        self.timer.timeout.connect(lambda:self.yon_dengesi())
        self.timer.timeout.connect(lambda:self.goruntu_goster())


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
        self.pushButton_9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 4, 2, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 4, 0, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 4, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 3, 2, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 3, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
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
        self.pushButton_9.setText(_translate("MainWindow", "LOITER"))
        self.pushButton_7.setText(_translate("MainWindow", "FBWB"))
        self.pushButton_8.setText(_translate("MainWindow", "RTL"))
        self.pushButton_2.setText(_translate("MainWindow", "ARM"))
        self.pushButton_4.setText(_translate("MainWindow", "FBWA"))
        self.pushButton_6.setText(_translate("MainWindow", "AUTOTUNE"))
        self.pushButton_5.setText(_translate("MainWindow", "AUTO"))
        self.pushButton_3.setText(_translate("MainWindow", "MANUEL"))
        self.pushButton.setText(_translate("MainWindow", "DISARM"))
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

    def gps_hizi(self):
        gps_speed = self.iha.groundspeed
        self.gpsspeed_value.setText(str(gps_speed))

    def gaz_yuzdesi(self):
        throttle= self.iha.channels['3']
        self.throttle_value.setText(str(throttle))

    def yatay_denge(self):
        roll= self.iha.attitude.roll
        self.roll_value.setText(str(roll))

    def boylam_denge(self):
        pitch = self.iha.attitude.pitch
        self.pitch_value.setText(str(pitch))

    def yon_dengesi(self):
        yaw= self.iha.attitude.yaw
        self.yaw_value.setText(str(yaw))

    def goruntu_goster(self):
        """"
        while len(self.data) < self.payload_size:
            self.data += self.conn.recv(4096)
            if not self.data:
                cv2.destroyAllWindows()
                self.conn, self.addr = self.s.accept()
                continue
        # receive image row data form client socket
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(self.data) < msg_size:
            self.data += self.conn.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        # unpack image using pickle
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # self.camera.set.....   Chatgptdeki kod eklenecek
        """
        ret,frame= self.cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame= cv2.flip(frame,1)
        # Convert to QImage
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
        # Set the image to the QLabel
        self.camera.setPixmap(QtGui.QPixmap.fromImage(image))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
