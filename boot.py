# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import toollib
import network
import time
import machine
from mqtt_test import TestMQTT
from button import Button


c = toollib.readConfig('config')

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(c['WLAN_SSID'], c['WLAN_PWD'])

while station.isconnected() == False:
    print('Trying to connect to',c['WLAN_SSID'])
    time.sleep(1)
print('Connection successful')

#m = TestMQTT('me', c['MQTT_HOST'], user=c['MQTT_USER'], password=c['MQTT_PWD'])

led = machine.Pin(12, machine.Pin.OUT)

def cb_switchLed(p):
    global led

    led.value(not led.value())


button = Button(14, cb_switchLed, trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING)
button.startListen()
