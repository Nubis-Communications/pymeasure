from pymeasure.instruments.multilane.pymlbertapi import pymlbertmgr as pybert
import logging

logging.basicConfig(
    filename="bert.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# from pymeasure.adapters import
import pyvisa

if __name__ == "__main__":

    try:
        bert = pybert.mlbertmgr()
    except:
        logging.info("Could not connect to Multilane BERT")

    channels = 2

    bert.setup_clock()
    modulation = "PAM4"
    baudrate = 56  # in GBd
    prbs = "prbs31"
    amplitude = 200  # Amplitude Level mV
    invert = "off"  # 'off', 'tx', 'rx' or 'txrx'
    ffetaps = 7
    fecmode = "disabled"
    fecpattern = "disabled"
    bert.configure_txrx(modulation, baudrate, prbs, amplitude, invert)
    # bert.configure_txrx(modulation, baudrate, prbs, amplitude, invert, ffetaps, fecmode, fecpattern)

    # APPLYCONFIG = True
    # #     # Eye Mode
    # EYEMODE = pybert.BERTMGR_SIGMODULATION.BERTMGR_PAM4
    # # Tx Taps Mode
    # TAPSMODE = pybert.BERTMGR_TAPSMODE.BERTMGR_3TAPS
    # # Line Rate (Gbaud)
    # LINERATE = 25
    # # FEC MODE
    # FECMODE = pybert.BERTMGR_FECMODE.BERTMGR_FECDISABLED
    # # FEC PATTERN
    # FECPATTERN = pybert.BERTMGR_FECPATTERN.FECPATTERN_DISABLED
    # # Creates PatternConfig initial struct
    # TXPATTERN = pybert.PatternConfig()
    # # Tx Pattern
    # TXPATTERN.pattern = pybert.BERTMGR_PATTERNTYPE.BERTMGR_PRBS7
    # # Tx Invertion
    # TXPATTERN.invert = False
    # # Creates PatternConfig initial struct
    # RXPATTERN = pybert.PatternConfig()
    # # Rx pattern
    # RXPATTERN.pattern = pybert.BERTMGR_PATTERNTYPE.BERTMGR_PRBS7
    # # Rx Inversion
    # RXPATTERN.invert = False
    # # Amplitude Level mV
    # AMPLITUDE = 200

    # # Set Linerate

    # # set EyeMode
    # SUCCESS = bert.mlbertmgr_setEyeMode(EYEMODE, APPLYCONFIG)
    # if SUCCESS != pybert.BERTMGR_STATUS.BERTMGR_SUCCESS:
    #     raise Exception("Failed to set EyeMode! : ", SUCCESS)
    # print("EyeMode is set !")

    # # Enable Gray Coding. Applied for PAM4 Eye Mode.
    # ENABLE = True
    # SUCCESS = bert.mlbertmgr_setGrayCoding(ENABLE, APPLYCONFIG)
    # if SUCCESS != pybert.BERTMGR_STATUS.BERTMGR_SUCCESS:
    #     raise Exception("Failed to set Gray Coding! : ", SUCCESS)
    # print("Gray Coding is set !")

    # # Set Taps Mode
    # SUCCESS = bert.mlbertmgr_setTapsMode(TAPSMODE, APPLYCONFIG)
    # if SUCCESS != pybert.BERTMGR_STATUS.BERTMGR_SUCCESS:
    #     raise Exception("Failed to set Taps Mode! : ", SUCCESS)
    # print("Taps Mode is set !")
    # APPLYCONFIG = True  # Trigger the configuration of all the applied settings

    # # Set FEC Mode. Check The table of features for compatibility
    # SUCCESS = bert.mlbertmgr_setFECMode(FECMODE, FECPATTERN, APPLYCONFIG)
    # if SUCCESS != pybert.BERTMGR_STATUS.BERTMGR_SUCCESS:
    #     raise Exception("Failed to set FEC Mode! : ", SUCCESS)
    # print("FEC Mode is set !")

    # for channel in range(channels):
    #     # Set Tx Pattern
    #     SUCCESS = bert.mlbertmgr_setTxPattern(channel, TXPATTERN, APPLYCONFIG)
    #     if SUCCESS != pybert.BERTMGR_STATUS.BERTMGR_SUCCESS:
    #         raise Exception("Failed to set Tx Pattern! : ", SUCCESS)
    #     print("Tx Patternset is set !")

    #     # Set Rx Pattern
    #     SUCCESS = bert.mlbertmgr_setRxPattern(channel, RXPATTERN, APPLYCONFIG)
    #     if SUCCESS != pybert.BERTMGR_STATUS.BERTMGR_SUCCESS:
    #         raise Exception("Failed to set Rx Pattern! : ", SUCCESS)
    #     print("Rx Pattern is set !")

    # except:
    #     raise Exception("Check connection")
