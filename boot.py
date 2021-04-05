# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import toollib
import network
import time
import ubinascii
import machine
from umqtt.robust import MQTTClient
from button import MQTTButton

topic = "buttons/bell/one"

client_id = ubinascii.hexlify(machine.unique_id())



c = toollib.readConfig('config')


def connect_wifi(c):

    print('Trying to connect to',c['WLAN_SSID'])
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(c['WLAN_SSID'], c['WLAN_PWD'])

    while not station.isconnected() :
        pass
    print('Connection successful')

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

def connect_mqtt():
    global client_id, c
    client = MQTTClient(client_id, c['MQTT_HOST'], user=c['MQTT_USER'], password=c['MQTT_PWD'])
    client.connect()
    print('Connected to {} MQTT broker'.format(c['MQTT_HOST']))
    return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()


connect_wifi(c)

try:
    client = connect_mqtt()
except OSError as e:
    restart_and_reconnect()

def cb_subscribedTopic(t,m):
    global led
    if m==b'True':
        blinkLED(led)


client.set_callback(cb_subscribedTopic)
client.subscribe(topic)

while True:
    try:
        client.wait_msg()
    except OSError as e:
        restart_and_reconnect()

