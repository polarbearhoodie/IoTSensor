import time
import network
import myConnect as mc
import picozero as pz
import machine

# LEDS
onboard = machine.Pin('LED', machine.Pin.OUT)
external = machine.Pin(17, machine.Pin.OUT)

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

# attempt to connect to the network for 20 seconds 
for i in range(20):
    if wlan.isconnected() and wlan.status() == 3:
        onboard.on()
        break
    else:
        print(wlan.status())
        time.sleep(1)

# reset the device if it is not connected to the network
if wlan.status() != 3:
    machine.reset()


# enter the main control loop for at least 1 hour (memory leak/low voltage after 3 days or 8640 cycles)
for j in range(360):
    
    # get averaged data
    photo_sum = 0
    therm_sum = 0
    for i in range(10):
        photo_sum += photo_pin.value
        therm_sum += thermo_pin.value    
        time.sleep(0.1)
    
    payload = "local,sensor=pico photoresistor={},thermoresistor={}".format(photo_sum, therm_sum)

    # send the payload in line format
    if link.pushToInflux("weather", payload) == 204:
        print("SEND OK")
    
    time.sleep(9)

# after an hour, reset everything and restart
machine.reset()