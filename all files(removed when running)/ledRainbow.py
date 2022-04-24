import os
import time

os.chdir("/home/student")
os.popen("sudo -S %s"%("python3 disable.py"), 'w').write('student')
while True:
    os.chdir("/home/student")
    os.popen("sudo -S %s"%("python3 rainbowTry.py"), 'w').write('student')
    time.sleep(7.2)

    x = 0
    while x < 10:
        os.chdir("/home/student")
        os.popen("sudo -S %s"%("python3 disable.py"), 'w').write('student')
        time.sleep(0.2)

        os.chdir("/home/student")
        os.popen("sudo -S %s"%("python3 green.py"), 'w').write('student')
        time.sleep(0.2)

        os.chdir("/home/student")
        os.popen("sudo -S %s"%("python3 disable.py"), 'w').write('student')
        time.sleep(0.2)

        os.chdir("/home/student")
        os.popen("sudo -S %s"%("python3 red.py"), 'w').write('student')
        time.sleep(0.2)

        x = x + 1

