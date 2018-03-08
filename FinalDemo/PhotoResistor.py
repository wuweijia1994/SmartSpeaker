import serial
import client
import threading
import time


ser=serial.Serial("/dev/cu.usbmodem1441",9600,timeout=0.5)
darkness = 700

def receive_data():
    global darkness
    while True:
        data = ser.readline().decode()
        while data == '':
            data = ser.readline().decode()
        darkness = int(data.strip())

def is_dark():
    global darkness
    # darkness = receive_data()
    if darkness > 550 :
        return True
    else:
        return False

if __name__ == '__main__':
    cnt = client.RaspConnection()
    cnt.connect()

    t = threading.Thread(target=receive_data, name='LoopThread')
    t.start()
    while True:
        if is_dark():
            cnt.send_commands('4')
            # time.sleep(5)
            print("It is dark!")

        else:
            cnt.send_commands('1')
            # time.sleep(2)
            # cnt.send_commands('2')
            # time.sleep(2)
            # cnt.send_commands('3')
            # time.sleep(2)
            print("It is bright!")