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

import neopixel


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


connect_wifi(c)
# try:
#     client = connect_mqtt()
# except OSError as e:
#     restart_and_reconnect()


pixel_pin = machine.Pin(5, machine.Pin.OUT)
num_pixels = 5
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.write()
        time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()



RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

while True:
    print("Go")
    pixels.fill(RED)
    pixels.write()
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.write()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.write()
    time.sleep(1)

    print(pixels[0])

    color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    color_chase(YELLOW, 0.1)
    color_chase(GREEN, 0.1)
    color_chase(CYAN, 0.1)
    color_chase(BLUE, 0.1)
    color_chase(PURPLE, 0.1)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow