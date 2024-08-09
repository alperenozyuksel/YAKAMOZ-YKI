import time
import threading
def toplama(a,b):
    print("Başladı")
    time.sleep(2)
    print(a+b)

def bitti():
    print("Bitti")


threading.Thread(target=toplama,args = (2,4)).start()
threading.Thread(target = bitti).start()



