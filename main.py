from machine import I2C, Pin
import time
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import DS3231

# ---- I2C Settings ---- #
i2c = I2C(0, sda=Pin(21), scl=Pin(22))

# ---- Display Settings ---- #
addr = 0x27
rows = 4
cols = 20
lcd = I2cLcd(i2c, addr, rows, cols)


# ---- DS3231 Settings ---- #
ds = DS3231.DS3231(i2c)


clock = [
    0x1F,
    0x1F,
    0x0E,
    0x04,
    0x04,
    0x0A,
    0x11,
    0x1F
    ]


termometer = [
    0x04,
    0x0E,
    0x0A,
    0x0A,
    0x0E,
    0x0E,
    0x1F,
    0x0E
]



# ---------- ## ------------- #

def time_funtion():
    hour = str(ds.Hour())
    minute = str(ds.Minute())
    seconds = str(ds.Second())
    #clock_hex = lcd.custom_char(0, bytearray(clock))
    #clock_icon = lcd.putchar(chr(0))
    lcd.putstr('Time: '+ hour + ':' + minute + ':' + seconds)

def temp():
    temp = str(ds.Temperature())
    #term = lcd.custom_char(1, bytearray(termometer))
    #term_icon = lcd.putchar(chr(1))
    lcd.putstr('Temp: ' + temp + ' C')

def main():
    lcd.clear()
    while True:
        lcd.move_to(0,0)
        time_funtion()
        lcd.move_to(0,1)
        temp()
        time.sleep(0.1)
        

if __name__ == '__main__':
    main()
