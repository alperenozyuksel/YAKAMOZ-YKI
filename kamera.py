import sys
import socket
import struct
import pickle
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

HOST = '192.168.1.10'
PORT = 8485


class VideoStream(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Video Stream')
        self.setGeometry(100, 100, 800, 600)

        # Create a QLabel to display the video frames
        self.image_label = QLabel(self)
        self.image_label.resize(800, 600)

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        # Timer to update the frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 ms

        self.data = b""
        self.payload_size = struct.calcsize(">L")

    def update_frame(self):
        while len(self.data) < self.payload_size:
            self.data += self.socket.recv(4096)
            if not self.data:
                return

        # Receive image row data from client socket
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.socket.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        # Unpack image using pickle
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        if frame is not None:
            # Convert the image to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.socket.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoStream()
    window.show()
    sys.exit(app.exec_())
