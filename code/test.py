import serial

ser = serial.Serial('/dev/ttyACM1',9600, timeout=1)

message = "Hello".encode()

while True:
    ser.write(message)
    distance = ser.readline().decode()
    print(distance)
ser.close()