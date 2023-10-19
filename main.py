import time
import network
import myConnect as mc
import picozero as pz
from machine import Pin

# LEDS
onboard = Pin('LED', Pin.OUT)
external = Pin(17, Pin.OUT)

# ensures minimal power draw
external.on()

# init sensors
thermo_pin = pz.Pot(27)
photo_pin = pz.Pot(28)

# Connection and Keys
link = mc.myConnect()

# set the wlan setings
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(link.keys['WIFI_NAME'], link.keys['WIFI_PASS'])

# connect to the network 
while(True):
    if wlan.isconnected() and wlan.status() == 3:
        onboard.on()
        break
    else:
        print(wlan.status())
        time.sleep(1)

# enter the main control loop
while True:
    
    # get averaged data
    photo_sum = 0
    therm_sum = 0
    for i in range(10):
        photo_sum += photo_pin.value
        therm_sum += thermo_pin.value    
        time.sleep(0.1)
    
    # send the payload in line format
    if link.pushToInflux("weather", "local,sensor=pico photoresistor={},thermoresistor={}".format(photo_sum, therm_sum)) == 204:
        print("Send OK")

    time.sleep(9)