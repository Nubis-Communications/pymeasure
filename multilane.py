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
    graycoding = True  # true/false
    prbs = "prbs31"
    amplitude = 250  # Amplitude Level mV
    invert = "off"  # 'off', 'tx', 'rx' or 'txrx'
    tapsmode = 3  # 3 or 7
    ffetaps = [-100, 800, -100]  # range -1000 <-> 1000
    innerlevel = 1000  # inner: 500-1500
    outerlevel = 2000  # outer: 1500-2500
    eyelevels = [innerlevel, outerlevel]
    scalinglevel = 80  # 80, 90, 100, 110, 120
    bert.configure_modulation(
        channels=channels,
        modulation=modulation,
        baudrate=baudrate,
        prbs=prbs,
        amplitude=amplitude,
        invert=invert,
        tapsmode=tapsmode,
        ffetaps=ffetaps,
        eyelevels=eyelevels,
        scalinglevel=scalinglevel,
    )
    fecmode = "disabled"
    fecpattern = "disabled"

    bert.configure_fec(
        channels=channels,
        modulation=modulation,
        baudrate=baudrate,
        fecmode=fecmode,
        fecpattern=fecpattern,
    )

    bert.enable_txrx(channels)

    accumulate = False
    bert.basic_ber(channels=channels, accumulate=accumulate)
    # bert.measure_ber()
