from time import sleep
from gpiozero import MCP3008, Button, LED
import requests
import datetime
import os
import time

button = Button(17)
led = LED(27)
pot = MCP3008(0)

stable_test = 0.0
last_weight = 0
stable_counter = 0
difference = 0
justDrank = False
lastTime = time.time()


def send_data(last_weight_value, difference_value):
    global justDrank
    today = datetime.datetime.now()
    date = str(today.strftime("%Y-%m-%d"))
    time = str(today.strftime("%X"))
    url = "https://studev.groept.be/api/a21ib2d02/water_insert/" + date + "/" + time + "/" + str(last_weight_value) + "/" + str(difference_value)
    requests.get(url)
    # justDrank = True


def request_data():
    url = "https://studev.groept.be/api/a21ib2d02/led_get"
    return requests.get(url).json()


def process(new_data):
    print("new_data is:", new_data)
    if not compare(new_data, last_weight) and not new_data == 0:
        stable(new_data)
    sleep(2)


def compare(new_weight, to_compare):
    if -0.005 < new_weight - to_compare < 0.005:
        return True
    else:
        return False


def stable(new_weight):
    global stable_counter
    global stable_test
    global last_weight
    global difference
    global justDrank
    if stable_counter == 0:
        stable_counter = 1
        stable_test = new_weight
    else:
        if not compare(new_weight, stable_test):
            stable_counter = 0
        else:
            stable_counter = stable_counter + 1
            if stable_counter == 3:
                difference = last_weight - new_weight
                last_weight = new_weight
                print("Send new difference sent to database:", difference)
                send_data(last_weight, difference)
                if difference>0.01:
                    justDrank = True


def led_red():
    os.chdir("/home/student")
    os.popen("sudo -S %s" % ("python3 red.py"), 'w').write('student')
    sleep(0.1)


def led_green():
    os.chdir("/home/student")
    os.popen("sudo -S %s" % ("python3 green.py"), 'w').write('student')
    sleep(0.1)

def main():
    measurement = round(pot.value,3)
    # print(measurement)
    weight_kg = (measurement - 0.340) * (360 / (451 - 340))
    if weight_kg < 0:
        weight_kg = 0.0
    process(round(weight_kg,3))


os.chdir("/home/student")
os.popen("sudo -S %s" % ("python3 disable.py"), 'w').write('student')
sleep(0.1)

initialized = False
stop_threads = False
while True:
    button.wait_for_release()
    button.wait_for_press()
    jason = request_data()
    interval = int(jason[0]['timer'])
    led_green()
    power = True
    led.on()
    stop_threads = False
    while power:
        main()
        currentTime = time.time()
        jason = request_data()
        if int(jason[0]['led_state']) == 0:
            os.chdir("/home/student")
            os.popen("sudo -S %s" % ("python3 disable.py"), 'w').write('student')
            sleep(0.1)
        else:
            if justDrank:
                led_green()
                lastTime = currentTime
                justDrank = False
            jason = request_data()
            interval = int(jason[0]['timer'])
            if currentTime-lastTime > interval:
                print("in loop to go red")
                led_red()
                lastTime = currentTime
        if button.is_pressed:
            power = False
            led.off()
            stop_threads = True
            os.chdir("/home/student")
            os.popen("sudo -S %s" % ("python3 disable.py"), 'w').write('student')
            sleep(0.1)
            break
