import serial
import time

def main():
    # open a serial connection
    try:
        s = serial.Serial('/dev/ttyACM0')
    except:
        print("could not connect, program stopped...")
        return
    while True:
        print("what do you want to do?\n 1 - change threshold\n 2 - get threshhold\n 3 - get distance")
        tmp = input(">")
        try:
            if int(tmp) == 1:
                tmp2 = input("what is the new value?:")
                s.write(bin(tmp2))
                time.sleep(1)
                print(s.readline().strip())
            elif int(tmp) == 2:
                s.write(b"get")
                time.sleep(1)
                print(s.readline().strip())
            else:
                s.write(b"d")
                time.sleep(1)
                print(s.readline().strip())
        except:
            pass

if __name__ == "__main__":
    main()