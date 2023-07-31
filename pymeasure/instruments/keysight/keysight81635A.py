class Agilent_PowerMeter(object):
    def __init__(self, fullname):
        """
        Work with Agilent power meters
        """
        self.inst = rm.open_resource(fullname)
        self.name = fullname
        return

    def idn(self):
        """
        return IDN
        """
        return self.inst.query("*IDN?")

    def PowerMeter(self, ch=1):
        """
        get power meter measured value
        """
        p = self.inst.query("fetc1:chan{}:pow?".format(ch))
        return float(p.rstrip().split("<")[0])

    def read_wavelength(self, ch=1):
        """
        get power meter wavelength measured value in nm
        """
        p = self.inst.query(":SENS1:CHAN{}:POW:WAV?".format(ch))
        return 1e9 * float(p.rstrip().split("<")[0])

    def set_wavelength(self, ch, wav):
        """
        set wavelength (nm). wave is in nm.
        """
        self.inst.write(":SENS1:CHAN{}:POW:WAV {}".format(ch, wav * 1e-9))
        return

    def set_cal_offset(self, ch, dB):
        """
        set wavelength (nm). wave is in nm.
        """
        self.inst.write(":SENSE1:CHAN{}:CORR {}".format(ch, dB))
        return

    def read_cal_offset(self, ch):
        """
        set wavelength (nm). wave is in nm.
        """
        dB = self.inst.query(":SENSE1:CHAN{}:CORR?".format(ch))
        return float(dB.rstrip().split("<")[0])

    def set_averaging_time(self, atime):
        """
        set averaging time in seconds
        """
        self.inst.write(":SENSE1:CHAN1:POW:ATIM {}".format(atime))
        return

    def read_averaging_time(self):
        """
        read averaging time in seconds
        """
        atime = self.inst.query(":SENSE1:CHAN1:POW:ATIM?")
        return float(atime.rstrip().split("<")[0])

    def set_power_unit(self, ch, unit=0):
        """
        set power meter unit, unit=0 for dBm, unit=1 for W
        """
        self.inst.write(":SENSE1:CHAN{}:POW:UNIT {}".format(ch, unit))
        return

    def set_autorange(self, ch, auto=1):
        """
        set auto range, 1=ON, 0=OFF
        """
        self.inst.write(":SENSE1:CHAN{}:POW:RANGE:AUTO {}".format(ch, auto))
        return

    def start_minmax_mode(self):
        self.inst.write(":SENSE1:FUNC:STAT MINM,STAR")
        return

    def stop_minmax_mode(self):
        self.inst.write(":SENSE1:FUNC:STAT MINM,STOP")
        return

    def set_minmax_mode(self, mode, nsample=100):
        """
        set minmax mode
        mode = "CONT", "WIND", "REFR"
        nsample = number of samples when mode=window
        """
        self.inst.write(":SENSE1:FUNC:PAR:MINM {},{}".format(mode, nsample))
        return

    def get_minmax_state(self):
        result = self.inst.query("SENSE1:FUNC:STAT?")
        return result.rstrip().split(",")[1]

    def get_minmax_result(self, ch):
        result = self.inst.query("SENSE1:CHAN{}:FUNC:RES?".format(ch))
        minimum = float(result.split(",")[0].split(":")[1])
        maximum = float(result.split(",")[1].split(":")[1])
        return minimum, maximum, maximum - minimum
