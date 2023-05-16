import serial
import time
import keyboard
import os

def countdown():
    distance = "0"
    while True:
        try:
            distance = ser.readline().decode().strip()
            ser.flushInput()
            if float(distance) < 0:
                distance = "wrong angle"
        except:
            pass
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Distance: {distance} cm\nLimit: {limit}")
        time.sleep(0.05)

def handle_up_key(arg):
    global limit
    global ser
    limit += 10
    ser.write(str(limit).encode())

def handle_down_key(arg):
    global limit
    global ser
    limit -= 10
    ser.write(str(limit).encode())

def main():
    keyboard.on_press_key("up", handle_up_key)
    keyboard.on_press_key("down", handle_down_key)
    countdown()

if __name__ == "__main__":
    global limit
    global ser
    limit = 50
try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    main()
except Exception as e:
    print("error: cant connect to device",e)


