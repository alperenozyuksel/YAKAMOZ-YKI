import time
from dronekit import connect, VehicleMode

class ButtonManager():

    def __init__(self,iha):
        self.iha=iha


    def BAGLAN_butonu(self):
        print("BAGLAN BUTONU")


    def ARMED_butonu(self):

        while self.iha.baglanti.is_armable == False:
                print("Arm ici gerekli sartlar saglanamadi.")
                time.sleep(1)
        print("Iha su anda armedilebilir")
        self.iha.baglanti.armed = True

    def DISARMED_butonu(self):
        self.iha.baglanti.disarm = True


    def FBWA_butonu(self):
        self.iha.baglanti.mode = VehicleMode("FBWA")

    def FBWB_butonu(self):
        self.iha.baglanti.mode = VehicleMode("FBWB")

    def RTL_butonu(self):
        self.iha.baglanti.mode = VehicleMode("RTL")

    def MANUEL_butonu(self):
        self.iha.baglanti.mode = VehicleMode("MANUEL")

    def AUTO_butonu(self):
        self.iha.baglanti.mode = VehicleMode("AUTO")