from pymavlink import mavutil
import time

# MAVLink bağlantısını kurun
# Port ve baudrate ayarlarını kendi kurulumunuza göre değiştirin
master = mavutil.mavlink_connection("127.0.0.1:14550")

# Bağlantının hazır olduğunu kontrol edin
master.wait_heartbeat()
print("Heartbeat from system (system_id %d component_id %d)" % (master.target_system, master.target_component))

def handle_message(msg):
    if msg.get_type() == 'STATUSTEXT':
        # Mesajın içeriğini al ve UTF-8 formatında decode et
        text = msg.text.decode('utf-8')
        print(f"Received STATUSTEXT message: {text}")

    elif msg.get_type() == 'SYS_STATUS':
        # SYS_STATUS mesajını işleyebilirsiniz, örneğin:
        print("Received SYS_STATUS message:")
        print(f"  Load: {msg.load}")
        print(f"  Battery Voltage: {msg.voltage_battery / 1000.0} V")
        print(f"  Battery Current: {msg.current_battery / 100.0} A")
        print(f"  Drop Rate Comm: {msg.drop_rate_comm}")


# Mesajları dinleyin
try:
    while True:
        msg = master.recv_match(blocking=True)
        if msg:
            handle_message(msg)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    master.close()
