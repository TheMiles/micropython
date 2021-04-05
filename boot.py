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
import pixel


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


# connect_wifi(c)
# try:
#     client = connect_mqtt()
# except OSError as e:
#     restart_and_reconnect()


pixels = pixel.Pixels(5,5)

while True:
    pixels.fill(pixel.RED)
    time.sleep(1)
    pixels.fill(pixel.GREEN)
    time.sleep(1)
    pixels.fill(pixel.BLUE)
    time.sleep(1)

    pixels.color_chase(pixel.RED)
    pixels.color_chase(pixel.YELLOW)
    pixels.color_chase(pixel.GREEN)
    pixels.color_chase(pixel.CYAN)
    pixels.color_chase(pixel.BLUE)
    pixels.color_chase(pixel.PURPLE)

    pixels.rainbow_cycle()