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
from bme680 import *
from machine import Pin, I2C

last_message     = 0
message_interval = 5


client_id = ubinascii.hexlify(machine.unique_id())

topic_pub_temp = b'esp/bme680/temperature'
topic_pub_hum  = b'esp/bme680/humidity'
topic_pub_pres = b'esp/bme680/pressure'
topic_pub_gas  = b'esp/bme680/gas'


c = toollib.readConfig('config')

def connect_wifi(c):

    print('Trying to connect to',c['WLAN_SSID'])
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(c['WLAN_SSID'], c['WLAN_PWD'])

    while not station.isconnected() :
        pass
    print('Connection successful')


# ESP32 - Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21))
bme = BME680_I2C(i2c=i2c)

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

def read_bme_sensor():
    try:
        temp = (b'{:.2f}'.format(bme.temperature))
        hum = (b'{:.2f}'.format(bme.humidity))
        pres = (b'{:.2f}'.format(bme.pressure))
        gas = (b'{:.2f}'.format(bme.gas/1000))

        return temp, hum, pres, gas
    except OSError as e:
        return('Failed to read sensor.')


try:
    connect_wifi(c)
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
        if (time.time() - last_message) > message_interval:
            temp, hum, pres, gas = read_bme_sensor()
            print("Temp: {} hum {} pres {} gas {}".format(temp, hum, pres, gas))
            client.publish(topic_pub_temp, temp)
            client.publish(topic_pub_hum, hum)
            client.publish(topic_pub_pres, pres)
            client.publish(topic_pub_gas, gas)

            last_message = time.time()
    except OSError as e:
        restart_and_reconnect()

