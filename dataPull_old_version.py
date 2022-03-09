from time import sleep

from gpiozero import MCP3008, Button, LED

button = Button(17)
led = LED(27)
pot = MCP3008(0)

stable_test = 0.0
last_weight = 0
stable_counter = 0
difference = 0


def main():
    measurement = round(pot.value,3)
    weight_kg = (measurement - 0.333) * (1075 / (840 - 333))
    if weight_kg < 0:
        weight_kg = 0.0
    print("new weight:", round(weight_kg,3))
    sleep(2)


while True:
    main()