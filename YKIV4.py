import datetime
import math
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QTimer
from pymavlink import mavutil

# Global MAVLink connection
connection_string = "127.0.0.1:14550"
mavlink_connection = mavutil.mavlink_connection(connection_string)

class HorizonIndicator(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.altitude = 0.0
        self.battery_voltage = 0.0
        self.battery_current = 0.0
        self.battery_percent = 0.0

        # MAVLink connection
        self.master = mavlink_connection

        # Timer to periodically update data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_indicator)
        self.timer.start(50)  # 50 ms interval

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing
        self.drawHorizon(qp)
        self.drawText(qp)
        self.drawRectangle(qp)
        self.drawGyroLines(qp)

    def drawHorizon(self, qp):
        center_x = self.width() // 2
        center_y = self.height() // 2

        pitch_offset = (self.pitch / 90.0) * (self.height() / 2)

        # Draw the sky
        qp.save()
        qp.setBrush(QColor(0, 102, 204))  # Blue color
        qp.translate(0, pitch_offset)
        qp.drawRect(0, -self.height(), self.width(), center_y + self.height())
        qp.restore()

        # Draw the ground
        qp.save()
        qp.setBrush(QColor(255, 140, 45))  # Orange color
        qp.translate(0, pitch_offset)
        qp.drawRect(0, center_y, self.width(), self.height() - center_y + self.height())
        qp.restore()

        # Draw pitch lines and labels
        qp.save()
        qp.translate(center_x, center_y + pitch_offset)
        qp.rotate(-self.roll)

        qp.setPen(QPen(QColor(255, 255, 0), 2, Qt.SolidLine))  # Yellow color

        for p in range(-30, 31, 10):
            if p == 0:
                continue
            y = (p / 50.0) * (self.height() / 2) * 1.1
            qp.drawLine(-55, -int(y), 55, -int(y))
            qp.drawText(60, -int(y + 5), str(p))
            qp.drawText(-85, -int(y + 5), str(p))

        qp.restore()

    def drawText(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Arial', 15))

        # Bottom-left text
        text_x = 10
        text_y_start = self.height() - 120
        line_height = 20

        qp.drawText(text_x, text_y_start, f'Roll: {self.roll:.2f}')
        qp.drawText(text_x, text_y_start + line_height, f'Pitch: {self.pitch:.2f}')
        qp.drawText(text_x, text_y_start + 2 * line_height, f'Yaw: {self.yaw:.2f}')
        qp.drawText(text_x, text_y_start + 3 * line_height, f'Altitude: {self.altitude:.2f}')

        # Top-right text for battery
        text_x = self.width() - 200
        text_y_start = 20

        qp.drawText(text_x, text_y_start, f'Voltage: {self.battery_voltage:.2f} V')
        qp.drawText(text_x, text_y_start + line_height, f'Current: {self.battery_current:.2f} A')
        qp.drawText(text_x, text_y_start + 2 * line_height, f'Percent: {self.battery_percent:.2f} %')

    def drawRectangle(self, qp):
        # Rectangle for the gyroscope display
        margin = 0.40
        margin_x = (1 - margin) / 2
        rect_x = int(self.width() * margin_x)
        rect_width = int(self.width() * margin)

        margin_y = 0.05
        rect_y = int(self.height() * margin_y)
        rect_height = int(self.height() * (1 - 2 * margin_y))

        radius = int(self.width() * 0.10)

        qp.setPen(QPen(QColor(255, 255, 255), 2, Qt.SolidLine))
        qp.setBrush(QColor(0, 0, 0, 0))

        qp.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, radius, radius)

    def drawGyroLines(self, qp):
        center_x = self.width() // 2
        center_y = self.height() // 2

        line_length = 25

        qp.setPen(QPen(QColor(0, 245, 0), 2, Qt.SolidLine))

        qp.drawLine(center_x, center_y, center_x + line_length, center_y + line_length)
        qp.drawLine(center_x, center_y, center_x - line_length, center_y + line_length)

    def update_indicator(self):
        if not self.master:
            print('MAVLink connection not established.')
            return

        try:
            msg = self.master.recv_match(type='ATTITUDE', blocking=True)
            if msg:
                self.pitch = msg.pitch * 57.2958
                self.roll = msg.roll * 57.2958
                self.yaw = msg.yaw * 57.2958

            msg_alt = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg_alt:
                self.altitude = msg_alt.relative_alt / 1000.0

            msg_batt = self.master.recv_match(type='BATTERY_STATUS', blocking=True)
            if msg_batt:
                self.battery_voltage = msg_batt.voltages[1] / 1000.0
                self.battery_current = msg_batt.current_battery / 100.0
                self.battery_percent = msg_batt.battery_remaining

            print(f"Pitch: {self.pitch}, Roll: {self.roll}, Yaw: {self.yaw}")  # Debug output
            self.update()  # Refresh the display
        except Exception as e:
            print(f'Error updating indicator: {e}')


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.iha = mavlink_connection

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.yukseklik())
        self.timer.timeout.connect(lambda: self.hava_hizi())
        self.timer.timeout.connect(lambda: self.gps_hizi())
        self.timer.timeout.connect(lambda: self.gps_sayisi())
        self.timer.timeout.connect(lambda: self.roll_acisi())
        self.timer.timeout.connect(lambda: self.pitch_acisi())
        self.timer.timeout.connect(lambda: self.yaw_acisi())
        self.timer.timeout.connect(lambda: self.batarya_durumu())
        self.timer.timeout.connect(lambda: self.gaz())
        self.timer.timeout.connect(lambda: self.saat())
        self.timer.timeout.connect(lambda: self.tarih())
        self.timer.timeout.connect(lambda: self.arm())
        self.timer.start(50)  # Adjusted timer interval

        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1413, 893)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.camera = QtWidgets.QLabel(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(580, 180, 341, 341))
        self.camera.setObjectName("camera")

        # Embed the HorizonIndicator in the main window
        self.gyroscope = HorizonIndicator(self.centralwidget)
        self.gyroscope.setGeometry(QtCore.QRect(930, 480, 461, 371))
        self.gyroscope.setObjectName("gyroscope")

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(590, 540, 291, 271))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.loiter_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.loiter_value.setObjectName("loiter_value")
        self.gridLayout.addWidget(self.loiter_value, 2, 0, 1, 1)
        self.rtl_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.rtl_value.setObjectName("rtl_value")
        self.gridLayout.addWidget(self.rtl_value, 2, 1, 1, 1)
        self.disarm_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.disarm_value.setObjectName("disarm_value")
        self.gridLayout.addWidget(self.disarm_value, 0, 1, 1, 1)
        self.arm_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.arm_value.setObjectName("arm_value")
        self.gridLayout.addWidget(self.arm_value, 0, 0, 1, 1)
        self.manual_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.manual_value.setObjectName("manual_value")
        self.gridLayout.addWidget(self.manual_value, 0, 2, 1, 1)
        self.autotune_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.autotune_value.setObjectName("autotune_value")
        self.gridLayout.addWidget(self.autotune_value, 2, 2, 1, 1)
        self.fbwa_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.fbwa_value.setObjectName("fbwa_value")
        self.gridLayout.addWidget(self.fbwa_value, 1, 0, 1, 1)
        self.fbwb_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.fbwb_value.setObjectName("fbwb_value")
        self.gridLayout.addWidget(self.fbwb_value, 1, 1, 1, 1)
        self.auto_value = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.auto_value.setObjectName("auto_value")
        self.gridLayout.addWidget(self.auto_value, 1, 2, 1, 1)
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(1230, 10, 160, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.ip_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.ip_text.setObjectName("ip_text")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ip_text)
        self.ip_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.ip_value.setObjectName("ip_value")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ip_value)
        self.baud_text = QtWidgets.QLabel(self.formLayoutWidget)
        self.baud_text.setObjectName("baud_text")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.baud_text)
        self.baud_value = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.baud_value.setObjectName("baud_value")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.baud_value)
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(1230, 80, 161, 61))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.tarih_text = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.tarih_text.setObjectName("tarih_text")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tarih_text)
        self.saat_text = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.saat_text.setObjectName("saat_text")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.saat_text)
        self.tarih_value = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.tarih_value.setObjectName("tarih_value")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tarih_value)
        self.saat_value = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.saat_value.setObjectName("saat_value")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.saat_value)
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(20, 20, 171, 226))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.altitude_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.altitude_text.setObjectName("altitude_text")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.altitude_text)
        self.airspeed_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.airspeed_text.setObjectName("airspeed_text")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.airspeed_text)
        self.airspeed_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.airspeed_value.setObjectName("airspeed_value")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.airspeed_value)
        self.gpsspeed_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.gpsspeed_text.setObjectName("gpsspeed_text")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.gpsspeed_text)
        self.gpsspeed_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.gpsspeed_value.setObjectName("gpsspeed_value")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.gpsspeed_value)
        self.distance_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.distance_text.setObjectName("distance_text")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.distance_text)
        self.distance_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.distance_value.setObjectName("distance_value")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.distance_value)
        self.roll_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.roll_text.setObjectName("roll_text")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.roll_text)
        self.roll_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.roll_value.setObjectName("roll_value")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.roll_value)
        self.pitch_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.pitch_text.setObjectName("pitch_text")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.pitch_text)
        self.pitch_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.pitch_value.setObjectName("pitch_value")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.pitch_value)
        self.yaw_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.yaw_text.setObjectName("yaw_text")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.yaw_text)
        self.yaw_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.yaw_value.setObjectName("yaw_value")
        self.formLayout_3.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.yaw_value)
        self.throttle_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.throttle_text.setObjectName("throttle_text")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.throttle_text)
        self.throttle_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.throttle_value.setObjectName("throttle_value")
        self.formLayout_3.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.throttle_value)
        self.gps_text = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.gps_text.setObjectName("gps_text")
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.gps_text)
        self.gps_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.gps_value.setObjectName("gps_value")
        self.formLayout_3.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.gps_value)
        self.altitude_value = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.altitude_value.setObjectName("altitude_value")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.altitude_value)
        self.formLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(200, 20, 296, 141))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.battery_text = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.battery_text.setFont(font)
        self.battery_text.setObjectName("battery_text")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.battery_text)
        self.battery_value = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setBold(True)
        font.setWeight(75)
        self.battery_value.setFont(font)
        self.battery_value.setObjectName("battery_value")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.battery_value)
        self.telemetry_text = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.telemetry_text.setFont(font)
        self.telemetry_text.setObjectName("telemetry_text")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.telemetry_text)
        self.telemetry_value = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setBold(True)
        font.setWeight(75)
        self.telemetry_value.setFont(font)
        self.telemetry_value.setObjectName("telemetry_value")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.telemetry_value)
        self.arm_text = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.arm_text.setFont(font)
        self.arm_text.setObjectName("arm_text")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.arm_text)
        self.arm_value_2 = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.arm_value_2.setFont(font)
        self.arm_value_2.setObjectName("arm_value_2")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.arm_value_2)
        self.mode_text = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.mode_text.setFont(font)
        self.mode_text.setObjectName("mode_text")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.mode_text)
        self.mode_value = QtWidgets.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.mode_value.setFont(font)
        self.mode_value.setObjectName("mode_value")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.mode_value)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1413, 22))
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
        self.camera.setText(_translate("MainWindow", "Camera"))
        self.loiter_value.setText(_translate("MainWindow", "LOITER"))
        self.rtl_value.setText(_translate("MainWindow", "RTL"))
        self.disarm_value.setText(_translate("MainWindow", "DISARM"))
        self.arm_value.setText(_translate("MainWindow", "ARM"))
        self.manual_value.setText(_translate("MainWindow", "MANUAL"))
        self.autotune_value.setText(_translate("MainWindow", "AUTOTUNE"))
        self.fbwa_value.setText(_translate("MainWindow", "FBWA"))
        self.fbwb_value.setText(_translate("MainWindow", "FBWB"))
        self.auto_value.setText(_translate("MainWindow", "AUTO"))
        self.ip_text.setText(_translate("MainWindow", "IP:"))
        self.baud_text.setText(_translate("MainWindow", "BAUD:"))
        self.tarih_text.setText(_translate("MainWindow", "DATE:"))
        self.saat_text.setText(_translate("MainWindow", "TIME:"))
        self.altitude_text.setText(_translate("MainWindow", "ALTITUDE:"))
        self.airspeed_text.setText(_translate("MainWindow", "AIR SPEED:"))
        self.gpsspeed_text.setText(_translate("MainWindow", "GPS SPEED:"))
        self.distance_text.setText(_translate("MainWindow", "DISTANCE:"))
        self.roll_text.setText(_translate("MainWindow", "ROLL:"))
        self.pitch_text.setText(_translate("MainWindow", "PITCH:"))
        self.yaw_text.setText(_translate("MainWindow", "YAW:"))
        self.throttle_text.setText(_translate("MainWindow", "THROTTLE:"))
        self.gps_text.setText(_translate("MainWindow", "GPS SATELLITES:"))
        self.battery_text.setText(_translate("MainWindow", "BATTERY:"))
        self.telemetry_text.setText(_translate("MainWindow", "TELEMETRY:"))
        self.arm_text.setText(_translate("MainWindow", "ARM STATUS:"))
        self.mode_text.setText(_translate("MainWindow", "MODE:"))

    def yukseklik(self):
        yukseklik1 = self.iha.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        yukseklik2 = yukseklik1.relative_alt / 1000.0
        self.altitude_value.setText(str(yukseklik2))

    def hava_hizi(self):
        airspeed1 = self.iha.recv_match(type='VFR_HUD', blocking=True)
        airspeed2 = airspeed1.airspeed
        self.airspeed_value.setText(f"{airspeed2:.2f} m/s")

    def gps_hizi(self):
        gpshizi1 = self.iha.recv_match(type='GPS_RAW_INT', blocking = True)
        gpshizi2 = gpshizi1.vel/100.0
        self.gpsspeed_value.setText(f"{gpshizi2:.2f} m/s")

    def gps_sayisi(self):
        gpssayisi1 = self.iha.recv_match(type='GPS_RAW_INT', blocking=True)
        gpssayisi2 = gpssayisi1.satellites_visible
        self.gps_value.setText(str(gpssayisi2))

    def roll_acisi(self):
        roll_acisi1 = self.iha.recv_match(type='ATTITUDE', blocking=True)
        roll_acisi2 = roll_acisi1.roll
        roll_acisi3 = math.degrees(roll_acisi2)
        self.roll_value.setText(f"{roll_acisi3:.2f}")


    def pitch_acisi(self):
        pitchaci1 = self.iha.recv_match(type='ATTITUDE', blocking=True)
        pitchaci2 = pitchaci1.pitch
        pitchaci3 = math.degrees(pitchaci2)
        self.pitch_value.setText(f"{pitchaci3:.2f}")


    def yaw_acisi(self):
        yawaci1 = self.iha.recv_match(type='ATTITUDE', blocking=True)
        yawaci2 = yawaci1.yaw
        yawaci3 = math.degrees(yawaci2)
        self.yaw_value.setText(f"{yawaci3:.2f}")

    def batarya_durumu(self):
        batarya1 = self.iha.recv_match(type='BATTERY_STATUS', blocking=True)
        batarya2 = batarya1.battery_remaining
        self.battery_value.setText(str(batarya2))

    def gaz(self):
        message = self.iha.recv_match(type='RC_CHANNELS', blocking=True)
        throttle_channel = 2
        throttle_value = message.chan3_raw

        # Gaz yüzdesini hesapla (bu, veri aralığına ve kalibrasyonuna bağlıdır)
        # Tipik olarak, değerler 1000 ile 2000 arasında değişir. Bu aralığı normalize etmelisiniz.
        min_value = 1000
        max_value = 2000
        throttle_percentage = (throttle_value - min_value) / (max_value - min_value) * 100.0
        throttle_percentage = max(0, min(100, throttle_percentage))  # Yüzdeyi 0 ile 100 arasında sınırla
        self.throttle_value.setText(str(throttle_percentage))

    def arm(self):
        msg = self.iha.recv_match(type='HEARTBEAT', blocking=True)
        if msg:
            base_mode = msg.base_mode
            system_status = msg.system_status
            armed = base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED

            if armed:
                self.arm_value_2.setText(str("TRUE"))
            else:
                self.arm_value_2.setText(str("FALSE"))
            return armed

    def saat(self):
        saat1 = datetime.datetime.now().strftime('%H:%M:%S')
        self.saat_value.setText(saat1)

    def tarih(self):
        tarih1 = datetime.datetime.now().strftime("%d-%m-%Y")
        self.tarih_value.setText(tarih1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
