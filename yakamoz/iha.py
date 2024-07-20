from dronekit import connect, VehicleMode
import time

class iha():

    def __init__(self, connection):
        self.connection = connection
        self.baglanti= connect(self.connection, wait_ready=False)


    def BAGLAN_butonu(self):
        print("BAGLAN BUTONU")


    def ARMED_butonu(self):

        while self.baglanti.is_armable == False:
                print("Arm ici gerekli sartlar saglanamadi.")
                time.sleep(1)
        print("Iha su anda armedilebilir")
        self.baglanti.armed = True

    def DISARMED_butonu(self):
        self.baglanti.disarm = True


    def FBWA_butonu(self):
        self.baglanti.mode = VehicleMode("FBWA")


    def FBWB_butonu(self):
        self.baglanti.mode = VehicleMode("FBWB")

    def RTL_butonu(self):

        self.baglanti.mode = VehicleMode("RTL")

    def MANUEL_butonu(self):
        self.baglanti.mode = VehicleMode("MANUEL")

    def AUTO_butonu(self):
        self.baglanti.mode = VehicleMode("AUTO")