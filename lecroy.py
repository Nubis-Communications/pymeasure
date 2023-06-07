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
from pymeasure.instruments.lecroy.lecroyLabMaster10ZiA import LabMaster10ZiA
import pyvisa
import logging
import time

log = logging.getLogger("")
log.addHandler(logging.NullHandler())


if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    resource_list = rm.list_resources()
    # ip = resource_list[0]
    ip = "TCPIP::10.1.10.85::inst0::INSTR"
    scope = LabMaster10ZiA(ip)
    # scope.autosetup()

    scope.trig_setup("auto")
    scope.trigger_select = "c2"

    scope.ch_1.toggle_trace("off")
    scope.ch_2.toggle_trace("on")
    scope.ch_3.toggle_trace("on")

    scope.ch_2.select_inputAB("B")
    scope.ch_3.select_inputAB("B")

    sampleRate = 160e9
    # maxSamples = 8e6
    maxSamples = 32e3
    scope.set_memory_depth(maxSamples, sampleRate)

    scope.ch_2.set_vertical_scale(640e-3)  #! 80*8 = 640mV -> max range
    scope.ch_3.set_vertical_scale(640e-3)  #! 80*8 = 640mV -> max range

    time.sleep(5)
    type = "mean"
    C2_mean = scope.ch_2.get_measurement(type, "P1")
    C3_mean = scope.ch_3.get_measurement(type, "P2")

    type = "pkpk"
    C2_vpp = scope.ch_2.get_measurement(type, "P3")
    C3_vpp = scope.ch_3.get_measurement(type, "P4")

    scope.ch_2.set_vertical_scale_variable(True)
    scope.ch_3.set_vertical_scale_variable(True)


    scope.ch_2.set_vertical_offset(C2_mean)
    scope.ch_3.set_vertical_offset(C3_mean)

    scope.ch_2.set_vertical_scale(C2_vpp)
    scope.ch_3.set_vertical_scale(C3_vpp)
