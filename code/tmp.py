import serial
import time
import keyboard
import glob

def countdown():
    distance = "0"
    while True:
        color = "\033[92m"
        if leave:
            return
        try:
            distance = ser.readline().decode().strip()
            ser.flushInput()
            if float(distance) < 0:
                distance = "wrong angle"
                color = "\033[91m"
            if float(distance) > limit:
                color = "\033[39m\033[102m"
        except:
            pass
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(f"\033[93mDistance: {color}{distance}\033[49m \033[93mcm\nLimit: \033[96m{limit}")
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

def left(arg):
    global leave
    leave = True

def find_ports():
    ports = glob.glob('/dev/ttyACM[0-9]*')

    res = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            res.append(port)
        except:
            pass
    return res

def main():
    keyboard.on_press_key("up", handle_up_key)
    keyboard.on_press_key("down", handle_down_key)
    keyboard.on_press_key("escape", left)

    countdown()

if __name__ == "__main__":
    global limit
    global ser
    global leave
    leave = False
    limit = 50
try:
    ser = serial.Serial(find_ports()[0], 9600)
    main()
except Exception as e:
    print("error: cant connect to device\n", e)


