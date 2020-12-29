# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import toollib
import network
import time

c = toollib.readConfig('config')

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(c['WLAN_SSID'], c['WLAN_PWD'])

while station.isconnected() == False:
    print('Trying to connect to',c['WLAN_SSID'])
    time.sleep(1)
print('Connection successful')

