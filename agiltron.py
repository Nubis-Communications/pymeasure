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

    switch.switch_channel(4)
    switch.switch_channel(5)
    switch.switch_channel(6)

    # success_ = switch.read()
    # print(success_)
    ...
