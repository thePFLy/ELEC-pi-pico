import machine, time, _thread
from machine import Pin

# ultrasonic sensor ---------------------------------------------------------------------
# pin 40, VBUS -> [output] SR04 vcc
# pin 32, GP27 -> [PWM output] SR04 trig, at least 10µs psaced by at least 60µs
# pin 31, GP26 -> [PWM input] SR04 echo, read lenght for sistance (PW/58 = distance cm)
# GND

# 7 segment driver ----------------------------------------------------------------------
# pin 40, VBUS -> [output] CD4511 vcc(16), LT(3), BL(4)
# pin 29, GP22 -> [output] 7 seg 1 dot separator
# pin 27, GP21 -> [output] CD4511 D1(1)
# pin 26, GP20 -> [output] CD4511 D2(2)
# pin 25, GP19 -> [output] CD4511 D3(6)
# pin 24, GP18 -> [output] CD4511 D0(7)
# GND (8)

# transistors ---------------------------------------------------------------------------
# pin 22, GP17 -> [output] TRANSISTOR 7seg 1
# pin 21, GP16 -> [output] TRANSISTOR 7seg 2

# LEDs ----------------------------------------------------------------------------------
# pin , GP12 -> [output] green LED
# pin , GP13 -> [output] red LED
# GND

# CODE ----------------------------------------------------------------------------------

#pins setup
sensor_trig = Pin(27, mode=Pin.OUT)
sensor_echo = Pin(26, mode=Pin.IN)

data_0 = Pin(18, mode=Pin.OUT)
data_1 = Pin(21, mode=Pin.OUT)
data_2 = Pin(20, mode=Pin.OUT)
data_3 = Pin(19, mode=Pin.OUT)
data_dot = Pin(22, mode=Pin.OUT)

seg_1 = Pin(15, mode=Pin.OUT)
seg_2 = Pin(16, mode=Pin.OUT)

led_green = Pin(12, mode=Pin.OUT)
led_red = Pin(13, mode=Pin.OUT)
time.sleep_us(100)

#global variables
sensor_timeout = 30000
distance_cm = 0
distance_target = 50

#pins default values
sensor_trig.value(0)
data_0.value(0)
data_1.value(0)
data_2.value(0)
data_3.value(0)
data_dot.value(0)
seg_1.value(0)
seg_2.value(0)
led_green.value(1)
led_red.value(0)

def itob(n):
    if n == 0:
        return "00000000"
    numbers = str(int(n))+"0"
    out = [0,0,0,0,0,0,0,0]
    
    tmp = int(numbers[0])
    if tmp >= 8:
        out[0] = 1
        tmp -= 8
    if tmp >= 4:
        out[1] = 1
        tmp -= 4
    if tmp >= 2:
        out[2] = 1
        tmp -= 2
    if tmp >= 1:
        out[3] = 1
        
    tmp = int(numbers[1])
    if tmp >= 8:
        out[4] = 1
        tmp -= 8
    if tmp >= 4:
        out[5] = 1
        tmp -= 4
    if tmp >= 2:
        out[6] = 1
        tmp -= 2
    if tmp >= 1:
        out[7] = 1
        
    return out

# MAIN
uart = machine.UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
#_thread.start_new_thread(display_thread, (distance_cm, ))
while True:
    # read usb
    if uart.any():
        received_data = uart.readline().decode().strip()
        if received_data == "exit":
            break
        print("Received data:", received_data)
        uart.write("ACK: " + received_data + "\n")
        
    # send pulse
    sensor_trig.value(0)
    time.sleep_us(5)
    sensor_trig.value(1)
    time.sleep_us(10)
    sensor_trig.value(0)

    #await response
    try:
        pulse_len = (machine.time_pulse_us(sensor_echo, 1, sensor_timeout))
        distance_cm = (pulse_len / 2) / 29.1
        time.sleep_us(15000)

    except:
        #allow timeout to happen whitout breaking everything (could be more precise tho)

        #display 0 if the sensor is too far from any objects
        distance_cm = 0
        
    #display led
    if distance_cm > distance_target:
        led_green.value(0)
        led_red.value(1)
    else:
        led_green.value(1)
        led_red.value(0)
        
    #display 7-seg
    tmp = itob(distance_cm)
    print(distance_cm, tmp)
    #print(tmp)
    seg_2.value(0)
    seg_1.value(1)
    data_0.value(tmp[4])
    data_1.value(tmp[5])
    data_2.value(tmp[6])
    data_3.value(tmp[7])
    time.sleep_us(20000)
    seg_1.value(0)
    seg_2.value(1)
    data_0.value(tmp[0])
    data_1.value(tmp[1])
    data_2.value(tmp[2])
    data_3.value(tmp[3])
        
