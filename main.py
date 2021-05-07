from machine import I2C, Pin, Timer
import time
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import DS3231

# ---- I2C Settings ---- #
i2c = I2C(0, sda=Pin(21), scl=Pin(22))

# ---- Rotary Encoder ---- #
btn = Pin(2, Pin.IN, Pin.PULL_UP)

# ---- Display Settings ---- #
addr = 0x27
rows = 4
cols = 20
lcd = I2cLcd(i2c, addr, rows, cols)

# ---- DS3231 Settings ---- #
ds = DS3231.DS3231(i2c)

# ---------- ## ------------- #


def time_funtion():
    lcd.putstr('{:02d}:{:02d}:{:02d}'.format(ds.Hour(), ds.Minute(),
                                             ds.Second()))


def day():
    wkdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
        'Nov', 'Dec'
    ]
    lcd.putstr('{} {:02d} {}'.format(wkdays[ds.Weekday() - 1], ds.Day(),
                                     months[ds.Month() - 1]))


def temp():
    grade = [0x1C, 0x14, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00]
    lcd.custom_char(0, bytearray(grade))
    lcd.putstr('{:02d}'.format(int(ds.Temperature())))
    lcd.putchar(chr(0))
    lcd.putstr('C')


def alarm():
    alarm = [0x04, 0x0E, 0x0E, 0x0E, 0x0E, 0x1F, 0x00, 0x04]
    lcd.custom_char(1, bytearray(alarm))
    lcd.putchar(chr(1))


def btn_status(timer):
    print('Value BNT: {}'.format(btn.value()))


def main():
    lcd.clear()
    tim = Timer(1)
    tim.init(period=1000, mode=Timer.PERIODIC, callback=btn_status)
    while True:
        lcd.move_to(0, 0)
        alarm()
        lcd.move_to(16, 0)
        temp()
        lcd.move_to(6, 1)
        time_funtion()
        lcd.move_to(5, 2)
        day()
        lcd.move_to(2, 3)
        lcd.putstr('By Gaston Giane.')
        time.sleep(0.1)


if __name__ == '__main__':
    main()

