from time import sleep
from gpiozero import MCP3008, Button, LED
import requests
import datetime

button = Button(17)
led = LED(27)
pot = MCP3008(0)

stable_test = 0.0
last_weight = 0
stable_counter = 0
difference = 0


def send_data(last_weight_value, difference_value):
    today = datetime.datetime.now()
    date = str(today.strftime("%Y-%m-%d"))
    time = str(today.strftime("%X"))
    url = "https://studev.groept.be/api/a21ib2d02/insert_water/" + date + "/" + time + "/" + str(last_weight_value) + "/" + str(difference_value)
    requests.get(url)


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
                print("data sent to database:", last_weight)
                send_data(last_weight, difference)
                print("sent succesfully")


def main():
    measurement = round(pot.value,3)
    # print(measurement)
    weight_kg = (measurement - 0.333) * (360 / (451 - 333))
    if weight_kg < 0:
        weight_kg = 0.0
    process(round(weight_kg,3))


while True:
    main()

# while True:
#     button.wait_for_release()
#     button.wait_for_press()
#     power = True
#     led.on()
#     while power:
#         main()
#         if button.is_pressed:
#             power = False
#             led.off()
#             break
