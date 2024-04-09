# -----------------------------------------------------------------------------
# Summary:		Implementation of LeCroyDSO Control class
# Authors:		Ashok Bruno
# Started:		10/21/2022
# Copyright 2022-2025 Nubis Communications Corporation. All Rights Reserved.
# -----------------------------------------------------------------------------


from pymeasure.instruments import Instrument, Channel
from pymeasure.instruments.validators import strict_discrete_set, strict_range
import time
import re
import sys
import numpy as np

# ------------------------------------------------------------------------------------


def _math_define_validator(value, values):
    """
    Validate the input of the math_define property
    :param value: input parameters as a 3-element tuple
    :param values: allowed space for each parameter
    """
    if not isinstance(value, tuple):
        raise ValueError("Input value {} of trigger_select should be a tuple".format(value))
    if len(value) != 3:
        raise ValueError("Number of parameters {} different from 3".format(len(value)))
    output = (sanitize_source(value[0]), value[1], sanitize_source(value[2]))
    for i in range(3):
        strict_discrete_set(output[i], values=values[i])
    return output


def sanitize_source(source):
    """Parse source string

    :param source can be "cX", "ch X", "chan X", "channel X", "math" or "line", where X is
    a single digit integer. The parser is case and white space insensitive.
    :return: can be "C1", "C2", "C3", "C4", "MATH" or "LINE."""

    match = re.match(r"^\s*(C|CH|CHAN|CHANNEL)\s*(?P<number>\d)\s*$|" r"^\s*(?P<name_only>MATH|LINE)\s*$", source, re.IGNORECASE)
    if match:
        if match.group("number") is not None:
            source = "C" + match.group("number")
        else:
            source = match.group("name_only")
        source = source.upper()
    else:
        raise ValueError(f"source {source} not recognized")
    return source


