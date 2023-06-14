"""
This example demonstrates how to make a graphical interface, and uses
a random number generator to simulate data so that it does not require
an instrument to use.

Run the program by changing to the directory containing this file and calling:

python gui.py

"""

# import sys
# import random
# import tempfile
# from time import sleep

# from datetime import datetime, timedelta

# from pymeasure.experiment import Procedure, IntegerParameter, Parameter, FloatParameter
from pymeasure.instruments.keithley.keithley2230G import Keithley2230G
import pyvisa
import logging
import time
import numpy as np

log = logging.getLogger("")
log.addHandler(logging.NullHandler())


if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    resource_list = rm.list_resources()
    # print(resource_list)
    usb = resource_list[0]
    smu = Keithley2230G(usb)

    smu.enable_output = "OFF"

    smu.ch_1.set_voltage(12)
    smu.ch_2.set_voltage(0)
    # smu.ch_3.set_voltage(0)

    # a = smu.ch_1.measure_voltage()
    b = smu.ch_2.measure_voltage()
    # c = smu.ch_3.measure_voltage()

    smu.enable_output = "ON"

    inputnominal0v = smu.ch_2.measure_voltage()
    ...
    minVoltage = 0
    maxVoltage = 5
    step = 0.1
    num = int((maxVoltage - minVoltage) / step)
    vals = np.linspace(minVoltage, maxVoltage, num + 1)

    for i in vals:
        smu.ch_2.set_voltage(i)
        check = smu.ch_2.measure_voltage()
        input()

    ...
    ...


# power =[
# 
17.02 17.01 17.02 17.02 17.03 17.04 17.05 17.05 17.05 17.05 
17.05 17.03 17.01 16.98 16.93 16.88 16.80 16.70 16.58 16.43
16.24 16.01 15.76 15.46 15.10 14.68 14.21 13.67 13.05 12.35
11.55 10.69 09.66 08.59 07.59 06.31 04.89 03.40 01.80 00.09
-1.61 -3.51 -5.40 -7.34 -9.31 -11.33 -13.33 -15.23 -17.12 -18.76 -20.27
# ]
