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

topic = "buttons/bell/one"


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

led = machine.Pin(12, machine.Pin.OUT)

def blinkLED(led):
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.2)
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.2)
    led.value(1)
    time.sleep(0.5)
    led.value(0)


def cb_subscribedTopic(t,m):
    global led

    if m==b'True':
        blinkLED(led)


button = MQTTButton(14, client, topic)

client.set_callback(cb_subscribedTopic)
client.subscribe(topic)

try:
    while 1:
        client.wait_msg()
finally:
    client.disconnect()
