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
    USB = resource_list[0]
    smu = Keithley2230G(USB)

    smu.enable_output = "OFF"

    smu.ch_1.set_voltage(0)
    smu.ch_2.set_voltage(0)
    smu.ch_3.set_voltage(0)

    a = smu.ch_1.measure_voltage()
    b = smu.ch_2.measure_voltage()
    c = smu.ch_3.measure_voltage()

    smu.enable_output = "ON"
    ...
    ...
