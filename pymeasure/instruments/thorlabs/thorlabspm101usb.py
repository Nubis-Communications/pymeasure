class Thorlabs_101PM:
    def __init__(self, device_name):
        self.inst = rm.open_resource(device_name)
        return

    def get_ID(self):
        return self.inst.query("*IDN?")

    def set_units(self, unit):
        if unit.upper() != "W" and unit.upper() != "DBM":
            print("wrong units")
            return
        else:
            self.inst.write("SENSE:POW:UNIT " + unit)

    def set_wavelength(self, wavelength):
        if 800 <= wavelength <= 1700:
            self.inst.write("SENSE:CORR:WAV " + str(wavelength))
        else:
            print("wavelength not in the range")
            return

    def get_power(self):
        return self.inst.query("MEAS:POW?")

    def get_wavelength(self):
        return self.inst.query("SENSE:CORR:WAV?")

    def set_averaging(self, count):
        if 0 <= count <= 40:
            self.inst.write("SENSE:AVERage " + str(count))
        else:
            print("averaging value not it range")
            return

    def set_autorange(self):
        self.inst.query("CURRent:RANGe:AUTO 1")

    def close_connection(self):
        self.inst.close()

    def set_upper_range_dBm(self, power):
        power_W = 10 ** (power / 10) * 0.001
        self.inst.write("SENSe:POWer:RANGe " + str(power_W))
