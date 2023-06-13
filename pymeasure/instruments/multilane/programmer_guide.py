import sys  # sys.maxsize
import os  # os.path
import ctypes  # DLL types marshalling
import time  # time.sleep
from pymlbertapi import pymlbertmgr

# flake8: noqa
__version__ = "1.4.0"
__author__ = "MultilaneInc <support@multilaneinc.com>"
__date__ = "2021-11-11"

##################################################################################################################################################


# Main Flow: ConnectConfigurationion and  Basics
def main():
    """Main function."""
    # creates Instance
    mlbert = pymlbertmgr.mlbertmgr()
    try:
        NB_CHANNELS = 1
        # Connects to device before initializing the instance
        # Edit IPADDRESS of your Instance
        IPADDRESS = "172.16.110.101"
        SUCCESS = mlbert.mlbertmgr_openConnection(IPADDRESS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to connect to %s!" % IPADDRESS, " : ", SUCCESS)
        print("Connected")

        # Initialises instance
        SAVE_CONFIG = ""
        SAVE_BATHTUB = ""
        SAVE_EYE = ""
        SAVE_BATHTUB_ENABLE = 0
        SAVE_EYE_ENABLE = 0
        T_PARAMS = pymlbertmgr.InstanceParams(SAVE_CONFIG, SAVE_BATHTUB, SAVE_EYE, SAVE_BATHTUB_ENABLE, SAVE_EYE_ENABLE)
        SUCCESS = mlbert.mlbertmgr_initializeInstance(T_PARAMS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to initialize Instance ! : ", SUCCESS)
        print("Instance initialized")

        ##################################################################################################################################################
        # Test Flow 1: Get Board information of any BERT

        # Get Board Info
        INFO = ctypes.pointer(pymlbertmgr.Board_Info())
        SUCCESS = mlbert.mlbertmgr_getInfo(INFO)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to retrieve Board Info! : ", SUCCESS)
        print("Board Info is: ")

        # Print out Board Info.
        for fields in INFO[0]._fields_:
            if (fields[0] == "ipAddress") | (fields[0] == "Mask") | (fields[0] == "Gateway"):
                hexadr = getattr(INFO[0], fields[0])
                stradr = "" + str((hexadr & 0xFF))
                for i in range(3):
                    hexadr = hexadr >> 8
                    stradr = str((hexadr & 0xFF)) + "." + stradr
                print("\t", fields[0], ": ", stradr)

            elif fields[0] == "MAC":
                hexadr = getattr(INFO[0], fields[0])
                stradr = "" + str(hex(hexadr & 0xFF)[2:])
                for i in range(5):
                    hexadr = hexadr >> 8
                    stradr = str(hex(hexadr & 0xFF)[2:] + "-" + stradr)
                print("\t", fields[0], ": ", stradr)

            elif fields[0] == "SN":
                SNSTR = ""
                for i in range(10):
                    SNSTR = SNSTR + " " + str(hex(getattr(INFO[0], fields[0])[i]))
                print("\t", fields[0], ": ", SNSTR)
            elif (fields[0] == "HWRev") | (fields[0] == "FWRev"):
                hexadr = getattr(INFO[0], fields[0])
                print("\t", fields[0], ": ", hexadr >> 8, ".", hexadr & 0xF)
            elif fields[0] == "adapterType":
                if INFO[0].isAdapterMode == True:
                    print("\t", fields[0], ": ", pymlbertmgr.ADAPTER_TYPE(getattr(INFO[0], fields[0])))
            else:
                print("\t", fields[0], ": ", getattr(INFO[0], fields[0]))

        ##################################################################################################################################################
        # Test Flow 2: Configure Clock Settings

        APPLYCONFIG = False  # Configurations are cashed in the instrument's memory. Enable APPLYCONFIG for the last call of the flow to trigger the configuration of the instrument

        # Edit parameters for your instance
        # Clock Source
        CLOCKSOURCE = pymlbertmgr.BERTMGR_CLOCKSOURCE.BERTMGR_INTERNALCLKSRC
        # Output Clock Mode
        CLOCKMODE = pymlbertmgr.BERTMGR_CLOCKMODE.BERTMGR_REFCLK
        # Monitor Divider
        DIVIDER = pymlbertmgr.BERTMGR_MONITORDIVIDER.BERTMGR_MONITOR_DIV4
        # CDR Divider
        CDRDIVIDER = pymlbertmgr.BERTMGR_CDRDIVIDER.BERTMGR_CDR_DIV32

        # Set ClockSource
        SUCCESS = mlbert.mlbertmgr_setClockSource(CLOCKSOURCE, APPLYCONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set ClockSource! : ", SUCCESS)
        print("ClockSource is set !")

        # Set ClockMode
        SUCCESS = mlbert.mlbertmgr_setClockMode(CLOCKMODE, APPLYCONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set ClockMode! : ", SUCCESS)
        print("ClockMode is set !")

        # Clock Divider
        # Set Monitor Divider
        SUCCESS = mlbert.mlbertmgr_setMonitorDivider(DIVIDER, APPLYCONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set Monitor Divider! : ", SUCCESS)
        print("Monitor Divider is set !")

        # Set CDR Divider. Check the table of features for compatibility with the BERT
        # SUCCESS = mlbert.mlbertmgr_setCDRDivider(CDRDIVIDER, APPLYCONFIG)
        # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
        #     raise Exception("Failed to set CDR Divider! : ", SUCCESS)
        # print("CDR Divider is set !")

        ##################################################################################################################################################
        # Test Flow 3: Configure LineRate, Coding and Amplitude Levels

        # Eye Mode
        EYEMODE = pymlbertmgr.BERTMGR_SIGMODULATION.BERTMGR_PAM4
        # Tx Taps Mode
        TAPSMODE = pymlbertmgr.BERTMGR_TAPSMODE.BERTMGR_3TAPS
        # Line Rate (Gbaud)
        LINERATE = 25
        # FEC MODE
        FECMODE = pymlbertmgr.BERTMGR_FECMODE.BERTMGR_FECDISABLED
        # FEC PATTERN
        FECPATTERN = pymlbertmgr.BERTMGR_FECPATTERN.FECPATTERN_DISABLED
        # Creates PatternConfig initial struct
        TXPATTERN = pymlbertmgr.PatternConfig()
        # Tx Pattern
        TXPATTERN.pattern = pymlbertmgr.BERTMGR_PATTERNTYPE.BERTMGR_PRBS7
        # Tx Invertion
        TXPATTERN.invert = False
        # Creates PatternConfig initial struct
        RXPATTERN = pymlbertmgr.PatternConfig()
        # Rx pattern
        RXPATTERN.pattern = pymlbertmgr.BERTMGR_PATTERNTYPE.BERTMGR_PRBS7
        # Rx Inversion
        RXPATTERN.invert = False
        # Amplitude Level mV
        AMPLITUDE = 200

        # user defigned pattern
        # Tx Pattern
        # TXPATTERN.pattern = pymlbertmgr.BERTMGR_PATTERNTYPE.BERTMGR_USERDEFINED
        # USER_DEFIGNED_PATTERN=  pymlbertmgr.UserDefinedPatternDefinition()
        # USER_DEFIGNED_PATTERN.Pattern1.Pattern=0XAAAAFFFF55550000
        # USER_DEFIGNED_PATTERN.Pattern1.Repetition=1
        # USER_DEFIGNED_PATTERN.Pattern2.Pattern=0XFFFF0000FFFF0000
        # USER_DEFIGNED_PATTERN.Pattern2.Repetition=0

        # Set Linerate
        SUCCESS = mlbert.mlbertmgr_setLinerate(LINERATE, APPLYCONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set Linerate! : ", SUCCESS)
        print("Linerate is set !")

        # set EyeMode
        SUCCESS = mlbert.mlbertmgr_setEyeMode(EYEMODE, APPLYCONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set EyeMode! : ", SUCCESS)
        print("EyeMode is set !")

        # Enable Gray Coding. Applied for PAM4 Eye Mode.
        # ENABLE = True
        # SUCCESS =  mlbert.mlbertmgr_setGrayCoding(ENABLE, APPLYCONFIG)
        # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
        #    raise Exception("Failed to set Gray Coding! : ", SUCCESS)
        # print ("Gray Coding is set !")

        # Set Taps Mode
        SUCCESS = mlbert.mlbertmgr_setTapsMode(TAPSMODE, APPLYCONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set Taps Mode! : ", SUCCESS)
        print("Taps Mode is set !")
        APPLYCONFIG = True  # Trigger the configuration of all the applied settings

        # Set FEC Mode. Check The table of features for compatibility
        SUCCESS = mlbert.mlbertmgr_setFECMode(FECMODE, FECPATTERN, APPLYCONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set FEC Mode! : ", SUCCESS)
        print("FEC Mode is set !")

        for channel in range(NB_CHANNELS):
            # Set Tx Pattern
            SUCCESS = mlbert.mlbertmgr_setTxPattern(channel, TXPATTERN, APPLYCONFIG)
            if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to set Tx Pattern! : ", SUCCESS)
            print("Tx Patternset is set !")

            # Set Rx Pattern
            SUCCESS = mlbert.mlbertmgr_setRxPattern(channel, RXPATTERN, APPLYCONFIG)
            if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to set Rx Pattern! : ", SUCCESS)
            print("Rx Pattern is set !")

            # set User Defined Pattern
            # SUCCESS =  mlbert.mlbertmgr_setUserDefinedPattern(channel, USER_DEFIGNED_PATTERN, APPLYCONFIG)
            # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            #     raise Exception("Failed to set User Defined Pattern! : ", SUCCESS)
            # print ("User Defined Pattern is set!")

            # Set Calibrated Amplitude level. This function requires a calibrated Instrument
            # SUCCESS =  mlbert.mlbertmgr_setAmplitude(channel, AMPLITUDE,  APPLYCONFIG )
            # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            #    raise Exception("Failed to set Amplitude Level! : ", SUCCESS)
            # print ("Amplitude Level is set !")

        ##################################################################################################################################################
        # Test Flow 4: Set advanced amplitude and equalization

        # Edit parameters for your instance
        # Advanced Amplitude
        APROXAMPLITUDE = ctypes.pointer(ctypes.c_int(0))
        ADVANCEDAMPLITUDE = pymlbertmgr.AdvancedAmplitude()
        # Main Tap Value (-1000 to +1000)
        ADVANCEDAMPLITUDE.mainTap = ctypes.c_int(1000)
        # Post-emphasis Value (-1000 to +1000)
        ADVANCEDAMPLITUDE.postEmphasis = ctypes.c_int(0)
        # Pre-emphasis Value (-1000 to +1000)
        ADVANCEDAMPLITUDE.preEmphasis = ctypes.c_int(0)
        # Inner Eye level(500 to 1500). Applied for PAM4
        ADVANCEDAMPLITUDE.innerLevel = ctypes.c_int(1000)
        # Outer Eye level (1500 to 2500). Applied to PAM4
        ADVANCEDAMPLITUDE.outerLevel = ctypes.c_int(2000)
        # Scaling Level Percentage (70, 80, 90, 100, 110, 120)
        ADVANCEDAMPLITUDE.scalingLevel = ctypes.c_int(80)
        # 7-Taps Mode
        for i in range(7):
            ADVANCEDAMPLITUDE.advancedTaps[i] = ctypes.c_int(0)

        for channel in range(NB_CHANNELS):  # set advanced Amplitude on CHANNEL
            # Set Rx DSP MODE - optional
            # SUCCESS =  mlbert.mlbertmgr_setDSPMode(CHANNEL, DSPMODE, APPLYCONFIG)
            # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            #    raise Exception("Failed to set DSP MODE! : ", SUCCESS)
            # print ("DSP MODE is set!")

            # Set Advanced Amplitude
            SUCCESS = mlbert.mlbertmgr_setAdvancedAmplitude(channel, ADVANCEDAMPLITUDE, APROXAMPLITUDE, APPLYCONFIG)

            if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to set Advanced Amplitude! : ", SUCCESS)
            print("APROX AMPLITUDE = ", APROXAMPLITUDE[0])

        ##################################################################################################################################################
        # Test Flow 5: Enable – disable Tx, Rx
        for channel in range(NB_CHANNELS):
            # Edit parameters for your instance
            ISENABLED = ctypes.pointer(ctypes.c_bool(False))
            STATUS = True
            # Enable  Tx
            SUCCESS = mlbert.mlbertmgr_TxEnable(channel, STATUS)
            if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to Enable Tx! :", SUCCESS)
            print("Tx Enabled !")

            # Enable  Rx
            SUCCESS = mlbert.mlbertmgr_RxEnable(channel, STATUS)
            if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to Enable Rx! : ", SUCCESS)
            print("Rx Enabled !")

            # Get Tx Status
            SUCCESS = mlbert.mlbertmgr_getTxStatus(channel, ISENABLED)
            if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to  Get Tx Status! : ", SUCCESS)
            print("TX enable status : ", ISENABLED[0])

            # Get Rx Status
            SUCCESS = mlbert.mlbertmgr_getRxStatus(channel, ISENABLED)
            if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to  Get Rx Status! : ", SUCCESS)
            print("RX enable status : ", ISENABLED[0])

        ##################################################################################################################################################
        # Test Flow 6: Get BERT active configuration settings

        CONFIG = ctypes.pointer(pymlbertmgr.ConfigurationSettings())
        SUCCESS = mlbert.mlbertmgr_getActiveConfig(CONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to get configuration", pymlbertmgr.BERTMGR_STATUS(SUCCESS))
        print("Get Active Configuration Done!")

        ##################################################################################################################################################
        # Test Flow 7: Monitor function

        # First method: Single read monitor flags.
        # Reads BERT Temperature flags
        SINGLEMONITORFLAG = pymlbertmgr.BERTMGR_MONITOR_FLAGS.BERTMGR_MONITOR_TEMPERATURE
        # Temperature monitor requires 4 x ushort. Refer to the documentation for the required memory allocation per flag
        SINGLE_MONITOR = (ctypes.c_ushort * 4)()
        # Enable Single Monitor Flag and sleep for 350 ms before starting monitor reading.
        # It is recommended to Enable the Monitor at the beginning of the main flow to avoid any settling time.

        # Enable Single Monitor Flag
        Enabled = True
        SUCCESS = mlbert.mlbertmgr_enableMonitorFlag(SINGLEMONITORFLAG, Enabled)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Enable Single Monitor Flag: ", SUCCESS)
        print("Single Monitor Flag is Enabled !")
        time.sleep(0.35)
        # Single Read Monitor Flag
        SUCCESS = mlbert.mlbertmgr_singleReadMonitor(SINGLEMONITORFLAG, SINGLE_MONITOR)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Read Single Monitor Flag: ", SUCCESS)
        print("single Read Monitor is Done !")
        # Disable Single Monitor Flag
        Enabled = False
        SUCCESS = mlbert.mlbertmgr_enableMonitorFlag(SINGLEMONITORFLAG, Enabled)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Disable Single Monitor Flag: ", SUCCESS)
        print("Single Monitor Flag is Disabled !")

        # Second method: MultiRead monitor flags
        # Refer to MONITOR_FLAGS Enum for bits order. Set to 1023 to enable all monitor flags
        MULTIMONITORFLAGS = 1023
        # Monitor multiple Flags (e.g 200) following the same order of the MONITOR_FLAGS Enum
        MULTI_MONITOR = ctypes.pointer(((ctypes.c_ushort * 2) * 200)())
        # Enable Multi Monitor Flags
        SUCCESS = mlbert.mlbertmgr_enableMonitor(MULTIMONITORFLAGS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Enable Multi Monitor Flags ! : ", SUCCESS)
        print("Multi Monitor Flags are Enabled !")
        # Wait for Monitor Accumulation.
        time.sleep(0.35)

        # Multi-Read Monitor
        SUCCESS = mlbert.mlbertmgr_multiReadMonitor(MULTIMONITORFLAGS, MULTI_MONITOR)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Read Multi Monitor! : ", SUCCESS)
        print("Multi Read Monitor is done!")

        # Disable Monitor Flags
        MULTIMONITORFLAGS = 0
        SUCCESS = mlbert.mlbertmgr_enableMonitor(MULTIMONITORFLAGS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to  Disable Monitor! : ", SUCCESS)
        print("Monitor Flags are Disabled!")

        ##################################################################################################################################################
        # Test Flow 8: Read Histogram Data

        # Edit parameters for your instance
        # Enabled channel flags (1 bit/channel)
        HISTENABLEDCHANNEL = 0b00000001
        CHANNEL = 0
        HIST = ctypes.pointer(pymlbertmgr.HistogramData())
        # Get Enabled Channels
        ACTUAL_ENABLED = ctypes.pointer(ctypes.c_ushort())

        # Non blocking API call
        SUCCESS = mlbert.mlbertmgr_captureHistogramData(HISTENABLEDCHANNEL, ACTUAL_ENABLED)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Capture Histogram Data! :", SUCCESS)
        print("Histogram Data is Captured!")
        print("Actual Enabled Channels: ", bin(ACTUAL_ENABLED[0]))

        # Read back the captured histogram data from the BERT
        SUCCESS = mlbert.mlbertmgr_readHistogramData(CHANNEL, HIST)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Read Histogram Data! :", SUCCESS)
        print("Histogram Data Read is done!")

        ##################################################################################################################################################
        # Test Flow 9: Execute fundamental BER Test

        # Pre-allocate MEASBERDATA Struct
        MEASBERDATA = (pymlbertmgr.MeasurementsData * 1024)()
        DATACOUNT = ctypes.pointer(ctypes.c_int(0))
        NB_BER_CHANNELS = 4
        # Enable BER Data Accumulation. Otherwise, the latest Data is captured
        ACCUMULATE = False
        # BER Enbaled CHANNELS. First Channel is Enabled
        # If the test is under the fec feachure please check the  mlbertmgr_configureFECLinks for enabling link.
        BERENABLEDCH = 0b00001111
        VALUE = (ctypes.c_ushort * NB_BER_CHANNELS)(0)
        # Before starting the BER accumulation, it is recommended to add a settling time of 2 seconds
        # ML4054B requires 5 seconds after the configuration
        # "pymlbertmgr.getConfigStatus()" will be implemented in a future library release to check the instrument configuration status and avoid adding a sleep time in the application script
        time.sleep(5)  ## Ensure stabilization time after the BERT configuration

        # Initialize Rx Lock Status and Monitor Rx Lock Status
        SUCCESS = pymlbertmgr.BERTMGR_STATUS.BERTMGR_FAILED
        # Call Rx lock Status in a while loop
        RETRY = 20
        # initialize Rx Lock Monitor Flag
        SINGLEMONITORFLAG = pymlbertmgr.BERTMGR_MONITOR_FLAGS.BERTMGR_MONITOR_RXLOCK

        SUCCESS = mlbert.mlbertmgr_enableMonitor(SINGLEMONITORFLAG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to  Enable Monitor! : ", SUCCESS)
        print("Monitor Flags are Enabled!")
        # Wait for Monitor Data accumulation
        time.sleep(0.35)
        for channel in range(NB_BER_CHANNELS):
            while VALUE[channel] == 0 and RETRY > 0:
                time.sleep(0.1)  # Sleep for 100 ms
                # Single Read Monitor of Rx Lock Status
                SUCCESS = mlbert.mlbertmgr_singleReadMonitor(SINGLEMONITORFLAG, VALUE)
                if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
                    raise Exception("Failed to Read single Monitor! : ", SUCCESS)
                RETRY -= 1
            if VALUE[channel] == 1:
                print("Rx ", channel, " is  locked!")
            else:
                print("Rx ", channel, " is not locked!")

        # Disable Monitor Flags
        MONITORFLAGS = 0
        SUCCESS = mlbert.mlbertmgr_enableMonitor(MONITORFLAGS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to  Disable Monitor! : ", SUCCESS)
        print("Monitor Flags are Disabled!")
        # Start BER. This function requires Rx Lock.
        mlbert.mlbertmgr_startBER(BERENABLEDCH, ACCUMULATE)
        # BER Counting Time
        # ML4054 BER Accumulation starts 4 seconds after enabling the BER process.
        time.sleep(4)

        # Get Available Data
        SUCCESS = mlbert.mlbertmgr_getAvailableBERData(MEASBERDATA, DATACOUNT)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Get Available Data!", SUCCESS)

        # print Out BER Data. Check MeasurementsData struct for more details
        print("Datacount: ", DATACOUNT[0])
        print("Measured BER Data : \r")
        for channel in range(NB_CHANNELS):
            # for ber if the fec is disabled
            print("\nchannel ", channel)
            print("\tEnabled Channels : ", MEASBERDATA[DATACOUNT[0] - 1].berData.enabledChannels[channel])
            print("\tLocked Channels : ", MEASBERDATA[DATACOUNT[0] - 1].berData.lockedChannels[channel])
            print("\tBER Capture Time : ", MEASBERDATA[DATACOUNT[0] - 1].berData.Time[channel])
            print("\tBit Count : ", MEASBERDATA[DATACOUNT[0] - 1].berData.BitCount[channel])
            print("\tErrorCount_MSB: ", MEASBERDATA[DATACOUNT[0] - 1].berData.ErrorCount_MSB[channel])
            print("\tErrorCount_LSB: ", MEASBERDATA[DATACOUNT[0] - 1].berData.ErrorCount_LSB[channel])
            print("\tErrorCount : ", MEASBERDATA[DATACOUNT[0] - 1].berData.ErrorCount[channel])
            print("\tAccumulatedErrorCount_MSB: ", MEASBERDATA[DATACOUNT[0] - 1].berData.AccumulatedErrorCount_MSB[channel])
            print("\tBER_MSB_Interval: ", MEASBERDATA[DATACOUNT[0] - 1].berData.BER_MSB_Interval[channel])
            print("\tBER_MSB_Realtime: ", MEASBERDATA[DATACOUNT[0] - 1].berData.BER_MSB_Realtime[channel])
            print("\tAccumulatedErrorCount_LSB: ", MEASBERDATA[DATACOUNT[0] - 1].berData.AccumulatedErrorCount_LSB[channel])
            print("\tBER_LSB_Interval: ", MEASBERDATA[DATACOUNT[0] - 1].berData.BER_LSB_Interval[channel])
            print("\tBER_LSB_Realtime: ", MEASBERDATA[DATACOUNT[0] - 1].berData.AccumulatedErrorCount_LSB[channel])
            print("\tAccumulatedErrorCount  : ", MEASBERDATA[DATACOUNT[0] - 1].berData.AccumulatedErrorCount[channel])
            print("\tBER_Interval: ", MEASBERDATA[DATACOUNT[0] - 1].berData.BER_Interval[channel])
            print("\tBER Realtime : ", MEASBERDATA[DATACOUNT[0] - 1].berData.BER_Realtime[channel])
        # Stop BER
        SUCCESS = mlbert.mlbertmgr_stopBER()
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Stop BER Test!", SUCCESS)
        print("BER Test stopped!")

        ##################################################################################################################################################
        # test flow 10: Fec link test flow
        # FEC mode
        # FECMODE = pymlbertmgr.BERTMGR_FECMODE.BERTMGR_50G_KR4
        # # FEC PATTERN
        # FECPATTERN = pymlbertmgr.BERTMGR_FECPATTERN.FECPATTERN_IDLE
        # # channels fec link
        # CHANNELS = 0b1  # 1111111
        # SKIPRESET = False

        # # Set FEC Mode. Check The table of features for compatibility
        # # SUCCESS = mlbert.mlbertmgr_setFECMode(FECMODE, FECPATTERN, APPLYCONFIG)
        # # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
        # #     raise Exception("Failed to set FEC Mode! : ", SUCCESS)
        # # print("FEC Mode is set !")

        # # Set FEC Links. Check The table of features for compatibility
        # # SUCCESS = mlbert.mlbertmgr_configureFECLinks(CHANNELS, SKIPRESET, APPLYCONFIG)
        # # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
        # #     raise Exception("Failed to set FEC Mode! : ", SUCCESS)
        # # print("FEC Mode is set !")
        # time.sleep(4)
        # # Start BER. This function requires Rx Lock.
        # mlbert.mlbertmgr_startBER(BERENABLEDCH, ACCUMULATE)

        # # BER Counting Time
        # # ML4054 BER Accumulation starts 4 seconds after enabling the BER process.
        # time.sleep(7)

        # # Get Available Data
        # SUCCESS = mlbert.mlbertmgr_getAvailableBERData(MEASBERDATA, DATACOUNT)
        # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
        #     raise Exception("Failed to Get Available Data!", SUCCESS)

        # for channel in range(NB_CHANNELS):
        #     print("channel: ", channel)
        #     print("\tenabled : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.enabled)
        #     print("\tenabledLinks : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.enabledLinks[channel])
        #     print("\tlockedLinks : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.lockedLinks[channel])
        #     print("\tTime: ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.Time[channel])
        #     print("\tBitCount : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.BitCount[channel])
        #     print("\tFEC_CorrectedBitCount_Interval : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.FEC_CorrectedBitCount_Interval[channel])
        #     print("\tFEC_CW_UnCorrectedCount_Interval : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.FEC_CW_UnCorrectedCount_Interval[channel])
        #     print("\tFEC_CW_CorrectedCount_Interval : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.FEC_CW_CorrectedCount_Interval[channel])
        #     print("\tFEC_CW_ProcessedCount_Interval : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.FEC_CW_ProcessedCount_Interval[channel])
        #     print("\tFEC_CW_UncorrectedErrorRate_Interval : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.FEC_CW_UncorrectedErrorRate_Interval[channel])
        #     print("\tAccumulatedFEC_CW_UnCorrectedCount : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.AccumulatedFEC_CW_UnCorrectedCount[channel])
        #     print("\tAccumulatedFEC_CW_CorrectedCount : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.AccumulatedFEC_CW_CorrectedCount[channel])
        #     print("\tAccumulatedFEC_CW_ProcessedCount : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.AccumulatedFEC_CW_ProcessedCount[channel])
        #     print("\tAccumulatedFEC_CW_UncorrectedErrorRate : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.AccumulatedFEC_CW_UncorrectedErrorRate[channel])
        #     print("\tSER nSymbols : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.SER[channel].nSymbols)
        #     print("\tSER InstantSER : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.SER[channel].InstantSER[0])
        #     print("\tSER AccumulatedSER : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.SER[channel].AccumulatedSER[0])
        #     print("\tTotalBitCount : ", MEASBERDATA[DATACOUNT[0] - 1].RealFECData_4044.TotalBitCount[channel], "\n")

        # # Stop BER
        # SUCCESS = mlbert.mlbertmgr_stopBER()
        # if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
        #     raise Exception("Failed to Stop BER Test!", SUCCESS)
        # print("BER Test stopped!")

        ##################################################################################################################################################
        # Test Flow 11: Adapter Control Pins Flow

        # Detect Module Adapter Type
        ADAPTERTYPE = ctypes.pointer(ctypes.c_int())
        SUCCESS = mlbert.mlbertmgr_detectAdapter(ADAPTERTYPE)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Detect Adapter! :", SUCCESS)
        print("ADAPTER TYPE:", pymlbertmgr.ADAPTER_TYPE(ADAPTERTYPE[0]))

        # Set Adapter I2C Control Mode to External
        ISENABLED = False
        SUCCESS = mlbert.mlbertmgr_setExternalAdapterMode(ISENABLED)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Set External Adapter Mode! :", SUCCESS)
        print("Exterunal Adaper Mode is: ", ISENABLED)

        # Control Adapter Pins
        STATUS = False
        AdapterContolePin = pymlbertmgr.ADAPTER_HWSIGNAL_CNTRL.ADAPTER_HWSIGNAL_CNTRL_QDD_MODSEL_L
        SUCCESS = mlbert.mlbertmgr_setControlPin(AdapterContolePin, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Set Control Pin! :", SUCCESS)
        print("ADAPTER_HWSIGNAL_CNTRL_QDD_MODSEL_L is set to ", STATUS)

        ##################################################################################################################################################
        # Test Flow 12: Tranceiver control Flow and Sequential read/write + MSA

        # Transceiver Tx Controls
        CHANNEL = 0
        STATUS = False
        # Transceiver TX Output Disable
        SUCCESS = mlbert.mltxvr_setTxOutputDisable(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Set TX Output Disable! :", SUCCESS)
        print("Set TX Output Disable To: ", STATUS)

        # Transceiver DataPathDeInit Configuration.
        SUCCESS = mlbert.mltxvr_setTxDataPathDeInit(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Set TX Data PathDeInit! :", SUCCESS)
        print("Set TX Data PathDeInit To: ", STATUS)

        # Transceiver TX Squelch Disable Configuration.
        SUCCESS = mlbert.mltxvr_setTxSquelchDisable(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Set TX Squelch Disable :", SUCCESS)
        print("Set TX Squelch Disable To ", STATUS)

        # Transceiver TX Force Squelch Configuration.
        SUCCESS = mlbert.mltxvr_setTxForceSquelch(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Set TX Force Squelch! :", SUCCESS)
        print("Set TX Force Squelch TO ", STATUS)

        # Transceiver TX Polarity Flip Configuration.
        SUCCESS = mlbert.mltxvr_setTxPolarityFlip(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set TX Polarity Flip! :", SUCCESS)
        print("Set TX Polarity Flip to ", STATUS)

        # Transceiver TX input equalization
        # CMIS Range is from 0-12.
        VALUE = 1
        SUCCESS = mlbert.mltxvr_setTxInputEqualization(CHANNEL, VALUE)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set TX Input Equalization! :", SUCCESS)
        print("Set TX Input Equalization To: ", VALUE)

        # Transceiver RX Controls
        STATUS = False
        # Transceiver Rx Polarity Flip
        SUCCESS = mlbert.mltxvr_setRxPolarityFlip(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set RX Polarity Flip! :", SUCCESS)
        print("Set RX Polarity Flip To: ", STATUS)

        # Transceiver RX Squelch Disable Configuration.
        SUCCESS = mlbert.mltxvr_setRxSquelchDisable(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set RX Squelch Disable! :", SUCCESS)
        print("Set RX Squelch Disable To: ", STATUS)

        # Transceiver RX Output Disable Configuration.
        SUCCESS = mlbert.mltxvr_setRxOutputDisable(CHANNEL, STATUS)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set RX Output Disable! :", SUCCESS)
        print("Set RX Output Disable To: ", STATUS)

        # Transceiver RX Output Pre-Cursor.
        # CMIS Range from 0-7
        VALUE = 1
        SUCCESS = mlbert.mltxvr_setRxPreCursor(CHANNEL, VALUE)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set Rx Pre Cursor! :", SUCCESS)
        print("Set Set RX Pre Cursor To: ", VALUE)

        # Transceiver RX Output Post-Cursor.
        # Range from 0-7
        SUCCESS = mlbert.mltxvr_setRxPostCursor(CHANNEL, VALUE)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set Rx post Cursor! :", SUCCESS)
        print("Set Set RX post Cursor To: ", VALUE)

        # Transceiver RX Output Amplitude.
        TRANS_RX_AMPLITUDE = pymlbertmgr.TXVR_RX_AMPLITUDE.TXVR_RX_AMPLITUDE_100_400
        SUCCESS = mlbert.mltxvr_setRxAmplitude(CHANNEL, TRANS_RX_AMPLITUDE)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Set RX Amplitude! :", SUCCESS)
        print("Transceivwe Rx Amplitude is Set")

        # Get Transceiver Active Configuration Settings
        TRANS_ACTIVECONFIG = ctypes.pointer(pymlbertmgr.TXVR_ConfigurationSettings())
        TRANS_NB_CHANNEL = 8
        SUCCESS = mlbert.mltxvr_getActiveConfig(TRANS_ACTIVECONFIG)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Get Transceiver Active Configuration! :", SUCCESS)
        print("Reading of Transceiver Active Configuration is successfull")
        # Printing all value of the ActivConfg struct
        for channel in range(TRANS_NB_CHANNEL):
            print("channel: ", channel)
            for fields in TRANS_ACTIVECONFIG[0]._fields_:
                print(fields[0], " ", getattr(TRANS_ACTIVECONFIG[0], fields[0])[channel])

        # Reads Transceiver MSA values
        NB_PAGES = 7
        MSAPAGES = (ctypes.c_int * NB_PAGES)()
        MSAPAGES[0] = pymlbertmgr.TXVR_MSA_PAGE.TXVR_MSA_PAGE_LOWERMEMORY
        MSAPAGES[1] = pymlbertmgr.TXVR_MSA_PAGE.TXVR_MSA_PAGE_0
        MSAPAGES[2] = pymlbertmgr.TXVR_MSA_PAGE.TXVR_MSA_PAGE_1
        MSAPAGES[3] = pymlbertmgr.TXVR_MSA_PAGE.TXVR_MSA_PAGE_2
        MSAPAGES[4] = pymlbertmgr.TXVR_MSA_PAGE.TXVR_MSA_PAGE_3
        MSAPAGES[5] = pymlbertmgr.TXVR_MSA_PAGE.TXVR_MSA_PAGE_16
        MSAPAGES[6] = pymlbertmgr.TXVR_MSA_PAGE.TXVR_MSA_PAGE_17
        MSAVALUES = (ctypes.c_ushort * (128 * NB_PAGES))()
        SUCCESS = mlbert.mltxvr_getMSAValues(MSAPAGES, MSAVALUES, NB_PAGES)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed To Get MSA Values! :", SUCCESS)
        print("Getting MSA Values is successfull!")

        # Sequential MSA Read
        # Register addresse range is 128->255, Except LOWERMEMORY where the addresse range is 0->127
        # LOWERMEMORY page index is 0
        READING_PAGE_SELECT = 0
        READING_REGISTER_ADDRESS = 128
        READING_DATA_LENGTH = 128
        READING_DATA_BUFFER = (ctypes.c_ushort * READING_DATA_LENGTH)()
        READING_BANK_SELECT = 0
        SUCCESS = mlbert.mltxvr_sequentialRead(READING_PAGE_SELECT, READING_REGISTER_ADDRESS, READING_DATA_LENGTH, READING_DATA_BUFFER, READING_BANK_SELECT)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Sequentially Read Transceiver Data!", SUCCESS)
        print("Sequential Reading is Successfull!")

        # Sequential MSA Write
        WRITING_PAGE_SELECT = 0
        WRITING_REGISTER_ADDRESS = 0
        WRITING_DATA_LENGTH = 128
        WRITING_DATA_BUFFER = (ctypes.c_ulong * WRITING_DATA_LENGTH)()
        WRITING_BANK_SELECT = 0
        SUCCESS = mlbert.mltxvr_sequentialWrite(WRITING_PAGE_SELECT, WRITING_REGISTER_ADDRESS, WRITING_DATA_LENGTH, WRITING_DATA_BUFFER, WRITING_BANK_SELECT)

        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Sequentially WRITE Transceiver Data ", SUCCESS)
        print("Sequential Writing is Successfull!")

        ##########################################################Adapter And Tranciver Monitor########################################################################################
        # Test Flow 13: Adapter And Transceiver Monitor Flow

        # Enable Adapter Monitor Flag
        MONITORFLAG = pymlbertmgr.BERTMGR_MONITOR_FLAGS.BERTMGR_MONITOR_ADAPTER
        # Monitor Adapter requires 26 ushort values
        ADAPTER_MONITOR_VALUES = (ctypes.c_ushort * 26)()
        ENABLED = True
        SUCCESS = mlbert.mlbertmgr_enableMonitorFlag(MONITORFLAG, ENABLED)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Enable Adapter monitor Flag: ", SUCCESS)
        print("Adapter monitor Flag Is Enabled!")
        # Wait for Monitor Accumulation
        time.sleep(0.35)

        # Single-Read Monitor
        SUCCESS = mlbert.mlbertmgr_singleReadMonitor(MONITORFLAG, ADAPTER_MONITOR_VALUES)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Read Monitor! : ", SUCCESS)
        print("Adapter single Read Monitor is done!")
        # Disable Monitor
        ENBALED = False
        SUCCESS = mlbert.mlbertmgr_enableMonitorFlag(MONITORFLAG, ENBALED)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Disable Adapter monitor Flag: ", SUCCESS)
        print("Adapter monitor Flag Is Disabled!")

        # Print Out Adapter Monitor Values. Voltage values must be converted by dividing by 256
        print("VCC =  ", ADAPTER_MONITOR_VALUES[0] / 256, "V")
        print("VCC1 =  ", ADAPTER_MONITOR_VALUES[1] / 256, "V")
        print("VCC-TX =  ", ADAPTER_MONITOR_VALUES[2] / 256, "V")
        print("VCC-RX =  ", ADAPTER_MONITOR_VALUES[3] / 256, "V")
        print("VOLTAGE5 =  ", ADAPTER_MONITOR_VALUES[4], "V")
        print("VOLTAGE6 =  ", ADAPTER_MONITOR_VALUES[5], "V")
        print("VOLTAGE7 =  ", ADAPTER_MONITOR_VALUES[6], "V")
        print("VOLTAGE8 =  ", ADAPTER_MONITOR_VALUES[7], "V")
        print("I-VCC  =  ", ADAPTER_MONITOR_VALUES[8], "mA")
        print("I-VCC1  =  ", ADAPTER_MONITOR_VALUES[9], "mA")
        print("I-VCC-TX  =  ", ADAPTER_MONITOR_VALUES[10], "mA")
        print("I-VCC-RX  =  ", ADAPTER_MONITOR_VALUES[11], "mA")
        print("CURRENT5 =  ", ADAPTER_MONITOR_VALUES[12], "mA")
        print("CURRENT6 =  ", ADAPTER_MONITOR_VALUES[13], "mA")
        print("CURRENT7 =  ", ADAPTER_MONITOR_VALUES[14], "mA")
        print("CURRENT8 =  ", ADAPTER_MONITOR_VALUES[15], "mA")
        print("Temp1 =  ", ADAPTER_MONITOR_VALUES[16])
        print("Temp2 =  ", ADAPTER_MONITOR_VALUES[17])
        print("Temp3 =  ", ADAPTER_MONITOR_VALUES[18])
        print("Temp4 =  ", ADAPTER_MONITOR_VALUES[19])
        print("Temp5 =  ", ADAPTER_MONITOR_VALUES[20])
        print("Temp6 =  ", ADAPTER_MONITOR_VALUES[21])
        print("Temp7 =  ", ADAPTER_MONITOR_VALUES[22])
        print("Temp8 =  ", ADAPTER_MONITOR_VALUES[23])

        print("Control Signals: ")
        # Read back control Pins Status
        if (ADAPTER_MONITOR_VALUES[24] & 1 << 0) == 1 << 0:
            print("\tModeSetL is enabled")
        else:
            print("\tModeSetL is disabled")

        if (ADAPTER_MONITOR_VALUES[24] & (1 << 1)) == 1 << 1:
            print("\tResetL is enabled")
        else:
            print("\tResetL is disabled")

        if (ADAPTER_MONITOR_VALUES[24] & 1 << 2) == 1 << 2:
            print("\tLPMode is enabled")
        else:
            print("\tLPMode is disabled")

        print("RO Signals: ")
        # Active Low
        if (ADAPTER_MONITOR_VALUES[24] & 1 << 3) != 1 << 3:
            print("\tModePrsL is active")
        else:
            print("\tModePrsL is deactive")
        # Active Low
        if (ADAPTER_MONITOR_VALUES[24] & 1 << 4) != 1 << 4:
            print("\tIntL is active")
        else:
            print("\tIntL is deactive")

        print("Adapter IsExternalMode:  ", ADAPTER_MONITOR_VALUES[25])

        # Enable Transceiver Monitor Flag
        MONITORFLAG = pymlbertmgr.BERTMGR_MONITOR_FLAGS.BERTMGR_MONITOR_TRANSCEIVER
        # Monitor Transceiver requires ushort values.
        TRANS_MONITOR_VALUES = (ctypes.c_ushort * 80)()
        ENABLED = True
        SUCCESS = mlbert.mlbertmgr_enableMonitorFlag(MONITORFLAG, ENABLED)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Enable Tranciver monitor Flag: ", SUCCESS)
        print("Tranciver monitor Flag Is Enabled!")
        # Wait for Monitor Accumulation
        time.sleep(0.35)

        # Single-Read Monitor
        SUCCESS = mlbert.mlbertmgr_singleReadMonitor(MONITORFLAG, TRANS_MONITOR_VALUES)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Read Monitor! : ", SUCCESS)
        print("Single Read Monitor is done!")

        # Disable Transceiver Monitor Flag
        ENABLED = False
        SUCCESS = mlbert.mlbertmgr_enableMonitorFlag(MONITORFLAG, ENABLED)
        if SUCCESS != pymlbertmgr.BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to Disable Transceiver monitor Flag: ", SUCCESS)
        print("Transceiver monitor Flag Is Disabled!")

        # Conversion is Performed According to CMIS Standard
        print("tempSupplyFlags:  ", TRANS_MONITOR_VALUES[0])
        print("aux1Aux2Flags:  ", TRANS_MONITOR_VALUES[1])
        print("aux3VendorFlags:  ", TRANS_MONITOR_VALUES[2])
        print("Temp1:  ", TRANS_MONITOR_VALUES[3] / 256)
        print("Temp2:  ", TRANS_MONITOR_VALUES[4] / 256)
        print("Temp3:  ", TRANS_MONITOR_VALUES[5] / 256)
        print("Temp4:  ", TRANS_MONITOR_VALUES[6] / 256)
        print("VCC:  ", TRANS_MONITOR_VALUES[7] / 10000, "V")
        print("VCC2:  ", TRANS_MONITOR_VALUES[8] / 10000, "V")
        print("VCC3:  ", TRANS_MONITOR_VALUES[9] / 10000, "V")
        print("VCC4:  ", TRANS_MONITOR_VALUES[10] / 10000, "V")
        print("aux1:  ", TRANS_MONITOR_VALUES[11])
        print("aux2:  ", TRANS_MONITOR_VALUES[12])
        print("aux3:  ", TRANS_MONITOR_VALUES[13])
        print("STATE_CHANGE:  ", TRANS_MONITOR_VALUES[14])
        print("TX_FAULT:  ", TRANS_MONITOR_VALUES[15])
        print("TX_LOS:  ", TRANS_MONITOR_VALUES[16])
        print("TX_LOL:  ", TRANS_MONITOR_VALUES[17])
        print("TXPOWER_HA:  ", TRANS_MONITOR_VALUES[18])
        print("TXPOWER_LA:  ", TRANS_MONITOR_VALUES[19])
        print("TXPOWER_HW:  ", TRANS_MONITOR_VALUES[20])
        print("TXPOWER_LW:  ", TRANS_MONITOR_VALUES[21])
        print("TXBIAS_HA:  ", TRANS_MONITOR_VALUES[22])
        print("TXBIAS_LA:  ", TRANS_MONITOR_VALUES[23])
        print("TXBIAS_HW:  ", TRANS_MONITOR_VALUES[24])
        print("TXBIAS_LW:  ", TRANS_MONITOR_VALUES[25])
        print("RX_LOS:  ", TRANS_MONITOR_VALUES[26])
        print("RX_LOL:  ", TRANS_MONITOR_VALUES[27])
        print("RXPOWER_HA:  ", TRANS_MONITOR_VALUES[28])
        print("RXPOWER_LA:  ", TRANS_MONITOR_VALUES[29])
        print("RXPOWER_LW:  ", TRANS_MONITOR_VALUES[30])
        print("RXPOWER_LW:  ", TRANS_MONITOR_VALUES[31])
        print("TX0:  ", TRANS_MONITOR_VALUES[32] / 10000, "mW")
        print("TX1:  ", TRANS_MONITOR_VALUES[33] / 10000, "mW")
        print("TX2:  ", TRANS_MONITOR_VALUES[34] / 10000, "mW")
        print("TX3:  ", TRANS_MONITOR_VALUES[35] / 10000, "mW")
        print("TX4:  ", TRANS_MONITOR_VALUES[36] / 10000, "mW")
        print("TX5:  ", TRANS_MONITOR_VALUES[37] / 10000, "mW")
        print("TX6:  ", TRANS_MONITOR_VALUES[38] / 10000, "mW")
        print("TX7:  ", TRANS_MONITOR_VALUES[39] / 10000, "mW")
        print("TX8:  ", TRANS_MONITOR_VALUES[40] / 10000, "mW")
        print("TX9:  ", TRANS_MONITOR_VALUES[41] / 10000, "mW")
        print("TX10:  ", TRANS_MONITOR_VALUES[42] / 10000, "mW")
        print("TX11:  ", TRANS_MONITOR_VALUES[43] / 10000, "mW")
        print("TX12:  ", TRANS_MONITOR_VALUES[44] / 10000, "mW")
        print("TX13:  ", TRANS_MONITOR_VALUES[45] / 10000, "mW")
        print("TX14:  ", TRANS_MONITOR_VALUES[46] / 10000, "mW")
        print("TX15:  ", TRANS_MONITOR_VALUES[47] / 10000, "mW")
        print("TX-Bias0:  ", TRANS_MONITOR_VALUES[48] * 0.002, "mA")
        print("TX-Bias1:  ", TRANS_MONITOR_VALUES[49] * 0.002, "mA")
        print("TX-Bias2:  ", TRANS_MONITOR_VALUES[50] * 0.002, "mA")
        print("TX-Bias3:  ", TRANS_MONITOR_VALUES[51] * 0.002, "mA")
        print("TX-Bias4:  ", TRANS_MONITOR_VALUES[52] * 0.002, "mA")
        print("TX-Bias5:  ", TRANS_MONITOR_VALUES[53] * 0.002, "mA")
        print("TX-Bias6:  ", TRANS_MONITOR_VALUES[54] * 0.002, "mA")
        print("TX-Bias7:  ", TRANS_MONITOR_VALUES[55] * 0.002, "mA")
        print("TX-Bias8:  ", TRANS_MONITOR_VALUES[56] * 0.002, "mA")
        print("TX-Bias9:  ", TRANS_MONITOR_VALUES[57] * 0.002, "mA")
        print("TX-Bias10:  ", TRANS_MONITOR_VALUES[58] * 0.002, "mA")
        print("TX-Bias11:  ", TRANS_MONITOR_VALUES[59] * 0.002, "mA")
        print("TX-Bias12:  ", TRANS_MONITOR_VALUES[60] * 0.002, " mA")
        print("TX-Bias13:  ", TRANS_MONITOR_VALUES[61] * 0.002, " mA")
        print("TX-Bias14:  ", TRANS_MONITOR_VALUES[62] * 0.002, " mA")
        print("TX-Bias15:  ", TRANS_MONITOR_VALUES[63] * 0.002, " mA")
        print("RX0:  ", TRANS_MONITOR_VALUES[64] / 10000, "mW")
        print("RX1:  ", TRANS_MONITOR_VALUES[65] / 10000, "mW")
        print("RX2:  ", TRANS_MONITOR_VALUES[66] / 10000, "mW")
        print("RX3:  ", TRANS_MONITOR_VALUES[67] / 10000, "mW")
        print("RX4:  ", TRANS_MONITOR_VALUES[68] / 10000, "mW")
        print("RX5:  ", TRANS_MONITOR_VALUES[69] / 10000, "mW")
        print("RX6:  ", TRANS_MONITOR_VALUES[70] / 10000, "mW")
        print("RX7:  ", TRANS_MONITOR_VALUES[71] / 10000, "mW")
        print("RX8:  ", TRANS_MONITOR_VALUES[72] / 10000, "mW")
        print("RX9:  ", TRANS_MONITOR_VALUES[73] / 10000, "mW")
        print("RX10:  ", TRANS_MONITOR_VALUES[74] / 10000, "mW")
        print("RX11:  ", TRANS_MONITOR_VALUES[75] / 10000, "mW")
        print("RX12:  ", TRANS_MONITOR_VALUES[76] / 10000, "mW")
        print("RX13:  ", TRANS_MONITOR_VALUES[77] / 10000, "mW")
        print("RX14:  ", TRANS_MONITOR_VALUES[78] / 10000, "mW")
        print("RX15:  ", TRANS_MONITOR_VALUES[79] / 10000, "mW")

    finally:
        # Disconnect
        print("mlbertmgr_closeConnection: ", mlbert.mlbertmgr_closeConnection())
        # Destroy Instance
        mlbert.mlbertmgr_destroyInstance()
        print("mlbertmgr_destroyInstance done.")


if __name__ == "__main__":
    main()
