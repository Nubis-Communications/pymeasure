class Thorlabs_TEC(object):
    def __init__(self, address="COM5"):
        self.inst = serial.Serial(address, baudrate=115200, timeout=10)
        self.type = self.get_TEC_type()
        return

    def read(self):
        serialString = ""  # Used to hold data coming over UART
        while True:
            # Wait until there is data waiting in the serial buffer
            if self.inst.in_waiting > 0:
                # Read data out of the buffer until a carraige return / new line is found
                serialString = serialString + self.inst.read().decode("utf-8")
            else:
                break
        return serialString.rstrip()

    def query(self, command):
        for i in range(10):
            self.inst.write(command.encode())
            time.sleep(1)
            nbytes = self.inst.in_waiting
            if nbytes > 0:
                response = self.read()
                return response
        print("failed query")
        response = ""
        return response

    def get_TEC_type(self):
        TEC_type = self.query("m?/n")
        return TEC_type

    def get_set_temperature(self):
        mC = self.query("T?/n")
        degreesC = float(mC) / 1000
        return degreesC

    def get_actual_temperature(self):
        mC = self.query("Te?/n")
        degreesC = float(mC) / 1000
        return degreesC

    def set_temperature(self, degreesC):
        command = "T" + str(int(degreesC * 1000)) + "/n"
        print(command)
        n = self.inst.write(command.encode())
        return n
