import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QTimer
from pymavlink import mavutil
import math

class HorizonIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        self.altitude = 0.0
        self.battery_voltage = 0.0
        self.battery_current = 0.0
        self.battery_percent = 0.0
        self.initUI()

        # MAVLink bağlantısını başlatın
        self.master = mavutil.mavlink_connection("127.0.0.1:14550")

        # Zamanlayıcı kurarak belirli aralıklarla veri almayı sağlayın
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_indicator)
        self.timer.start(50)  # 50 ms'de bir veri al ve güncelle

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Horizon Indicator')
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawHorizon(qp)
        self.drawText(qp)
        qp.end()

    def drawHorizon(self, qp):
        center_x = self.width() / 2
        center_y = self.height() / 2

        # Pitch ve roll hesaplamaları
        pitch_offset = (self.pitch / 90.0) * (self.height() / 2)
        roll_angle = math.radians(self.roll)

        # Horizon çizimi için renkler ve arka plan
        qp.setBrush(QColor(0, 102, 204))
        qp.save()
        qp.translate(center_x, center_y)
        qp.rotate(-self.roll)
        qp.translate(-center_x, -center_y + pitch_offset)
        qp.drawRect(0, -self.height(), self.width(), self.height())

        qp.setBrush(QColor(153, 51, 51))
        qp.drawRect(0, center_y - pitch_offset, self.width(), self.height())

        # Orta çizgiyi daha belirgin hale getirin
        qp.setPen(QPen(QColor(255, 255, 0), 4))  # Sarı ve daha kalın çizgi
        qp.drawLine(0, center_y, self.width(), center_y)
        qp.restore()

        # Pitch çizgileri
        qp.save()
        qp.translate(center_x, center_y)
        qp.rotate(-self.roll)
        qp.setPen(QPen(Qt.blue, 2))  # Pitch çizgileri mavi yapıldı
        for p in range(-30, 31, 10):
            if p == 0:
                continue
            y = (p / 90.0) * (self.height() / 2) + pitch_offset
            qp.drawLine(-50, y, 50, y)
            qp.drawText(55, y + 5, str(p))
            qp.drawText(-70, y + 5, str(p))
        qp.restore()

    def drawText(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setFont(QFont('Arial', 15))

        # Alt kısımdaki metin bilgileri
        text_x = 10
        text_y_start = self.height() - 120
        line_height = 20

        qp.drawText(text_x, text_y_start, f'Roll: {self.roll:.2f}')
        qp.drawText(text_x, text_y_start + line_height, f'Pitch: {self.pitch:.2f}')
        qp.drawText(text_x, text_y_start + 2 * line_height, f'Yaw: {self.yaw:.2f}')
        qp.drawText(text_x, text_y_start + 3 * line_height, f'Altitude: {self.altitude:.2f}')

        # Sağ üst köşedeki batarya bilgileri
        text_x = self.width() - 200
        text_y_start = 20

        qp.drawText(text_x, text_y_start, f'Voltage: {self.battery_voltage:.2f} V')
        qp.drawText(text_x, text_y_start + line_height, f'Current: {self.battery_current:.2f} A')
        qp.drawText(text_x, text_y_start + 2 * line_height, f'Percent: {self.battery_percent:.2f} %')

    def update_indicator(self):
        # MAVLink'den veri al
        try:
            msg = self.master.recv_match(type='ATTITUDE', blocking=True, timeout=1)
            if msg:
                self.pitch = msg.pitch * 57.2958  # Radyan -> Derece dönüşümü
                self.roll = msg.roll * 57.2958  # Radyan -> Derece dönüşümü
                self.yaw = msg.yaw * 57.2958  # Radyan -> Derece dönüşümü

            msg_alt = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=1)
            if msg_alt:
                self.altitude = msg_alt.relative_alt / 1000.0  # Milimetre -> Metre dönüşümü

            msg_batt = self.master.recv_match(type='BATTERY_STATUS', blocking=True, timeout=1)
            if msg_batt:
                self.battery_voltage = msg_batt.voltages[1] / 1000.0  # Milivolt -> Volt dönüşümü
                self.battery_current = msg_batt.current_battery / 100.0  # Centi-ampere -> Amper dönüşümü
                self.battery_percent = msg_batt.battery_remaining  # Yüzde olarak

            self.update()  # Ekranı güncelle
        except Exception as e:
            print(f'Error: {e}')

def main():
    app = QApplication(sys.argv)
    ex = HorizonIndicator()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
