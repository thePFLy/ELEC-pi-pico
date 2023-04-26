import machine, time, _thread
from machine import Pin

UART = machine.UART(0, baudrate=9600)

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
# pin 19, GP14 -> [output] green LED
# pin 20, GP15 -> [output] red LED
# GND

# CODE ----------------------------------------------------------------------------------

#pins setup
sensor_trig = Pin(32, mode=Pin.OUT)
sensor_echo = Pin(31, mode=Pin.IN)

data_0 = Pin(24, mode=Pin.OUT)
data_1 = Pin(27, mode=Pin.OUT)
data_2 = Pin(28, mode=Pin.OUT)
data_3 = Pin(25, mode=Pin.OUT)
data_dot = Pin(29, mode=Pin.OUT)

seg_1 = Pin(22, mode=Pin.OUT)
seg_2 = Pin(21, mode=Pin.OUT)

led_green = Pin(19, mode=Pin.OUT)
led_red = Pin(20, mode=Pin.OUT)

#global variables
sensor_timeout = 30000
distance_cm = 0
distance_target = 0

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
    out = [0,0,0,0]
    if n >= 8:
        out[3] = 1
        n -= 8
    if n >= 4:
        out[2] = 1
        n -= 4
    if n >= 2:
        out[1] = 1
        n -= 2
    if n >= 1:
        out[0] = 1
        n -= 1
    return out


def display_thread(distance_cm):
    while True:
        d = str(round(distance_cm))
        if distance_cm >= 100:
            data_dot.value(1)
        else:
            data_dot.value(0)
        if distance_cm <= distance_target:
            led_red.value(1)
            led_green.value(0)
        else:
            led_green.value(1)
        seg_1.value(1)
        seg_2.value(0)
        tmp = itob(int(d[0]))
        data_3.value(tmp[3])
        data_2.value(tmp[2])
        data_1.value(tmp[1])
        data_0.value(tmp[0])
        led_red.value(0)
        seg_1.value(0)
        seg_2.value(1)
        tmp = itob(int(d[1]))
        data_3.value(tmp[3])
        data_2.value(tmp[2])
        data_1.value(tmp[1])
        data_0.value(tmp[0])


# MAIN
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
_thread.start_new_thread(display_thread,distance_cm)
while True:
    # read usb
    if uart.any(): 
        data = uart.read() 
        if data == b'get':
            uart.write(bin(distance_target))
        elif data == b'd':
            uart.write(bin(distance_cm))
        else:
            try:
                distance_target = int(data)
                uart.write(bin("value changed..."))
            except:
                pass

    # send pulse
    sensor_trig.value(0)
    time.sleep_us(5)
    sensor_trig.value(1)
    time.sleep_us(10)
    sensor_trig.value(0)

    #await response
    try:
        pulse_len = machine.time_pulse_us(sensor_echo, 1, sensor_timeout)
        distance_cm = (pulse_len / 2) / 29.1

    except:
        #allow timeout to happen whitout breaking everything (could be more precise tho)

        #display 0 if the sensor is too far from any objects
        distance_cm = 0
