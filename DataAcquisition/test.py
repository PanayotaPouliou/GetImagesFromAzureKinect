import os
import time

x = range(0, 10)
for n in x:
    os.system('python DataAcquisition\getDataImplementationGuide.py')
    time.sleep(10)
    print(n)
