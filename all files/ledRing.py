import os
from time import sleep

import requests


def request():
    url = "https://studev.groept.be/api/a21ib2d02/led_get"
    return requests.get(url).json()


def led_ring():
    # x = 0
    # while x < 3:
    #     os.chdir("/home/student")
    #     os.popen("sudo -S %s" % ("python3 green.py"), 'w').write('student')
    #     sleep(1)
    #     x = x + 1
    os.chdir("/home/student")
    os.popen("sudo -S %s" % ("python3 rainbowTry.py"), 'w').write('student')
    sleep(7.5)

def led_green():
    os.chdir("/home/student")
    os.popen("sudo -S %s" % ("python3 green.py"), 'w').write('student')
    sleep(5)

while True:
    jason = request()
    print("request successfully")
    led_state = int(jason[0]['led_state'])
    print("led: ", led_state)
    timer = int(jason[0]['timer'])
    print("timer: ", timer)
    if led_state == 1:
        led_ring()
        os.chdir("/home/student")
        os.popen("sudo -S %s" % ("python3 disable.py"), 'w').write('student')
        sleep(0.01)
        led_green()
        # sleep(timer)
    else:
        os.chdir("/home/student")
        os.popen("sudo -S %s" % ("python3 disable.py"), 'w').write('student')