class ScopeChannel(Channel):
    """Implementation of a LeCroy T3DSO1204 Oscilloscope channel.

    Implementation modeled on Channel object of Keysight DSOX1102G instrument."""

    _BOOLS = {True: "ON", False: "OFF"}

    bwlimit = Instrument.control(
        "BWL?",
        "BWL %s",
        """ Toggles the 20 MHz internal low-pass filter. (strict bool)""",
        validator=strict_discrete_set,
        values=_BOOLS,
        map_values=True,
    )

    coupling = Instrument.control(
        "CPL?",
        "CPL %s",
        """ A string parameter that determines the coupling ("ac 1M", "dc 1M", "ground").""",
        validator=strict_discrete_set,
        values={"ac 1M": "A1M", "dc 1M": "D1M", "ground": "GND"},
        map_values=True,
    )

    display = Instrument.control(
        "TRA?",
        "TRA %s",
        """Control the display enabled state. (strict bool)""",
        validator=strict_discrete_set,
        values=_BOOLS,
        map_values=True,
    )

    # invert = Instrument.control("INVS?", "INVS %s", """ Toggles the inversion of the input signal. (strict bool)""", validator=strict_discrete_set, values=_BOOLS, map_values=True)

    offset = Instrument.control(
        "OFST?",
        "OFST %.2EV",
        """ A float parameter to set value that is represented at center of screen in
        Volts. The range of legal values varies depending on range and scale. If the specified
        value is outside of the legal range, the offset value is automatically set to the nearest
        legal value.
        """,
    )

    # skew_factor = Instrument.control(
    #     "SKEW?",
    #     "SKEW %.2ES",
    #     """ Channel-to-channel skew factor for the specified channel. Each analog channel can be
    #     adjusted + or -100 ns for a total of 200 ns difference between channels. You can use
    #     the oscilloscope's skew control to remove cable-delay errors between channels.
    #     """,
    #     validator=strict_range,
    #     values=[-1e-7, 1e-7],
    #     preprocess_reply=lambda v: v.rstrip("S"),
    # )

    probe_attenuation = Instrument.control(
        "ATTN?",
        "ATTN %g",
        """ A float parameter that specifies the probe attenuation. The probe attenuation
        may be from 0.1 to 10000.""",
        validator=strict_discrete_set,
        values={0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000},
    )

    unit = Instrument.control(
        "UNIT?",
        "UNIT %s",
        """ Unit of the specified trace. Measurement results, channel sensitivity, and trigger
        level will reflect the measurement units you select. ("A" for Amperes, "V" for Volts).""",
        validator=strict_discrete_set,
        values=["A", "V"],
    )

    trigger_coupling = Instrument.control(
        "TRCP?",
        "TRCP %s",
        """ A string parameter that specifies the input coupling for the selected trigger sources.
        • ac    — AC coupling block DC component in the trigger path, removing dc offset voltage
                  from the trigger waveform. Use AC coupling to get a stable edge trigger when
                  your waveform has a large dc offset.
        • dc    — DC coupling allows dc and ac signals into the trigger path.
        • lowpass  — HFREJ coupling places a lowpass filter in the trigger path.
        • highpass — LFREJ coupling places a highpass filter in the trigger path.
        """,
        validator=strict_discrete_set,
        values={"ac": "AC", "dc": "DC", "lowpass": "HFREJ", "highpass": "LFREJ"},
        map_values=True,
    )

    trigger_level = Instrument.control(
        "TRLV?",
        "TRLV %.2EV",
        """ A float parameter that sets the trigger level voltage for the active trigger source.
            When there are two trigger levels to set, this command is used to set the higher
            trigger level voltage for the specified source. :attr:`trigger_level2` is used to set
            the lower trigger level voltage.
            When setting the trigger level it must be divided by the probe attenuation. This is
            not documented in the datasheet and it is probably a bug of the scope firmware.
            An out-of-range value will be adjusted to the closest legal value.
        """,
    )

    # trigger_level2 = Instrument.control(
    #     "TRLV2?",
    #     "TRLV2 %.2EV",
    #     """ A float parameter that sets the lower trigger level voltage for the specified source.
    #     Higher and lower trigger levels are used with runt/slope triggers.
    #     When setting the trigger level it must be divided by the probe attenuation. This is
    #     not documented in the datasheet and it is probably a bug of the scope firmware.
    #     An out-of-range value will be adjusted to the closest legal value.
    #     """,
    # )

    trigger_slope = Instrument.control(
        "TRSL?",
        "TRSL %s",
        """ A string parameter that sets the trigger slope of the specified trigger source.
        <trig_slope>:={NEG,POS,WINDOW} for edge trigger.
        <trig_slope>:={NEG,POS} for other trigger
        """,
        validator=strict_discrete_set,
        values={"negative": "NEG", "positive": "POS", "window": "WINDOW"},
        map_values=True,
    )

    _measurable_parameters = [
        "PKPK",
        "MAX",
        "MIN",
        "AMPL",
        "TOP",
        "BASE",
        "CMEAN",
        "MEAN",
        "RMS",
        "CRMS",
        "OVSN",
        "FPRE",
        "OVSP",
        "RPRE",
        "PER",
        "FREQ",
        "PWID",
        "NWID",
        "RISE",
        "FALL",
        "WID",
        "DUTY",
        "NDUTY",
        "ALL",
    ]

    display_parameter = Instrument.setting(
        "PACU %s",
        """Set the waveform processing of this channel with the specified algorithm and the result
        is displayed on the front panel. The command accepts the following parameters:
        Parameter   Description
        PKPK        vertical peak-to-peak
        MAX         maximum vertical value
        MIN         minimum vertical value
        AMPL        vertical amplitude
        TOP         waveform top value
        BASE        waveform base value
        CMEAN       average value in the first cycle
        MEAN        average value
        RMS         RMS value
        CRMS        RMS value in the first cycle
        OVSN        overshoot of a falling edge
        FPRE        preshoot of a falling edge
        OVSP        overshoot of a rising edge
        RPRE        preshoot of a rising edge
        PER         period
        FREQ        frequency
        PWID        positive pulse width
        NWID        negative pulse width
        RISE        rise-time
        FALL        fall-time
        WID         Burst width
        DUTY        positive duty cycle
        NDUTY       negative duty cycle
        ALL         All measurement """,
        validator=strict_discrete_set,
        values=_measurable_parameters,
    )

    def get_measurement(self, type, position):
        """finish"""  #! finish, create dictionary for measurements"""

        if type == "mean":
            typeIdx = 7
        elif type == "pkpk":
            typeIdx = 3
        self.set_meas_param = (position, typeIdx)
        opc = int(self.ask("*OPC?"))
        while not opc:
            int(self.ask("*OPC?"))
        print(opc)

        self.set_meas_channel = (position, self.id - 1)
        opc = int(self.ask("*OPC?"))
        while not opc:
            int(self.ask("*OPC?"))
        print(opc)
        # turn on view
        # self.write(f"VBS 'app.Measure.{position}.View=1'")

        value = self.get_meas_value(position)
        # turn off view
        self.write(f"VBS 'app.Measure.{position}.View=0'")

        opc = int(self.ask("*OPC?"))
        while not opc:
            int(self.ask("*OPC?"))

        return value

    def get_meas_value(self, position):
        """#! finish"""
        return self.ask(f"VBS? 'return=app.Measure.{position}.Out.Result.Value'")

    set_meas_param = Instrument.control(
        "VBS? 'return=app.Measure.%s.ParamEngine=%d'",
        "VBS 'app.Measure.%s.ParamEngine=%d",
        """  .""",  #! finish
    )

    # set_meas_view = Instrument.control(
    #     "VBS? 'return=app.Measure.%s.View=%d",
    #     "VBS 'app.Measure.%s.View=%d'",
    #     """  .""",  #! finish
    # )

    # meas_value = Instrument.control(
    #     "VBS? 'return=app.Measure.%s.Out.Result.Value'",
    #     "VBS 'app.Measure.%s.Out.Result.Value'",
    #     """  .""",  #! finish
    # )

    set_meas_channel = Instrument.control(
        "VBS? 'return=app.Measure.%s.Source1=ch'",
        "VBS 'app.Measure.%s.Source1=%s'",
        """  .""",  #! finish
    )

    def set_vertical_scale(self, yscale):
        """finish"""  #! finish
        yrange = (float(yscale) / 0.95) / 8
        self.vertical_scale = yrange

    vertical_scale = Instrument.control(
        "VBS? 'return=app.Acquisition.ch.VerScale",
        "VBS 'app.Acquisition.ch.VerScale=%f",
        """  A float parameter that specifies the vertical scale (units per division) in Volts.""",  #! finish
    )

    def measure_parameter(self, parameter: str):
        """Process a waveform with the selected algorithm and returns the specified measurement.
        :param parameter: same as the display_parameter property
        """
        parameter = strict_discrete_set(value=parameter, values=self._measurable_parameters)
        output = self.ask("PAVA? %s" % parameter)
        match = re.match(r"^\s*(?P<parameter>\w+),\s*(?P<value>.*)\s*$", output)
        if match:
            if match.group("parameter") != parameter:
                raise ValueError(f"Parameter {match.group('parameter')} different from {parameter}")
            return float(match.group("value"))
        else:
            raise ValueError(f"Cannot extract value from output {output}")

    def set_vertical_scale_variable(self, truefalse):
        """finish"""  #! finish
        self.write(f"VBS 'app.Acquisition.ch.VerScaleVariable={truefalse}'")

    def set_vertical_offset(self, yscale):
        """finish"""  #! finish
        yrange = -float(yscale)
        self.vertical_offset = yrange

    vertical_offset = Instrument.control(
        "VBS? 'return=app.Acquisition.ch.VerOffset=%f'",
        "VBS 'app.Acquisition.ch.VerOffset=%f",
        """  .""",  #! finish
    )

    def select_inputAB(self, input):
        """#! finish."""

        # ! maybe use self.sanitize_source
        if self.id not in [2, 3]:
            raise Exception("Channel must be either 2 or 3, not 1 or 4.")

        if input.upper() in ["B", "INPUTB"]:
            input = 1
        elif input.upper() in ["A", "INPUTA"]:
            input = 0
        else:
            raise Exception("Input A or B only")

        self.input_select = input
        opc = int(self.ask("*OPC?"))
        while not opc:
            int(self.ask("*OPC?"))
        print(opc)

    input_select = Instrument.control(
        "VBS? 'return=app.Acquisition.ch.ActiveInput'",
        "VBS 'app.Acquisition.ch.ActiveInput=%d'",
        """ #! TODO: finish """,
        # validator=strict_discrete_set,
        # values={0: "InputA", 1: "InputB"},
        # map_values=True,
    )

    def toggle_trace(self, trace_status):
        """Starts repetitive acquisitions.

        This is the same as pressing the Run key on the front panel.
        """
        self.trace = trace_status

    trace = Instrument.control(
        "TRA?",
        "TRA %s",
        """ A string parameter that specifies whether a channel is on or off.
        • The first input is the channel
        • The first input is 'on' or 'off'
        This property is set by a tuple.
        """,
    )

    def insert_id(self, command):
        # only in case of the BWL and PACU commands the syntax is different. Why? SIGLENT Why?
        if command[0:4] == "VBS ":
            return command.replace(".ch.", ".C%d." % (self.id))
        elif command[0:5] == "PACU ":
            return "PACU %s,C%d" % (command[5:], self.id)
        else:
            return "C%d:%s" % (self.id, command)

    # noinspection PyIncorrectDocstring
    def setup(self, **kwargs):
        """Setup channel. Unspecified settings are not modified. Modifying values such as
        probe attenuation will modify offset, range, etc. Refer to oscilloscope documentation and
        make multiple consecutive calls to setup() if needed.

        :param bwlimit: A boolean, which enables 20 MHz internal low-pass filter.
        :param coupling: "AC 1M", "DC 1M", "ground".
        :param display: A boolean, which enables channel display.
        :param invert: A boolean, which enables input signal inversion.
        :param offset: Numerical value represented at center of screen, must be inside
                       the legal range.
        :param skew_factor: Channel-tochannel skew factor from -100ns to 100ns.
        :param probe_attenuation: Probe attenuation values from 0.1 to 1000.
        :param scale: Units per division.
        :param unit: Unit of the specified trace: "A" for Amperes, "V" for Volts
        :param trigger_mode: specifies the trigger mode for the selected source
        :param trigger_coupling: input coupling for the selected trigger sources
        :param trigger_level: trigger level voltage for the active trigger source
        :param trigger_level2: trigger lower level voltage for the active trigger source (only
                               SLEW/RUNT trigger)
        :param trigger_slope: trigger slope of the specified trigger source
        #! TODO: add all modified triggers etc
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def current_configuration(self):
        """Read channel configuration as a dict containing the following keys:
        - "channel": channel number (int)
        - "attenuation": probe attenuation (float)
        - "bandwidth_limit": bandwidth limiting enabled (bool)
        - "coupling": "ac 1M", "dc 1M", "ground" coupling (str)
        - "offset": vertical offset (float)
        - "skew_factor": channel-tochannel skew factor (float)
        - "display": currently displayed (bool)
        - "unit": "A" or "V" units (str)
        - "volts_div": vertical divisions (float)
        - "inverted": inverted (bool)
        - "trigger_coupling": trigger coupling can be "dc" "ac" "highpass" "lowpass" (str)
        - "trigger_level": trigger level (float)
        - "trigger_level2": trigger lower level for SLEW or RUNT trigger (float)
        - "trigger_slope": trigger slope can be "negative" "positive" "window" (str)
        """

        ch_setup = {
            "channel": self.id,
            "attenuation": self.probe_attenuation,
            "bandwidth_limit": self.bwlimit,
            "coupling": self.coupling,
            "offset": self.offset,
            "skew_factor": self.skew_factor,
            "display": self.display,
            "unit": self.unit,
            "inverted": self.invert,
            "trigger_coupling": self.trigger_coupling,
            "trigger_level": self.trigger_level,
            "trigger_level2": self.trigger_level2,
            "trigger_slope": self.trigger_slope,
        }
        return ch_setup


class LabMaster10ZiA(Instrument):
    """Represents the LeCroy LabMaster 10 Zi-A Oscilloscope interface for interacting with the instrument.

    Refer to the LeCroy LabMaster 10 Zi-A Oscilloscope Programmer's Guide for further details about using the lower-level methods to interact directly with the scope.

    Attributes:

    .. code-block:: python

        scope = LabMaster10ZiA(resource)
        scope.autoscale()
        ch1_data_array, ch1_preamble = scope.download_waveform(source="C1", points=2000)
        # ...
        scope.shutdown()
    """

    WRITE_INTERVAL_S = 0.02

    channels = Instrument.ChannelCreator(ScopeChannel, (1, 2, 3, 4))

    def __init__(self, adapter, name="LeCroy LabMaster 10 Zi-A Oscilloscope", **kwargs):
        super().__init__(adapter, name, **kwargs)
        if self.adapter.connection is not None:
            self.adapter.connection.timeout = 15000

        self._grid_number = 14  # Number of grids in the horizontal direction
        self._seconds_since_last_write = 0
        self.waveform_source = "C1"
        self._header_size = 16  # bytes
        self._footer_size = 2  # bytes
        self.default_setup()

        # determine what model this scope is
        (self.manufacturer, self.model, self.serial_number, self.firmware_version) = self.ask("*IDN?").split(",")

        if self.model != "MCM-ZI-A":
            raise Exception("Wrong instrument requested.")

    def default_setup(self):
        """Set up the oscilloscope for remote operation.

        The COMM_HEADER command controls the way the oscilloscope formats response to queries. This command does not affect the interpretation of messages sent to the oscilloscope. Headers can be sent in their long or short form regardless of the CHDR setting.
        By setting the COMM_HEADER to OFF, the instrument is going to reply with minimal information, and this makes the response message much easier to parse.
        The user should not be fiddling with the COMM_HEADER during operation, because if the communication header is anything other than OFF, the whole driver breaks down.
        """
        self._comm_header = "OFF"
        self.write(r"""vbs 'app.settodefaultsetup' """)

    def autosetup(self):
        """Autoscale displayed channels."""
        self.write("ASET")

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

    # def values(self, command, **kwargs):
    #     """Reads a set of values from the instrument through the adapter,
    #     passing on any key-word arguments.
    #     """
    #     return self.instrument.values(":channel%d:%s" % (self.number, command), **kwargs)

    # def values(self, command, separator=",", cast=float, preprocess_reply=None):
    #     """Write a command to the instrument and return a list of formatted
    #     values from the result.

    #     :param command: SCPI command to be sent to the instrument
    #     :param separator: A separator character to split the string into a list
    #     :param cast: A type to cast the result
    #     :param preprocess_reply: optional callable used to preprocess values
    #         received from the instrument. The callable returns the processed
    #         string.
    #     :returns: A list of the desired type, or strings where the casting fails
    #     """
    #     results = str(self.ask(command)).strip()
    #     if callable(preprocess_reply):
    #         results = preprocess_reply(results)
    #     results = results.split(separator)
    #     for i, result in enumerate(results):
    #         try:
    #             if cast == bool:
    #                 # Need to cast to float first since results are usually
    #                 # strings and bool of a non-empty string is always True
    #                 results[i] = bool(float(result))
    #             else:
    #                 results[i] = cast(result)
    #         except Exception:
    #             pass  # Keep as string
    #     return results

    def set_timebase_scale(self, timebase):
        """#! finish."""
        numDivisions = 10
        total_timebase = timebase / numDivisions
        total_timebase=np.round(total_timebase,12)
        self.timebase_scale = total_timebase

    def set_memory_depth(self, maxSamples:int, sampleRate:int):
        """#! finish."""
        timebase = maxSamples / sampleRate
        self.memory_depth = maxSamples
        self.set_timebase_scale(timebase)
        opc = int(self.ask("*OPC?"))
        while not opc:
            int(self.ask("*OPC?"))
        print(opc)

    # def disconnect(self):
    #     if self.connected:
    #         self.connected = False

    # def disconnect_from_dso(self):
    #     self._instr_conn.disconnect()

    _comm_header = Instrument.control(
        "CHDR?",
        "CHDR %s",
        """ Controls the way the oscilloscope formats response to queries.
        The user should not be fiddling with the COMM_HEADER during operation, because if the communication header is anything other than OFF, the whole driver breaks down.
        • SHORT — response starts with the short form of the header word.
        • LONG — response starts with the long form of the header word.
        • OFF — header is omitted from the response and units in numbers are suppressed.""",
        validator=strict_discrete_set,
        values=["OFF", "SHORT", "LONG"],
    )

    ##################
    # Timebase Setup #
    ##################

    timebase_offset = Instrument.control(
        "TRDL?",
        "TRDL %.2ES",
        """ A float parameter that sets the time interval in seconds between the trigger
        event and the reference position (at center of screen by default).""",
    )

    timebase_scale = Instrument.control(
        "VBS? 'return=app.Acquisition.Horizontal.HorScale'",
        "VBS 'app.Acquisition.Horizontal.HorScale=%s'",
        """  # finish  """,
        validator=strict_discrete_set,
        values={
            25e-6: "25e-6",
            20e-6: "20e-6",
            10e-6: "10e-6",
            5e-6: "5e-6",
            2e-6: "2e-6",
            1e-6: "1e-6",
            500e-9: "500e-9",
            200e-9: "200e-9",
            100e-9: "100e-9",
            50e-9: "50e-9",
            20e-9: "20e-9",
            10e-9: "10e-9",
            5e-9: "5e-9",
            2e-9: "2e-9",
            1e-9: "1e-9",
            500e-12: "500e-12",
            200e-12: "200e-12",
            100e-1: "100e-12",
            50e-12: "50e-12",
            20e-12: "20e-12",
        },
    )

    memory_depth = Instrument.control(
        "VBS? 'return=app.Acquisition.Horizontal.MaxSamples'",
        "VBS 'app.Acquisition.Horizontal.MaxSamples=%d'",
        """ # finish .""",
        validator=strict_discrete_set,
        values={
            40e6: "40e6",
            32e6: "32e6",
            16e6: "16e6",
            8e6: "8e6",
            3.2e6: "3.2e6",
            1.6e6: "1.6e6",
            800e3: "800ke3",
            320e3: "320e3",
            160e3: "160e3",
            80e3: "80e3",
            32e3: "32e3",
            16e3: "16e3",
            8e3: "8e3",
            3.2e3: "3.2e3",
            1.6e3: "1.6e3",
            800: "800",
            320: "320",
            160: "160",
            80: "80",
            32: "32",
        },
    )
    # timebase_scale = Instrument.control(
    #     "TDIV?",
    #     "TDIV %.2ES",
    #     """ A float parameter that sets the horizontal scale (units per division) in seconds (S),
    #     for the main window.""",
    #     validator=strict_range,
    #     values=[1e-9, 100],
    # )

    timebase_hor_magnify = Instrument.control(
        "HMAG?",
        "HMAG %.2ES",
        """ A float parameter that sets the zoomed (delayed) window horizontal scale (
        seconds/div). The main sweep scale determines the range for this command. """,
        validator=strict_range,
        values=[1e-9, 20e-3],
    )

    timebase_hor_position = Instrument.control(
        "HPOS?",
        "HPOS %.2ES",
        """ A string parameter that sets the horizontal position in the zoomed (delayed) view of
        the main sweep. The main sweep range and the main sweep horizontal position determine
        the range for this command. The value for this command must keep the zoomed view window
        within the main sweep range.""",
    )

    @property
    def timebase(self):
        """Read timebase setup as a dict containing the following keys:
        - "timebase_scale": horizontal scale in seconds/div (float)
        - "timebase_offset": interval in seconds between the trigger and the reference
        position (float)
        - "timebase_hor_magnify": horizontal scale in the zoomed window in seconds/div (float)
        - "timebase_hor_position": horizontal position in the zoomed window in seconds
        (float)"""
        tb_setup = {
            "timebase_scale": self.timebase_scale,
            "timebase_offset": self.timebase_offset,
            "timebase_hor_magnify": self.timebase_hor_magnify,
            "timebase_hor_position": self.timebase_hor_position,
        }
        return tb_setup

    def timebase_setup(self, scale=None, offset=None, hor_magnify=None, hor_position=None):
        """Set up timebase. Unspecified parameters are not modified. Modifying a single parameter
        might impact other parameters. Refer to oscilloscope documentation and make multiple
        consecutive calls to timebase_setup if needed.

        :param scale: interval in seconds between the trigger event and the reference position.
        :param offset: horizontal scale per division in seconds/div.
        :param hor_magnify: horizontal scale in the zoomed window in seconds/div.
        :param hor_position: horizontal position in the zoomed window in seconds."""

        if scale is not None:
            self.timebase_scale = scale
        if offset is not None:
            self.timebase_offset = offset
        if hor_magnify is not None:
            self.timebase_hor_magnify = hor_magnify
        if hor_position is not None:
            self.timebase_hor_position = hor_position

    ###############
    # Acquisition #
    ###############

    def trig_setup(self, trigger_setup):
        """Starts repetitive acquisitions.

        This is the same as pressing the Run key on the front panel.
        """
        self.trigger_mode = trigger_setup

    def sample_mode(self, samplemode_method):
        """A string parameter that specifies whether a channel is on or off.
        • The first input is the channel
        • The first input is 'on' or 'off'
        This property is set by a tuple.
        """
        self.write(f"VBS 'app.Acquisition.Horizontal.SampleMode = {samplemode_method}'")

    # def set_acquisition_length(self, size):
    #     """Set acquisition sample size. Used mainly for waveform acquisition.

    #     :param size: length of memory size.
    #     :return: acquisition sample size."""
    #     self.write(f"MSIZ {size}")

    # def get_acquisition_length(self):
    #     """Get acquisition sample size for a certain channel.
    #  Used mainly for waveform acquisition.

    #     :param source: channel number of channel name.
    #     :return: acquisition sample size of that channel."""
    #     return self.ask("MSIZ?")

    trigger_mode = Instrument.control(
        "TRMD?",
        "TRMD %s",
        """ A string parameter that specifies the trigger mode for the selected source.
        • auto      — #! TODO complete.
        • normal    — #! TODO complete.
        • single    — #! TODO complete.
        • stop      — #! TODO complete.
        """,
        validator=strict_discrete_set,
        values={"auto": "AUTO", "normal": "NORMAL", "single": "SINGLE", "stop": "STOP"},
        map_values=True,
    )

    trigger_select = Instrument.control(
        "TRIG_SELECT?",
        "TRIG_SELECT EDGE, SR, %s",
        """ A string parameter that selects the trigger source and type.
        <trig_select>:= #! TODO: sort out edge.
        """,
        validator=strict_discrete_set,
        values={"c1": "C1", "c2": "C2", "c3": "C3", "c4": "C4"},
        map_values=True,
    )

    ##################
    #    Waveform    #
    ##################

    waveform_points = Instrument.control(
        "WFSU?",
        "WFSU NP,%d",
        """ An integer parameter that sets the number of waveform points to be transferred with
        the digitize method. NP = 0 sends all data points.

        Note that the oscilloscope may provide less than the specified nb of points. """,
        validator=strict_range,
        get_process=lambda vals: vals[vals.index("NP") + 1],
        values=[0, sys.maxsize],
    )

    waveform_sparsing = Instrument.control(
        "WFSU?",
        "WFSU SP,%d",
        """ An integer parameter that defines the interval between data points. For example:
            SP = 0 sends all data points.
            SP = 4 sends 1 point every 4 data points.""",
        validator=strict_range,
        get_process=lambda vals: vals[vals.index("SP") + 1],
        values=[0, sys.maxsize],
    )

    waveform_first_point = Instrument.control(
        "WFSU?",
        "WFSU FP,%d",
        """ An integer parameter that specifies the address of the first data point to be sent.
        For waveforms acquired in sequence mode, this refers to the relative address in the
        given segment. The first data point starts at zero and is strictly positive.""",
        validator=strict_range,
        get_process=lambda vals: vals[vals.index("FP") + 1],
        values=[0, sys.maxsize],
    )

    memory_size = Instrument.control(
        "MSIZ?",
        "MSIZ %s",
        """ A float parameter that selects the maximum depth of memory.
        <size>:={7K,70K,700K,7M} for non-interleaved mode. Non-interleaved means a single channel is
        active per A/D converter. Most oscilloscopes feature two channels per A/D converter.
        <size>:={14K,140K,1.4M,14M} for interleave mode. Interleave mode means multiple active
        channels per A/D converter. """,
        validator=strict_discrete_set,
        values={
            7e3: "7K",
            7e4: "70K",
            7e5: "700K",
            7e6: "7M",
            14e3: "14K",
            14e4: "140K",
            14e5: "1.4M",
            14e6: "14M",
        },
        map_values=True,
    )

    @property
    def waveform_preamble(self):
        """Get preamble information for the selected waveform source as a dict with the
        following keys:
        - "type": normal, peak detect, average, high resolution (str)
        - "requested_points": number of data points requested by the user (int)
        - "sampled_points": number of data points sampled by the oscilloscope (int)
        - "transmitted_points": number of data points actually transmitted (optional) (int)
        - "memory_size": size of the oscilloscope internal memory in bytes (int)
        - "sparsing": sparse point. It defines the interval between data points. (int)
        - "first_point": address of the first data point to be sent (int)
        - "source": source of the data : "C1", "C2", "C3", "C4", "MATH".
        - "unit": Physical units of the Y-axis
        - "type":  type of data acquisition. Can be "normal", "peak", "average", "highres"
        - "average": average times of average acquisition
        - "sampling_rate": sampling rate (it is a read-only property)
        - "grid_number": number of horizontal grids (it is a read-only property)
        - "status": acquisition status of the scope. Can be "stopped", "triggered", "ready",
        "auto", "armed"
        - "xdiv": horizontal scale (units per division) in seconds
        - "xoffset": time interval in seconds between the trigger event and the reference position
        - "ydiv": vertical scale (units per division) in Volts
        - "yoffset": value that is represented at center of screen in Volts
        """
        vals = self.values("WFSU?")
        preamble = {
            "sparsing": vals[vals.index("SP") + 1],
            "requested_points": vals[vals.index("NP") + 1],
            "first_point": vals[vals.index("FP") + 1],
            "transmitted_points": None,
            "source": self.waveform_source,
            "type": self.acquisition_type,
            "sampling_rate": self.acquisition_sampling_rate,
            "grid_number": self._grid_number,
            "status": self.acquisition_status,
            "memory_size": self.memory_size,
            "xdiv": self.timebase_scale,
            "xoffset": self.timebase_offset,
        }
        preamble["average"] = self.acquisition_average if preamble["type"][0] == "average" else None
        strict_discrete_set(self.waveform_source, ["C1", "C2", "C3", "C4", "MATH"])
        preamble["sampled_points"] = self.acquisition_sample_size(self.waveform_source)
        return self._fill_yaxis_preamble(preamble)

    def download_waveform(self, source, requested_points=None):
        """Get data points from the specified source of the oscilloscope. The returned objects are two np.ndarray of data and time points and a dict with the waveform preamble, that contains metadata about the waveform.
        Note.
        :param source: measurement source. It can be "C1", "C2", "C3", "C4", "MATH".
        :param requested_points: number of points to acquire. If None the number of points
        requested in the previous call will be assumed, i.e. the value of the number of points stored in the oscilloscope memory. If 0 the maximum number of points will be returned.
        :return: data_ndarray, time_ndarray, waveform_preamble_dict: see waveform_preamble
        property for dict format."""
        # Sanitize the input arguments

        if requested_points is None:
            requested_points = self.memory_size
        self.waveform_source = sanitize_source(source)
        # Acquire the Y data and the preable
        ydata, preamble = self._acquire_data(requested_points)
        # Update the preamble with info about actually acquired data
        preamble["transmitted_points"] = len(ydata)
        preamble["requested_points"] = requested_points
        preamble["first_point"] = 0
        # Scale the Y-data and create the X-data
        return self._process_data(ydata, preamble)

    def _acquire_data(self, requested_points=0):
        """Acquire raw data points from the scope. The header, footer and number of points are sanity-checked, but they are not processed otherwise. For a description of the input arguments refer to the download_waveform method.
        If the number of expected points is big enough, the transmission is split in smaller chunks of 20k points and read one chunk at a time. I do not know the reason why, but if the chunk size is big enough the transmission does not complete successfully.
        :return: raw data points as numpy array and waveform preamble
        """
        # Setup waveform acquisition parameters
        self.waveform_points = requested_points
        self.waveform_first_point = 0

        # Calculate how many points are to be expected
        sample_points = self.acquisition_sample_size(self.waveform_source)
        if requested_points > 0:
            expected_points = min(requested_points, sample_points)
        else:
            expected_points = int(sample_points)

        # If the number of points is big enough, split the data in small chunks and read it one
        # chunk at a time. For less than a certain amount of points we do not bother splitting them.
        chunk_bytes = 20000
        chunk_points = chunk_bytes - self._header_size - self._footer_size
        iterations = -(expected_points // -chunk_points)
        i = 0
        data = []
        while i < iterations:
            # number of points already read
            read_points = i * chunk_points
            # number of points still to read
            remaining_points = expected_points - read_points
            # number of points requested in a single chunk
            requested_points = chunk_points if remaining_points > chunk_points else remaining_points
            self.waveform_points = requested_points
            # number of bytes requested in a single chunk
            requested_bytes = requested_points + self._header_size + self._footer_size
            # read the next chunk starting from this points
            first_point = read_points
            self.waveform_first_point = first_point
            # read chunk of points
            values = self._digitize(src=self.waveform_source, num_bytes=requested_bytes)
            # perform many sanity checks on the received data
            self._header_footer_sanity_checks(values)
            self._npoints_sanity_checks(values)
            # append the points without the header and footer
            data.append(values[self._header_size : -self._footer_size])
            i += 1
        data = np.concatenate(data)
        preamble = self.waveform_preamble
        return data, preamble

    ###############
    #    Math     #
    ###############

    math_define = Instrument.control(
        "DEF?",
        "DEF EQN,'%s%s%s'",
        """ A string parameter that sets the desired waveform math operation between two channels.
        Three parameters must be passed as a tuple:
        1. source1 : source channel on the left
        2. operation : operator must be "*", "/", "+", "-"
        3. source2 : source channel on the right """,
        validator=_math_define_validator,
        values=[["C1", "C2", "C3", "C4"], ["*", "/", "+", "-"], ["C1", "C2", "C3", "C4"]],
    )
