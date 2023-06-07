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
from pymeasure.instruments.agiltron.agiltronMEMS1xN import AgiltronMEMS1xN
import pyvisa
import logging
import time

log = logging.getLogger("")
log.addHandler(logging.NullHandler())


if __name__ == "__main__":
    # port = 23
    # uname = "root"
    # passwd = "fs19681086"
    # host = f"192.168.1.200"
    switch = AgiltronMEMS1xN()

    switch.switch_channel(1)
    switch.switch_channel(2)
    switch.switch_channel(3)
    switch.switch_channel(4)
    switch.switch_channel(5)
    switch.switch_channel(6)
    switch.switch_channel(7)
    switch.switch_channel(8)
    switch.switch_channel(9)
    switch.switch_channel(10)
    switch.switch_channel(11)
    switch.switch_channel(12)
    switch.switch_channel(13)
    switch.switch_channel(14)
    switch.switch_channel(15)
    switch.switch_channel(16)

    # success_ = switch.read()
    # print(success_)

    power_in_dbm = -0.01
    power_out_patch = -0.15
    power_out_ch1_dbm = -1.51 - power_out_patch
    power_out_ch2_dbm = -1.47 - power_out_patch
    power_out_ch3_dbm = -1.56 - power_out_patch
    power_out_ch4_dbm = -1.29 - power_out_patch
    power_out_ch5_dbm = -0.98 - power_out_patch
    power_out_ch6_dbm = -1.24 - power_out_patch
    power_out_ch7_dbm = -1.03 - power_out_patch
    power_out_ch8_dbm = -1.37 - power_out_patch
    power_out_ch9_dbm = -2.01 - power_out_patch
    power_out_ch10_dbm = -1.39 - power_out_patch
    power_out_ch11_dbm = -1.21 - power_out_patch
    power_out_ch12_dbm = -1.50 - power_out_patch
    power_out_ch13_dbm = -0.98 - power_out_patch
    power_out_ch14_dbm = -1.43 - power_out_patch
    power_out_ch15_dbm = -1.78 - power_out_patch
    power_out_ch16_dbm = -1.00 - power_out_patch

    power_out_array = [
        power_out_ch1_dbm,
        power_out_ch2_dbm,
        power_out_ch3_dbm,
        power_out_ch4_dbm,
        power_out_ch5_dbm,
        power_out_ch6_dbm,
        power_out_ch7_dbm,
        power_out_ch8_dbm,
        power_out_ch9_dbm,
        power_out_ch10_dbm,
        power_out_ch11_dbm,
        power_out_ch12_dbm,
        power_out_ch13_dbm,
        power_out_ch14_dbm,
        power_out_ch15_dbm,
        power_out_ch16_dbm,
    ]
    print(float([format(power_out_array[x], ".2f") for x in range(0, len(power_out_array))]))
    ...
