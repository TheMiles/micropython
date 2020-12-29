# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import toollib
import network
import time
import machine
from umqtt.robust import MQTTClient
from button import MQTTButton


c = toollib.readConfig('config')

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(c['WLAN_SSID'], c['WLAN_PWD'])

while station.isconnected() == False:
    print('Trying to connect to',c['WLAN_SSID'])
    time.sleep(1)
print('Connection successful')

client = MQTTClient("testClient", c['MQTT_HOST'], user=c['MQTT_USER'], password=c['MQTT_PWD'])
client.connect()

#m = TestMQTT('me', c['MQTT_HOST'], user=c['MQTT_USER'], password=c['MQTT_PWD'])

led = machine.Pin(12, machine.Pin.OUT)

def cb_switchLed(p):
    global led

    led.value(not led.value())


button = MQTTButton(14, client, "buttons/bell/one")

