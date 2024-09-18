import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPainterPath
from PyQt5.QtCore import Qt, QTimer, QPointF
from pymavlink import mavutil


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
        try:
            self.master = mavutil.mavlink_connection("127.0.0.1:14550")
        except Exception as e:
            print(f'Error connecting to MAVLink: {e}')
            self.master = None

        # Zamanlayıcı kurarak belirli aralıklarla veri almayı sağlayın
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_indicator)
        self.timer.start(50)  # 50 ms'de bir veri al ve güncelle

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Horizon Indicator')
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)  # Anti-aliasing etkinleştir

        # Horizon çizimi
        self.drawHorizon(qp)
        # Metin bilgileri
        self.drawText(qp)
        # Dikdörtgen çizimi
        self.drawRectangle(qp)
        # Gyro çizgileri
        self.drawGyroLines(qp)

        # Custom Plot Widget
        self.drawCustomPlot(qp)

        qp.end()

    def drawHorizon(self, qp):
        center_x = self.width() // 2
        center_y = self.height() // 2

        # Calculate the vertical offset based on the pitch
        pitch_offset = (self.pitch / 90.0) * (self.height() / 2)

        # Draw the sky
        qp.save()
        qp.setBrush(QColor(0, 102, 204))  # Blue color
        qp.translate(0, int(pitch_offset))
        qp.drawRect(0, -self.height(), self.width(), center_y + self.height())  # Draw the sky
        qp.restore()

        # Draw the ground
        qp.save()
        qp.setBrush(QColor(255, 140, 45))  # Orange color
        qp.translate(0, int(pitch_offset))
        qp.drawRect(0, center_y, self.width(), self.height() - center_y + self.height())  # Draw the ground
        qp.restore()

        # Draw pitch lines and labels
        qp.save()
        qp.translate(center_x, center_y + int(pitch_offset))
        qp.rotate(-self.roll)

        # Set line color to yellow
        qp.setPen(QPen(QColor(255, 255, 0), 2, Qt.SolidLine))  # Yellow color

        for p in range(-30, 31, 10):
            if p == 0:
                continue
            y = int((p / 50.0) * (self.height() / 2) * 1.1)  # Adjusted line position
            qp.drawLine(-55, -y, 55, -y)  # Extended line length
            qp.drawText(60, -int(y + 5), str(p))  # Adjusted text position
            qp.drawText(-85, -int(y + 5), str(p))  # Adjusted text position

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

    def drawRectangle(self, qp):
        # Dikdörtgenin konumu ve boyutları
        margin = 0.40  # Merkezden %40 genişlik
        margin_x = (1 - margin) / 2
        rect_x = int(self.width() * margin_x)
        rect_width = int(self.width() * margin)

        margin_y = 0.05  # Ekranın üstünden ve altından %5 uzaklık
        rect_y = int(self.height() * margin_y)
        rect_height = int(self.height() * (1 - 2 * margin_y))

        # Köşe yarıçapı %10 ekran genişliği
        radius = int(self.width() * 0.10)

        qp.setPen(QPen(QColor(255, 255, 255), 2, Qt.SolidLine))  # Beyaz renk ve 2 px kalınlıkta kenar çizgisi
        qp.setBrush(QColor(0, 0, 0, 0))  # Şeffaf iç renk

        qp.drawRoundedRect(rect_x, rect_y, rect_width, rect_height, radius,
                           radius)  # Köşeleri yuvarlatılmış dikdörtgen çizimi

    def drawGyroLines(self, qp):
        center_x = self.width() // 2
        center_y = self.height() // 2

        line_length = 25
        qp.setPen(QPen(QColor(0, 245, 0), 2, Qt.SolidLine))

        qp.save()
        qp.translate(center_x, center_y)
        qp.rotate(-self.pitch)  # pitch açısına göre döndür
        qp.translate(-center_x, -center_y)

        qp.drawLine(center_x, center_y, center_x + line_length, center_y + line_length)
        qp.drawLine(center_x, center_y, center_x - line_length, center_y + line_length)

        qp.restore()

    def drawCustomPlot(self, qp):
        center_x = self.width() // 2
        center_y = self.height() // 2

        length = 9
        values = np.arange(-60, 61, 10)
        num_values = len(values)
        x = np.linspace(-length / 2, length / 2, num_values)

        a = 0.05
        b = 0.5
        y = -a * x ** 2 + b

        pen = QPen(QColor('black'))
        pen.setWidth(2)
        qp.setPen(pen)

        path = QPainterPath()
        start_point = self.mapToPainter(x[0], y[0])
        path.moveTo(QPointF(start_point[0], start_point[1]))

        for i in range(1, num_values):
            x_pos, y_pos = self.mapToPainter(x[i], y[i])
            path.lineTo(QPointF(x_pos, y_pos))

        qp.drawPath(path)

        font = QFont()
        font.setPointSize(12)
        font.setFamily('Arial')
        qp.setFont(font)
        qp.setPen(QColor('black'))

        for i in range(num_values):
            display_value = abs(values[i])
            x_pos, y_pos = self.mapToPainter(x[i], y[i])

            text_rect = qp.boundingRect(int(x_pos) - 10, int(y_pos) - 20, 20, 20, 0, str(display_value))
            text_x = int(x_pos) - text_rect.width() // 2
            text_y = int(y_pos) - text_rect.height() - 10

            qp.drawText(text_x, text_y, str(display_value))
            qp.drawLine(int(x_pos), int(y_pos), int(x_pos), int(y_pos - 15))

        def get_parabola_value(degrees):
            return -a * (degrees / 10) ** 2 + b

        actual_angle = self.roll
        parabolic_value = get_parabola_value(actual_angle)

        triangle_width = 0.3
        triangle_height = 0.1
        triangle_y_offset = -0.49

        # Üçgenin köşe noktalarını hesapla
        triangle_points = [
            self.mapToPainter(-triangle_width / 2, -triangle_height - triangle_y_offset),
            self.mapToPainter(triangle_width / 2, -triangle_height - triangle_y_offset),
            self.mapToPainter(0, -triangle_y_offset)
        ]

        qp.save()
        qp.translate(center_x, center_y)
        qp.rotate(-self.roll)  # Roll açısına göre döndür
        qp.translate(-center_x, -center_y)

        path = QPainterPath()
        path.moveTo(QPointF(triangle_points[0][0], triangle_points[0][1]))
        path.lineTo(QPointF(triangle_points[1][0], triangle_points[1][1]))
        path.lineTo(QPointF(triangle_points[2][0], triangle_points[2][1]))
        path.closeSubpath()

        qp.setPen(QPen(QColor('black'), 2))
        qp.setBrush(QColor(0, 0, 0, 0))
        qp.drawPath(path)
        qp.restore()

    def mapToPainter(self, x, y):
        width = self.width()
        height = self.height()
        x_min = -12 / 2 - 1
        x_max = 12 / 2 + 1
        y_min = -0.05 * (12 / 2) ** 2 - 2
        y_max = 1

        x_norm = (x - x_min) / (x_max - x_min)
        y_norm = (y - y_min) / (y_max - y_min)

        x_pix = x_norm * width
        y_pix = (1 - y_norm) * height

        return x_pix, y_pix

    def update_indicator(self):
        if not self.master:
            print('MAVLink connection not established.')
            return

        try:
            # Her tür veriyi sadece bir kez alalım
            msg = self.master.recv_match(type='ATTITUDE', blocking=False)
            if msg:
                self.pitch = msg.pitch * 57.2958  # Radyan -> Derece dönüşümü
                self.roll = msg.roll * 57.2958  # Radyan -> Derece dönüşümü
                self.yaw = msg.yaw * 57.2958  # Radyan -> Derece dönüşümü

            msg_alt = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
            if msg_alt:
                self.altitude = msg_alt.relative_alt / 1000.0  # Milimetre -> Metre dönüşümü

            msg_batt = self.master.recv_match(type='BATTERY_STATUS', blocking=False)
            if msg_batt:
                self.battery_voltage = msg_batt.voltages[1] / 1000.0  # Milivolt -> Volt dönüşümü
                self.battery_current = msg_batt.current_battery / 100.0  # Centi-ampere -> Amper dönüşümü
                self.battery_percent = msg_batt.battery_remaining  # Yüzde olarak

            self.update()  # Ekranı güncelle
        except Exception as e:
            print(f'Error updating indicator: {e}')


def main():
    app = QApplication(sys.argv)
    ex = HorizonIndicator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()