from pymeasure.instruments import Instrument, Channel
from pymeasure.instruments.validators import strict_discrete_set, truncated_range

import time
import logging
import numpy as np

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class SMUChannel(Channel):
    def set_voltage(self, voltage):
        self.output_select = self.id
        self.voltage_set = voltage

    def set_voltage_limit(self, voltage_limit):
        self.output_select = self.id
        self.voltage_limit_set = voltage_limit
        self.voltage_limit_state = 1

    def set_current(self, current):
        self.output_select = self.id
        self.current_set = current

    def set_current_limit(self, current_limit):
        self.output_select = self.id
        self.current_limit_set = current_limit
        self.current_limit_state = 1

    def measure_current(self):
        """#! finish"""
        self.output_select = self.id
        current = self.ask(f"FETC:CURR? CH{self.id}")
        return current

    def measure_power(self):
        """#! finish"""
        self.output_select = self.id
        power = self.ask(f"FETC:POW? CH{self.id}")
        return power

    def measure_voltage(self):
        """#! finish"""
        self.output_select = self.id
        voltage = self.ask(f"FETC:VOLT? CH{self.id}")
        return voltage

    voltage_set = Instrument.control(
        "VOLT?",
        "VOLT %f",
        """  .""",  #! finish
    )

    voltage_limit_set = Instrument.control(
        "VOLT:LIM?",
        "VOLT:LIM %f",
        """  .""",  #! finish
    )

    voltage_limit_state = Instrument.control(
        "VOLT:LIM:STAT?",
        "VOLT:LIM:STAT %s",
        """  .""",  #! finish
    )

    current_set = Instrument.control(
        "CURR?",
        "CURR %f",
        """  .""",  #! finish
    )

    current_limit_set = Instrument.control(
        "CURR:LIM?",
        "CURR:LIM %f",
        """  .""",  #! finish
    )

    current_limit_state = Instrument.control(
        "CURR:LIM:STAT?",
        "CURR:LIM:STAT %s",
        """  .""",  #! finish
    )

    output_select = Instrument.control(
        "INST?",
        "INST CH%d",
        """#! finsih, implement range
    """,
        # validator=strict_discrete_set,
        # values={0: 0, 1: 1, "OFF": 0, "ON": 1},
        # map_values=True,
    )

    def insert_id(self, command):
        if command[0:4] in ["INST", "VOLT", "CURR", "FETC"]:
            print(command + "subclass")
            return command
        else:
            return "C%d:%s" % (self.id, command)

    # def configure(self, channel: int, voltage: float, compliance: float, enable: bool) -> None:
    #     assert channel in [1, 2, 3]
    #     self.inst.write(f"INST:SEL CH{channel}")
    #     self.inst.write(f"SOURCE:VOLT {voltage}V")
    #     self.inst.write(f"SOURCE:CURR {compliance}A")
    #     if enable:
    #         self.inst.write("SOURCE:OUTP:ENAB ON")
    #     else:
    #         self.inst.write("SOURCE:OUTP:ENAB OFF")

    # def set_output(self, state: bool):
    #     if state:
    #         self.inst.write("SOURCE:OUTP ON")
    #     else:
    #         self.inst.write("SOURCE:OUTP OFF")

    # def measure_voltage(self, channel: int) -> float:
    #     assert channel in [1, 2, 3]
    #     self.inst.write(f"INST:SEL CH{channel}")
    #     return float(self.inst.query(f"MEAS:VOLT? CH{channel}"))

    # def measure_current(self, channel: int) -> float:
    #     assert channel in [1, 2, 3]
    #     self.inst.write(f"INST:SEL CH{channel}")
    #     return float(self.inst.query(f"MEAS:CURR? CH{channel}"))

    # def enable_front_panel_keys(self):
    #     self.inst.write("SYST:LOC")
    #     del self.inst
    #     print("Please reconnect or reset next time")


class Keithley2230G(Instrument):
    """Represents the Keithley 2600 series (channel A and B) SourceMeter"""

    WRITE_INTERVAL_S = 0.02

    channels = Instrument.ChannelCreator(SMUChannel, (1, 2, 3))

    def __init__(self, adapter, name="Keithley 2600 SourceMeter", **kwargs):
        super().__init__(adapter, name, **kwargs)

        self._seconds_since_last_write = 0
        if self.adapter.connection is not None:
            self.adapter.connection.timeout = 3000
        # self.Ch1 = Channel(self, "1")
        # self.Ch2 = Channel(self, "2")
        # self.Ch3 = Channel(self, "3")
        # determine what model this scope is
        (self.manufacturer, self.model, self.serial_number, self.firmware_version) = self.ask("*IDN?").split(",")

        if self.model.strip() != "2230G-30-1":
            raise Exception("Wrong instrument requested.")

    def write(self, command, **kwargs):
        """Writes the command to the instrument through the adapter.
        Note.
        If the last command was sent less than WRITE_INTERVAL_S before, this method blocks for
        the remaining time so that commands are never sent with rate more than 1/WRITE_INTERVAL_S
        Hz.

        :param command: command string to be sent to the instrument
        """
        seconds_since_last_write = time.monotonic() - self._seconds_since_last_write
        if seconds_since_last_write < self.WRITE_INTERVAL_S:
            time.sleep(self.WRITE_INTERVAL_S - seconds_since_last_write)
            self._seconds_since_last_write = seconds_since_last_write
        super().write(command, **kwargs)

    @property
    def error(self):
        """Returns a tuple of an error code and message from a
        single error."""
        err = self.ask("print(errorqueue.next())")
        err = err.split("\t")
        # Keithley Instruments Inc. sometimes on startup
        # if tab delimitated message is greater than one, grab first two as code, message
        # otherwise, assign code & message to returned error
        if len(err) > 1:
            err = (int(float(err[0])), err[1])
            code = err[0]
            message = err[1].replace('"', "")
        else:
            code = message = err[0]
        log.info(f"ERROR {str(code)},{str(message)} - len {str(len(err))}")
        return (code, message)

    def check_errors(self):
        """Logs any system errors reported by the instrument."""
        code, message = self.error
        while code != 0:
            t = time.time()
            log.info("Keithley 2600 reported error: %d, %s" % (code, message))
            code, message = self.error
            if (time.time() - t) > 10:
                log.warning("Timed out for Keithley 2600 error retrieval.")

    enable_output = Instrument.control(
        "SOURCE:OUTP?",
        "SOURCE:OUTP %d",
        """#! finsih
        """,
        validator=strict_discrete_set,
        values={0: 0, 1: 1, "OFF": 0, "ON": 1},
        map_values=True,
    )

    def measure_all_current(self):
        """#! finish"""
        current = self.ask(f"FETC:CURR? ALL")
        return current

    def measure_all_power(self):
        """#! finish"""
        power = self.ask(f"FETC:POW? ALL")
        return power

    def measure_all_voltage(self):
        """#! finish"""
        voltage = self.ask(f"FETC:VOLT? ALL")
        return voltage

    def insert_id(self, command):
        if command[0:4] in ["SOUR", "FETC"]:
            # print(command + "subclass")
            return command
        else:
            return "C%d:%s" % (self.id, command)
