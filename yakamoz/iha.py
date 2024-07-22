from dronekit import connect, VehicleMode
import time

class iha():

    def __init__(self, connection):
        self.connection = connection
        self.baglanti = connect(self.connection, wait_ready=False)


