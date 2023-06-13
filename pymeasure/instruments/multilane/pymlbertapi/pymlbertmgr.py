"""MLBERTMGR API Python wrapper."""

import sys  # sys.maxsize
import os  # os.path
import ctypes  # DLL types marshalling
from enum import IntEnum
import logging

# flake8: noqa

__all__ = ("mlbertmgr",)
__version__ = "1.4.0"
__author__ = "MultilaneInc <support@multilaneinc.com>"
__date__ = "2021-11-11"


MAXCHANNELS = 8
MAX_ADDR_LEN = 256
BERMAXITEMSPOP = 1024
SERMAXNUMSYMBOLS = 31
FECMAXNUMLINKS = 8


class BERTMGR_AFETRIM_OPT(IntEnum):
    BERTMGR_AFETRIM_NEG4DB = (0,)
    BERTMGR_AFETRIM_NEG10DB = 1


class BERTMGR_CALIBRATIONMODE(IntEnum):
    BERTMGR_CALMODE_ADV = (-1,)  # Advanced mode
    BERTMGR_CALMODE_LRLV = (0,)  # Low-rate/low-voltage
    BERTMGR_CALMODE_LRHV = (1,)  # Low-rate/high-voltage
    BERTMGR_CALMODE_HRLV = (2,)  # High-rate/low-voltage
    BERTMGR_CALMODE_HRHV = (3,)  # High-rate/high-voltage


class BERTMGR_CDRDIVIDER(IntEnum):
    BERTMGR_CDR_DIV32 = (1 << 5,)
    BERTMGR_CDR_DIV64 = (1 << 6,)
    BERTMGR_CDR_DIV128 = (1 << 7,)
    BERTMGR_CDR_DIV256 = (1 << 8,)
    BERTMGR_CDR_DIV512 = (1 << 9,)
    BERTMGR_CDR_DIV1024 = (1 << 10,)
    BERTMGR_CDR_DIV2048 = (1 << 11,)
    BERTMGR_CDR_DIV4096 = 1 << 12


class BERTMGR_CLOCKMODE(IntEnum):
    BERTMGR_MONITORCLOCK_CH0toCH3 = (0,)
    BERTMGR_EXTERNAL = (1,)
    BERTMGR_REFCLK = (2,)
    BERTMGR_MONITORCLOCK_CH4toCH7 = (3,)
    BERTMGR_CDR_CH0toCH3 = (4,)
    BERTMGR_CDR_CH4toCH7 = (5,)
    BERTMGR_REFCLK2 = 6


class BERTMGR_CLOCKSOURCE(IntEnum):
    BERTMGR_EXTERNALCLKSRC = (0,)
    BERTMGR_INTERNALCLKSRC = 1


class BERTMGR_DSPMODE(IntEnum):
    BERTMGR_DSP_MODE_SLC1 = (0,)  # PAM4 Slicer
    BERTMGR_DSP_MODE_SLC1_LDEQ = (1,)  # PAM4 Slicer + Level-dependent equalizer (LDEQ)
    BERTMGR_DSP_MODE_SLC1_RC_SLC2 = (2,)  # PAM4 Slicer + Reflection canceller (RC)
    BERTMGR_DSP_MODE_SLC1_RC_LDEQ = (3,)  # PAM4 Slicer + LDEQ + RC
    BERTMGR_DSP_MODE_DFE1 = (4,)  # Decision Feedback Equalizer (DFE)
    BERTMGR_DSP_MODE_DFE1_RC_DFE2 = (7,)  # DFE + RC
    BERTMGR_DSP_MODE_SLC1_MPICAN_SLC2 = (8,)  # PAM4 Slicer + Multipath interference canceller (MPICAN)
    BERTMGR_DSP_MODE_SLC1_MPICAN_LDEQ = (9,)  # PAM4 Slicer + LDEQ + MPICAN
    BERTMGR_DSP_MODE_SLC1_RC_MPICAN_SLC2 = (10,)  # PAM4 Slicer + RC + MPICAN
    BERTMGR_DSP_MODE_SLC1_RC_MPICAN_LDEQ = (11,)  # PAM4 Slicer + LDEQ + RC + MPICAN
    BERTMGR_DSP_MODE_DFE1_MPICAN_DFE2 = (13,)  # DFE + MPICAN
    BERTMGR_DSP_MODE_DFE1_RC_MPICAN_DFE2 = 15  # DFE + RC + MPICAN


class BERTMGR_ERRORINSERTIONMODES(IntEnum):
    BERTMGR_ERRINJ_PAT_BIT0 = (0,)  # bit 0 one MSB
    BERTMGR_ERRINJ_PAT_BIT1 = (1,)  # bit 1 one LSB
    BERTMGR_ERRINJ_PAT_BIT01 = (2,)  # bit 0 and 1 one PAM4 (MSB and LSB)
    BERTMGR_ERRINJ_PAT_MSBS = (3,)  # all MSBs
    BERTMGR_ERRINJ_PAT_LSBS = (4,)  # all LSBs
    BERTMGR_ERRINJ_PAT_ALL = 5  # all bits


class BERTMGR_FECMODE(IntEnum):
    BERTMGR_FECDISABLED = (-1,)
    BERTMGR_400G_KP8_TO_KP4 = (0,)
    BERTMGR_200G_KP4_TO_KP2 = (1,)
    BERTMGR_200G_KP4_TO_KP4 = (2,)
    BERTMGR_100G_KP2_TO_KP1 = (3,)
    BERTMGR_100G_KP4_TO_KP4 = (4,)
    BERTMGR_100G_KP4_TO_KP2 = (5,)
    BERTMGR_100G_PCS4_TO_KR1 = (6,)
    BERTMGR_50G_KP1_TO_KP1 = (7,)
    BERTMGR_50G_KP2_TO_KP2 = (8,)
    BERTMGR_50G_KR2_TO_KR1 = (9,)
    BERTMGR_25G_KR1_TO_KR1 = (10,)
    BERTMGR_25G_KP1_TO_KP1 = (11,)
    BERTMGR_50G_KS = (20,)
    BERTMGR_50G_KR = (21,)
    BERTMGR_50G_KP = (22,)
    BERTMGR_100G_KR = (23,)
    BERTMGR_100G_KP = (24,)
    BERTMGR_200G_KP = (25,)
    BERTMGR_400G_KP = 26
    # 4054 fec mode
    BERTMGR_25G_FC = (40,)
    BERTMGR_25G_KR4 = (41,)
    BERTMGR_25G_KP4 = (42,)
    BERTMGR_50G_FC = (43,)
    BERTMGR_50G_KR4 = (44,)
    BERTMGR_50G_KP4 = (45,)
    BERTMGR_100G_FC = (46,)
    BERTMGR_100G_KR4 = (47,)
    BERTMGR_100G_KP4 = (48,)
    BERTMGR_200G_FC = (49,)
    BERTMGR_200G_KR4 = (50,)
    BERTMGR_200G_KP4 = 51


class BERTMGR_FECPATTERN(IntEnum):
    FECPATTERN_DISABLED = (-1,)
    FECPATTERN_IDLE = (0,)
    FECPATTERN_LOCALFAULT = (1,)
    FECPATTERN_REMOTEFAULT = 2


class BERTMGR_MONITOR_FLAGS(IntEnum):
    BERTMGR_MONITOR_LOS = (0x1 << 0,)  # LOS Enable Flag
    BERTMGR_MONITOR_DSP = (0x1 << 1,)  # DSP Monitor Enable Flag
    BERTMGR_MONITOR_SIGNALDETECT = (0x1 << 2,)  # Signal Detect Monitor Flag
    BERTMGR_MONITOR_TXLOCK = (0x1 << 3,)  # Tx Lock Monitor Flag (bit 3)
    BERTMGR_MONITOR_RXLOCK = (0x1 << 4,)  # RX Lock Monitor Flag (bit 4)
    BERTMGR_MONITOR_TEMPERATURE = (0x1 << 5,)  # Temperature Monitor Flag (bit 5)
    BERTMGR_MONITOR_SNR = (0x1 << 6,)  # SNR Monitor Flag
    BERTMGR_MONITOR_VOLTAGE = (0x1 << 7,)  # Voltage Monitor Flag
    BERTMGR_MONITOR_CURRENT = (0x1 << 8,)  # Current Monitor Flag
    BERTMGR_MONITOR_FFETAPS = 0x1 << 9  # FFE Taps Monitor Flag
    BERTMGR_MONITOR_XT_TXLOCK = (0x1 << 10,)  # XT Flag
    BERTMGR_MONITOR_ADAPTER = (0x1 << 11,)  # Adapter Monitor Flag
    BERTMGR_MONITOR_TRANSCEIVER = 0x1 << 12  # Tranceiver Monitor Flag


class BERTMGR_MONITORDIVIDER(IntEnum):
    BERTMGR_MONITOR_DIV1 = (1 << 0,)
    BERTMGR_MONITOR_DIV4 = (1 << 2,)
    BERTMGR_MONITOR_DIV8 = (1 << 3,)
    BERTMGR_MONITOR_DIV16 = (1 << 4,)
    BERTMGR_MONITOR_DIV32 = (1 << 5,)
    BERTMGR_MONITOR_DIV64 = (1 << 6,)
    BERTMGR_MONITOR_DIV128 = 1 << 7


class BERTMGR_PATTERNTYPE(IntEnum):
    BERTMGR_PRBS7 = (0,)
    BERTMGR_PRBS9_4 = (1,)
    BERTMGR_PRBS9_5 = (2,)
    BERTMGR_PRBS11 = (3,)
    BERTMGR_PRBS13 = (4,)
    BERTMGR_PRBS15 = (5,)
    BERTMGR_PRBS16 = (6,)
    BERTMGR_PRBS23 = (7,)
    BERTMGR_PRBS31 = (8,)
    BERTMGR_PRBS58 = (9,)
    BERTMGR_USERDEFINED = (10,)
    BERTMGR_JP03B = (11,)
    BERTMGR_LIN = (12,)
    BERTMGR_CJT = (13,)
    BERTMGR_SSPRQ = (14,)
    BERTMGR_SQ16 = (15,)
    BERTMGR_SQ32 = (16,)
    BERTMGR_IEEE8023BS_2 = (17,)
    BERTMGR_IEEE8023BS_4 = (18,)
    BERTMGR_OIFCEI311 = 19


class BERTMGR_SIGMODULATION(IntEnum):
    BERTMGR_PAM4 = (0,)
    BERTMGR_NRZ = 1


class BERTMGR_STATUS(IntEnum):
    BERTMGR_SUCCESS = (0,)
    BERTMGR_FAILED = (1,)
    BERTMGR_TIMEOUT = (2,)
    BERTMGR_UNEXPECTED_ERROR = (3,)
    BERTMGR_UNSUPPORTED_OPTION = (4,)
    BERTMGR_BER_DISABLED = 5


class BERTMGR_TAPSMODE(IntEnum):
    BERTMGR_3TAPS = (0,)
    BERTMGR_7TAPS = 1


class AdvancedAmplitude(ctypes.Structure):
    _fields_ = [
        ("mainTap", ctypes.c_int),
        ("postEmphasis", ctypes.c_int),
        ("preEmphasis", ctypes.c_int),
        ("innerLevel", ctypes.c_int),
        ("outerLevel", ctypes.c_int),
        ("scalingLevel", ctypes.c_int),
        ("advancedTaps", ctypes.c_int * 7),
    ]


class AmpRange(ctypes.Structure):
    _fields_ = [("min", ctypes.c_int), ("max", ctypes.c_int), ("calMode", ctypes.c_int)]


class BERData(ctypes.Structure):
    _fields_ = [
        ("enabled", ctypes.c_bool),
        ("enabledChannels", ctypes.c_bool * MAXCHANNELS),
        ("lockedChannels", ctypes.c_bool * MAXCHANNELS),
        ("Time", ctypes.c_double * MAXCHANNELS),
        ("BitCount", ctypes.c_ulonglong * MAXCHANNELS),
        ("ErrorCount_MSB", ctypes.c_ulong * MAXCHANNELS),
        ("ErrorCount_LSB", ctypes.c_ulong * MAXCHANNELS),
        ("ErrorCount", ctypes.c_ulonglong * MAXCHANNELS),
        ("AccumulatedErrorCount_MSB", ctypes.c_ulonglong * MAXCHANNELS),
        ("BER_MSB_Interval", ctypes.c_double * MAXCHANNELS),
        ("BER_MSB_Realtime", ctypes.c_double * MAXCHANNELS),
        ("AccumulatedErrorCount_LSB", ctypes.c_ulonglong * MAXCHANNELS),
        ("BER_LSB_Interval", ctypes.c_double * MAXCHANNELS),
        ("BER_LSB_Realtime", ctypes.c_double * MAXCHANNELS),
        ("AccumulatedErrorCount", ctypes.c_ulonglong * MAXCHANNELS),
        ("BER_Interval", ctypes.c_double * MAXCHANNELS),
        ("BER_Realtime", ctypes.c_double * MAXCHANNELS),
        ("TotalBitCount", ctypes.c_ulonglong * MAXCHANNELS),
    ]


class Board_Info(ctypes.Structure):
    _fields_ = [
        ("boardID", ctypes.c_ushort),
        ("HWRev", ctypes.c_ushort),
        ("FWRev", ctypes.c_ushort),
        ("SilabRev", ctypes.c_ushort),
        ("ipAddress", ctypes.c_long),
        ("Mask", ctypes.c_ulong),
        ("Gateway", ctypes.c_ulong),
        ("MAC", ctypes.c_ulonglong),
        ("SN", ctypes.c_ubyte * 10),
        ("Bootloader_Flag", ctypes.c_bool),
        ("isAdapterMode", ctypes.c_bool),
        ("adapterType", ctypes.c_int),
    ]


class ErrorStruct(ctypes.Structure):
    _fields_ = [("pattern", ctypes.c_int), ("gap", ctypes.c_byte), ("duration", ctypes.c_byte)]


class PatternConfig(ctypes.Structure):
    _fields_ = [("pattern", ctypes.c_int), ("invert", ctypes.c_bool), ("userDefined", ctypes.c_ulonglong * 2), ("repetition", ctypes.c_int)]


class SERData(ctypes.Structure):
    _fields_ = [("nSymbols", ctypes.c_int), ("InstantSER", ctypes.c_ulong * SERMAXNUMSYMBOLS), ("AccumulatedSER", ctypes.c_ulonglong * SERMAXNUMSYMBOLS)]


class RealFECData(ctypes.Structure):
    _fields_ = [
        ("enabled", ctypes.c_bool),
        ("enabledLinks", ctypes.c_bool * FECMAXNUMLINKS),
        ("lockedLinks", ctypes.c_bool * FECMAXNUMLINKS),
        ("Time", ctypes.c_double * FECMAXNUMLINKS),
        ("BitCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("FEC_Skew", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_Corrected_Ones_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_Corrected_Zeros_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_ErrorCount_Interval", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("FEC_Symbol_ErrorCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CorrectedBitCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_Symbol_ErrorRate_Interval", ctypes.c_double * FECMAXNUMLINKS),
        ("FEC_CorrectedBitRate_Interval", ctypes.c_double * FECMAXNUMLINKS),
        ("FEC_Frame_ErrorRate_Interval", ctypes.c_double * FECMAXNUMLINKS),
        ("FEC_CW_UnCorrectedCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CW_CorrectedCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CW_ProcessedCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CW_UncorrectedErrorRate_Interval", ctypes.c_double * FECMAXNUMLINKS),
        ("AccumulatedFEC_Corrected_Ones", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_Corrected_Zeros", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_ErrorCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_Symbol_ErrorCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CorrectedBitCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AveragedFEC_Symbol_ErrorRate", ctypes.c_double * FECMAXNUMLINKS),
        ("AveragedFEC_CorrectedBitRate", ctypes.c_double * FECMAXNUMLINKS),
        ("AveragedFEC_Frame_ErrorRate", ctypes.c_double * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_UnCorrectedCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_CorrectedCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_ProcessedCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_UncorrectedErrorRate", ctypes.c_double * FECMAXNUMLINKS),
        ("SER", SERData * FECMAXNUMLINKS),
        ("TotalBitCount", ctypes.c_ulonglong * MAXCHANNELS),
    ]


class EmulatorFECData(ctypes.Structure):
    _fields_ = [
        ("enabled", ctypes.c_bool),
        ("enabledLinks", ctypes.c_bool * FECMAXNUMLINKS),
        ("lockedLinks", ctypes.c_bool * FECMAXNUMLINKS),
        ("FEC_CorrectedBitError", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_BlockCount", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_SaturatedSymbolError", ctypes.c_ulong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CorrectedBitError", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_BlockCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_SaturatedSymbolError", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("SER", SERData * FECMAXNUMLINKS),
    ]


class RealFECData_4044(ctypes.Structure):
    _fields_ = [
        ("enabled", ctypes.c_bool),
        ("enabledLinks", ctypes.c_bool * FECMAXNUMLINKS),
        ("lockedLinks", ctypes.c_bool * FECMAXNUMLINKS),
        ("Time", ctypes.c_double * FECMAXNUMLINKS),
        ("BitCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("FEC_CorrectedBitCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CW_UnCorrectedCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CW_CorrectedCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CW_ProcessedCount_Interval", ctypes.c_ulong * FECMAXNUMLINKS),
        ("FEC_CW_UncorrectedErrorRate_Interval", ctypes.c_double * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_UnCorrectedCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_CorrectedCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_ProcessedCount", ctypes.c_ulonglong * FECMAXNUMLINKS),
        ("AccumulatedFEC_CW_UncorrectedErrorRate", ctypes.c_double * FECMAXNUMLINKS),
        ("SER", SERData * FECMAXNUMLINKS),
        ("TotalBitCount", ctypes.c_ulonglong * MAXCHANNELS),
    ]


class MeasurementsData(ctypes.Structure):
    _fields_ = [("berData", BERData), ("realFecData", RealFECData), ("emulatorFecData", EmulatorFECData), ("RealFECData_4044", RealFECData_4044)]


class FixedPatternDefinition(ctypes.Structure):
    _fields_ = [("Pattern", ctypes.c_ulonglong), ("Repetition", ctypes.c_byte)]


class UserDefinedPatternDefinition(ctypes.Structure):
    _fields_ = [("Pattern1", FixedPatternDefinition), ("Pattern2", FixedPatternDefinition)]


class NoiseSettings(ctypes.Structure):
    _fields_ = [
        ("NoiseLinerate", ctypes.c_double),
        ("NoiseStatus", ctypes.c_bool),
        ("NoiseChannelEnabled", ctypes.c_bool * MAXCHANNELS),
        ("NoiseLevel", ctypes.c_int * MAXCHANNELS),
        ("txPatternNoise", ctypes.c_int * MAXCHANNELS),
        ("NoiseeyeMode", ctypes.c_int),
        ("NoiseUserDefinedPattern", UserDefinedPatternDefinition * MAXCHANNELS),
    ]


class ConfigurationSettings(ctypes.Structure):
    _fields_ = [
        ("linerate", ctypes.c_double),
        ("SIGMODULATION", ctypes.c_int),
        ("grayMaping", ctypes.c_bool),
        ("preCoding", ctypes.c_bool),
        ("chipMode", ctypes.c_bool),
        ("CLOCKSOURCE", ctypes.c_int),
        ("clockType", ctypes.c_int),
        ("divider", ctypes.c_int),
        ("FEC", ctypes.c_bool),
        ("FECMODE", ctypes.c_int),
        ("FECPattern", ctypes.c_int),
        ("Tapsmode", ctypes.c_int),
        ("IEEEmode", ctypes.c_bool),
        ("AllTps", ctypes.c_bool * 7),
        ("txPattern", ctypes.c_int * MAXCHANNELS),
        ("rxPattern", ctypes.c_int * MAXCHANNELS),
        ("txInvert", ctypes.c_bool * MAXCHANNELS),
        ("rxInvert", ctypes.c_bool * MAXCHANNELS),
        ("txEnable", ctypes.c_bool * MAXCHANNELS),
        ("rxEnable", ctypes.c_bool * MAXCHANNELS),
        ("amplitude", ctypes.c_int * MAXCHANNELS),
        ("advancedAmplitude", AdvancedAmplitude * MAXCHANNELS),
        ("ampRange", AmpRange * MAXCHANNELS),
        ("Errormodes", ctypes.c_int * MAXCHANNELS),
        ("duration", ctypes.c_byte * MAXCHANNELS),
        ("gap", ctypes.c_byte * MAXCHANNELS),
        ("errorState", ctypes.c_bool * MAXCHANNELS),
        ("DSPmode", ctypes.c_int * MAXCHANNELS),
        ("calIsValid", ctypes.c_bool),
        ("noisesettings", NoiseSettings),
        ("ShallowLoopback", ctypes.c_bool),
        ("FECLinks", ctypes.c_ushort),
        ("UserDefinedPattern", UserDefinedPatternDefinition * MAXCHANNELS),
        ("AFE_Trim", ctypes.c_int),
        ("FECAvailability", ctypes.c_bool),
        ("MonitorDivider", ctypes.c_int),
        ("CDRDivider", ctypes.c_int),
        ("CDRSource", ctypes.c_int),
        ("CTLE", ctypes.c_int * MAXCHANNELS),
        ("PMenable", ctypes.c_bool),
        ("PMRJenable", ctypes.c_bool),
        ("PMamplitude", ctypes.c_ushort),
        ("PMfrequency", ctypes.c_ulonglong),
        ("PMRJamplitude", ctypes.c_ushort),
        ("PhaseShift", ctypes.c_ushort),
        ("PMPRBSamplitude", ctypes.c_ushort),
        ("PMdataswing", ctypes.c_ushort),
        ("PMpattern", ctypes.c_ushort),
        ("FMenable", ctypes.c_bool),
        ("FMRJenable", ctypes.c_bool),
        ("FMamplitude", ctypes.c_ushort),
        ("FMfrequency", ctypes.c_ulonglong),
        ("FMRJamplitude", ctypes.c_ushort),
        ("FMShift", ctypes.c_ushort),
    ]


class InstanceParams(ctypes.Structure):
    _fields_ = [
        ("saveConfig", ctypes.c_char * MAX_ADDR_LEN),
        ("saveBathtub", ctypes.c_char * MAX_ADDR_LEN),
        ("saveEye", ctypes.c_char * MAX_ADDR_LEN),
        ("saveBathtubEnable", ctypes.c_int),
        ("saveEyeEnable", ctypes.c_int),
    ]

    def __init__(self, Config, Bathtub, Eye, BathtubEnable, EyeEnable):
        self.saveConfig = bytes(Config, encoding="ASCII")
        self.saveBathtub = bytes(Bathtub, encoding="ASCII")
        self.saveEye = bytes(Eye, encoding="ASCII")
        self.saveBathtubEnable = ctypes.c_int(BathtubEnable)
        self.saveEyeEnable = ctypes.c_int(EyeEnable)


class HistogramData(ctypes.Structure):
    _fields_ = [("values", ctypes.c_ulong * 160)]


# Additional Struct and Enumeration Definitions for Adapter and Tranceiver


class ADAPTER_EXTERNALMODE(IntEnum):
    ADAPTER_EXTERNALMODE_DISABLED = (0,)
    ADAPTER_EXTERNALMODE_H_ENABLED = (1,)
    ADAPTER_EXTERNALMODE_SW_ENABLED = 2


class ADAPTER_HWSIGNAL_CNTRL(IntEnum):
    ADAPTER_HWSIGNAL_CNTRL_QDD_MODSEL_L = (0,)
    ADAPTER_HWSIGNAL_CNTRL_QDD_RESET_L = (1,)
    ADAPTER_HWSIGNAL_CNTRL_QDD_INITMODE = (2,)
    ADAPTER_HWSIGNAL_CNTRL_QSFP_MODSEL_L = (3,)
    ADAPTER_HWSIGNAL_CNTRL_QSFP_RESET_L = (4,)
    ADAPTER_HWSIGNAL_CNTRL_QSFP_LPMODE = (5,)
    ADAPTER_HWSIGNAL_CNTRL_OSFP_LPWn = (6,)
    ADAPTER_HWSIGNAL_CNTRL_OSFP_RSTn = 7


class ADAPTER_TYPE(IntEnum):
    ADAPTER_TYPE_UNDETECTED = (-1,)
    ADAPTER_TYPE_NOADAPTER = (0,)
    ADAPTER_TYPE_QDD = (1,)
    ADAPTER_TYPE_OSFP = (2,)
    ADAPTER_TYPE_QSFP = (3,)
    ADAPTER_TYPE_SFP = (4,)
    ADAPTER_TYPE_CFP2 = (5,)
    ADAPTER_TYPE_SFP_DD = 6


class TXVR_RX_AMPLITUDE(IntEnum):
    TXVR_RX_AMPLITUDE_100_400 = (0,)
    TXVR_RX_AMPLITUDE_300_600 = (1,)
    TXVR_RX_AMPLITUDE_400_800 = (2,)
    TXVR_RX_AMPLITUDE_600_1200 = (3,)
    TXVR_RX_AMPLITUDE_RESERVED = (4,)
    TXVR_RX_AMPLITUDE_CUSTOM = 15


class TXVR_MSA_PAGE(IntEnum):
    TXVR_MSA_PAGE_LOWERMEMORY = (0,)
    TXVR_MSA_PAGE_0 = (0,)
    TXVR_MSA_PAGE_1 = (1,)
    TXVR_MSA_PAGE_2 = (2,)
    TXVR_MSA_PAGE_3 = (3,)
    TXVR_MSA_PAGE_16 = (16,)
    TXVR_MSA_PAGE_17 = 17


class TXVR_ConfigurationSettings(ctypes.Structure):
    _fields_ = [
        ("DataPathDeInit", ctypes.c_bool * MAXCHANNELS),
        ("TXOuputDisable", ctypes.c_bool * MAXCHANNELS),
        ("TXPolarityFlip", ctypes.c_bool * MAXCHANNELS),
        ("TXSquelchDisable", ctypes.c_bool * MAXCHANNELS),
        ("TXForceSquelch", ctypes.c_bool * MAXCHANNELS),
        ("TXEqualization", ctypes.c_byte * MAXCHANNELS),
        ("RXOutputDisable", ctypes.c_bool * MAXCHANNELS),
        ("RXPolarityFlip", ctypes.c_bool * MAXCHANNELS),
        ("RXSquelchDisable", ctypes.c_bool * MAXCHANNELS),
        ("RXOutputAmplitude", ctypes.c_int * MAXCHANNELS),
        ("RXOutputPreCursor", ctypes.c_byte * MAXCHANNELS),
        ("RXOutputPostCursor", ctypes.c_byte * MAXCHANNELS),
    ]


############################################################################################

DLLPATH32 = r"MLBertLib\x86\BertAcquisitionManagerLib.dll"
"""str: 32-bit DLL path."""

DLLPATH64 = r"MLBertLib\x64\BertAcquisitionManagerLib.dll"
"""str: 64-bit DLL path."""

SOPATH_RHEL7 = r"MLBertLib\rhel7\libBertAcquisitionManagerLib-EL7-1.4.0.so"
"""str: RHEL7 SO path."""

SOPATH_RHEL5 = r"MLBertLib\rhel5\libBertAcquisitionManagerLib-EL5-1.4.0.so"
"""str: RHEL5 SO path."""


class _IntPtr(ctypes.Structure):
    """Temporary structure for IntPtr creation."""

    pass


class IntPtr(ctypes.POINTER(_IntPtr)):
    """Structure pointer used as class pointer."""

    pass


class mlbertmgr(object):
    """mlbert Manager API Wrapper class."""

    def __init__(self):
        """Create new mlbertmgr API Wrapper instance."""
        self._Is64 = sys.maxsize > 2**32
        if os.name != "nt":
            dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), SOPATH_RHEL7)
        else:
            dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), DLLPATH64)
        dlldir = os.path.dirname(dll_path)

        os.environ["PATH"] = dlldir + ";" + os.environ["PATH"]
        # dll_path = "/home/oxygen/work/pymeasure/pymeasure/instruments/multilane/mlbert_thunderapi_python_v1.4.0_20211111/mlbert_thunderapi_python_v1.4.0_20211111/pymlbertapi/MLBertLib/rhel7/libBertAcquisitionManagerLib-EL7-1.4.0.so"
        self._api = ctypes.cdll.LoadLibrary(dll_path)
        self._api.mlbertmgr_createInstance.restype = IntPtr
        self.instance = self._api.mlbertmgr_createInstance()
        self.ip = "172.16.110.101"
        SUCCESS = self.mlbertmgr_openConnection(ip=self.ip)
        if SUCCESS != BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to connect to %s!" % self.ip, " : ", SUCCESS)
        logging.info(f"BERT connected on {self.ip}")

        self.SAVE_CONFIG = ""
        self.SAVE_BATHTUB = ""
        self.SAVE_EYE = ""
        self.SAVE_BATHTUB_ENABLE = 0
        self.SAVE_EYE_ENABLE = 0
        self.T_PARAMS = InstanceParams(self.SAVE_CONFIG, self.SAVE_BATHTUB, self.SAVE_EYE, self.SAVE_BATHTUB_ENABLE, self.SAVE_EYE_ENABLE)

        SUCCESS = self.mlbertmgr_initializeInstance(self.T_PARAMS)
        if SUCCESS != BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to initialize Instance ! : ", SUCCESS)
        logging.info("Instance initialized")

    def setup_clock(self, source="internal", mode="refclk", monitor_divider=None, cdr_divider=None):
        # Clock Source
        if source.lower() == "internal":
            CLOCKSOURCE = BERTMGR_CLOCKSOURCE.BERTMGR_INTERNALCLKSRC
            logging.info("Clock source internal")
        else:
            CLOCKSOURCE = BERTMGR_CLOCKSOURCE.BERTMGR_EXTERNALCLKSRC
            logging.info("Clock source external")

        # Output Clock Mode
        if mode.lower() == "refclk":
            CLOCKMODE = BERTMGR_CLOCKMODE.BERTMGR_REFCLK
            logging.info("Clock mode refclk")
        else:
            logging.warning(f"Clock mode '{mode}' not supported, refer to manual")

        # Monitor Divider
        if monitor_divider is not None:
            DIVIDER = BERTMGR_MONITORDIVIDER.BERTMGR_MONITOR_DIV4
            logging.warning(f"Monitor divider '{monitor_divider}' not supported, refer to manual")
        else:
            logging.info("No monitor divider selected")

        # CDR Divider
        if cdr_divider is not None:
            CDRDIVIDER = BERTMGR_CDRDIVIDER.BERTMGR_CDR_DIV32
            logging.warning(f"CDR divider '{cdr_divider}' not supported, refer to manual")
        else:
            logging.info("No CDR divider selected")

    def configure_txrx(self, modulation="pam4", baudrate=56, prbs="PRBS31", amplitude=200, invert="off"):
        TXPATTERN = PatternConfig()
        RXPATTERN = PatternConfig()
        APPLYCONFIG = True

        # MODULATION CONTROL
        if modulation.lower() == "pam4":
            EYEMODE = BERTMGR_SIGMODULATION.BERTMGR_PAM4
            logging.info("PAM4 modulation selected")
        elif modulation.lower() == "nrz":
            EYEMODE = BERTMGR_SIGMODULATION.BERTMGR_NRZ
            logging.info("NRZ modulation selected")
        else:
            raise Exception("Modulation must be 'PAM4' or 'NRZ'")

        # LINE RATE CONTROL
        if baudrate <= 112:
            SUCCESS = self.mlbertmgr_setLinerate(baudrate, APPLYCONFIG)
            if SUCCESS != BERTMGR_STATUS.BERTMGR_SUCCESS:
                raise Exception("Failed to set Line rate! : ", SUCCESS)
            logging.info(f"Baud rate selected: {baudrate}G")
        else:
            raise Exception("Baud rate must be less than 112G")

        # PATTERN CONTROL
        self.supported_patterns = dir(BERTMGR_PATTERNTYPE)
        prbs_string = [p for p in self.supported_patterns if prbs.upper() in p]
        if prbs_string == []:
            logging.warning(f"PRBS pattern '{prbs}' not supported, refer to manual")
        elif len(prbs_string) == 1:
            TXPATTERN.pattern = eval("BERTMGR_PATTERNTYPE." + f"{prbs_string[0]}")
            logging.info(f"PRBS pattern selected: {prbs}G")
        else:
            logging.warning(f"PRBS pattern selected is ambiguous, be more specific")

        # AMPLITUDE CONTROL
        channel = 1
        amplitude = 175
        SUCCESS = self.mlbertmgr_setAmplitude(channel, amplitude, APPLYCONFIG)
        if SUCCESS != BERTMGR_STATUS.BERTMGR_SUCCESS:
            raise Exception("Failed to set Amplitude Level! : ", SUCCESS)
        print("Amplitude Level is set !")

        # INVERT CONTROL
        self.invert_list = ["off", "tx", "rx", "txrx"]
        if invert.lower() not in self.invert_list:
            raise Exception(f"Invert must be one of {self.invert_list}")
        else:
            self.invert_vals = "{0:02b}".format(self.invert_list.index(invert))
            TXPATTERN.invert = bool(int(self.invert_vals[1]))
            RXPATTERN.invert = bool(int(self.invert_vals[0]))
            logging.info(f"Invert settings, tx: {TXPATTERN.invert}, rx: {RXPATTERN.invert}")

    def mlbertmgr_destroyInstance(self):
        self._api.mlbertmgr_destroyInstance(self.instance)

    def mlbertmgr_openConnection(self, ip):
        IP = bytes(ip, encoding="ASCII")
        self._api.mlbertmgr_openConnection.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_openConnection(self.instance, IP)

    def mlbertmgr_initializeInstance(self, InstanceParams):
        self._api.mlbertmgr_initializeInstance.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_initializeInstance(self.instance, InstanceParams)

    def mlbertmgr_closeConnection(self):
        self._api.mlbertmgr_closeConnection.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_closeConnection(self.instance)

    def mlbertmgr_getActiveConfig(self, ConfigurationSettings):
        self._api.mlbertmgr_getActiveConfig.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getActiveConfig(self.instance, ConfigurationSettings)

    def mlbertmgr_applyConfiguration(self):
        self._api.mlbertmgr_applyConfiguration.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_applyConfiguration(self.instance)

    def mlbertmgr_setLinerate(self, linerate, applyConfig):
        self._api.mlbertmgr_setLinerate.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setLinerate(self.instance, ctypes.pointer(ctypes.c_double(linerate)), ctypes.c_bool(applyConfig))

    def mlbertmgr_setTxPattern(self, channel, PatternConfig, applyConfig):
        self._api.mlbertmgr_setTxPattern.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setTxPattern(self.instance, ctypes.c_int(channel), PatternConfig, ctypes.c_bool(applyConfig))

    def mlbertmgr_setRxPattern(self, channel, PatternConfig, applyConfig):
        self._api.mlbertmgr_setRxPattern.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setRxPattern(self.instance, ctypes.c_int(channel), PatternConfig, ctypes.c_bool(applyConfig))

    def mlbertmgr_setEyeMode(self, eyeMode, applyConfig):
        self._api.mlbertmgr_setEyeMode.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setEyeMode(self.instance, eyeMode, ctypes.c_bool(applyConfig))

    def mlbertmgr_setClockSource(self, CLOCKSOURCE, applyConfig):
        self._api.mlbertmgr_setClockSource.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setClockSource(self.instance, ctypes.c_int(CLOCKSOURCE), ctypes.c_bool(applyConfig))

    def mlbertmgr_setClockMode(self, CLOCKMODE, applyConfig):
        self._api.mlbertmgr_setClockMode.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setClockMode(self.instance, ctypes.c_int(CLOCKMODE), ctypes.c_bool(applyConfig))

    def mlbertmgr_setMonitorDivider(self, divider, applyConfig):
        self._api.mlbertmgr_setMonitorDivider.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setMonitorDivider(self.instance, ctypes.c_int(divider), ctypes.c_bool(applyConfig))

    def mlbertmgr_getClockOut(self, clockOutRate):
        self._api.mlbertmgr_getClockOut.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getClockOut(self.instance, clockOutRate)

    def mlbertmgr_setAmplitude(self, channel, amplitude, applyConfig):
        self._api.mlbertmgr_setAmplitude.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setAmplitude(self.instance, ctypes.c_int(channel), ctypes.c_int(amplitude), ctypes.c_bool(applyConfig))

    def mlbertmgr_getInfo(self, Board_Info):
        self._api.mlbertmgr_getInfo.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getInfo(self.instance, Board_Info)

    def mlbertmgr_setMainTap(self, channel, mainTap, applyConfig):
        self._api.mlbertmgr_setMainTap.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setMainTap(self.instance, ctypes.c_int(channel), ctypes.c_int(mainTap), ctypes.c_bool(applyConfig))

    def mlbertmgr_setPostEmphasis(self, channel, postEmphasis, applyConfig):
        self._api.mlbertmgr_setPostEmphasis.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setPostEmphasis(self.instance, ctypes.c_int(channel), ctypes.c_int(postEmphasis), ctypes.c_bool(applyConfig))

    def mlbertmgr_setPreEmphasis(self, channel, preEmphasis, applyConfig):
        self._api.mlbertmgr_setPreEmphasis.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setPreEmphasis(self.instance, ctypes.c_int(channel), ctypes.c_int(preEmphasis), ctypes.c_bool(applyConfig))

    def mlbertmgr_setInnerEyeLevel(self, channel, innerEye, applyConfig):
        self._api.mlbertmgr_setInnerEyeLevel.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setInnerEyeLevel(self.instance, ctypes.c_int(channel), ctypes.c_int(innerEye), ctypes.c_bool(applyConfig))

    def mlbertmgr_setOuterEyeLevel(self, channel, outerEye, applyConfig):
        self._api.mlbertmgr_setOuterEyeLevel.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setOuterEyeLevel(self.instance, ctypes.c_int(channel), ctypes.c_int(outerEye), ctypes.c_bool(applyConfig))

    def mlbertmgr_setScalingLevel(self, channel, scalingLevel, applyConfig):
        self._api.mlbertmgr_setScalingLevel.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setScalingLevel(self.instance, ctypes.c_int(channel), ctypes.c_int(scalingLevel), ctypes.c_bool(applyConfig))

    def mlbertmgr_setAdvancedAmplitude(self, channel, AdvancedAmplitude, output, applyConfig):
        self._api.mlbertmgr_setAdvancedAmplitude.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setAdvancedAmplitude(self.instance, ctypes.c_int(channel), AdvancedAmplitude, output, ctypes.c_bool(applyConfig))

    def mlbertmgr_setGrayCoding(self, enable, applyConfig):
        self._api.mlbertmgr_setGrayCoding.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setGrayCoding(self.instance, ctypes.c_bool(enable), ctypes.c_bool(applyConfig))

    def mlbertmgr_setFECMode(self, BERTMGR_FECMODE, BERTMGR_FECPATTERN, applyConfig):
        self._api.mlbertmgr_setFECMode.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setFECMode(self.instance, ctypes.c_int(BERTMGR_FECMODE), ctypes.c_int(BERTMGR_FECPATTERN), ctypes.c_bool(applyConfig))

    def mlbertmgr_getGrayCoding(self, isEnabled):
        self._api.mlbertmgr_getGrayCoding.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getGrayCoding(self.instance, isEnabled)

    def mlbertmgr_enableMonitor(self, enabledFlagsValue):
        self._api.mlbertmgr_enableMonitor.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_enableMonitor(self.instance, ctypes.c_int(enabledFlagsValue))

    def mlbertmgr_enableMonitorFlag(self, BERTMGR_MONITOR_FLAGS, isEnabled):
        self._api.mlbertmgr_enableMonitorFlag.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_enableMonitorFlag(self.instance, BERTMGR_MONITOR_FLAGS, ctypes.c_bool(isEnabled))

    def mlbertmgr_singleReadMonitor(self, BERTMGR_MONITOR_FLAGS, value):
        self._api.mlbertmgr_singleReadMonitor.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_singleReadMonitor(self.instance, ctypes.c_int(BERTMGR_MONITOR_FLAGS), value)

    def mlbertmgr_multiReadMonitor(self, enabledFlagsValue, values):
        self._api.mlbertmgr_multiReadMonitor.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_multiReadMonitor(self.instance, ctypes.c_int(enabledFlagsValue), values)

    def mlbertmgr_readLOS(self, value):
        self._api.mlbertmgr_readLOS.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_readLOS(self.instance, value)

    def mlbertmgr_startBER(self, channels, accumulate):
        return self._api.mlbertmgr_startBER(self.instance, ctypes.c_ushort(channels), ctypes.c_bool(accumulate))

    def mlbertmgr_getAvailableBERData(self, MeasurementsData, datacount):
        self._api.mlbertmgr_getAvailableBERData.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getAvailableBERData(self.instance, MeasurementsData, datacount)

    def mlbertmgr_stopBER(self):
        self._api.mlbertmgr_stopBER.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_stopBER(self.instance)

    def mlbertmgr_RxEnable(self, channel, status):
        self._api.mlbertmgr_RxEnable.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_RxEnable(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mlbertmgr_getRxStatus(self, channel, isEnabled):
        self._api.mlbertmgr_getRxStatus.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getRxStatus(self.instance, ctypes.c_int(channel), isEnabled)

    def mlbertmgr_TxEnable(self, channel, status):
        self._api.mlbertmgr_TxEnable.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_TxEnable(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mlbertmgr_getTxStatus(self, channel, isEnabled):
        self._api.mlbertmgr_getTxStatus.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getTxStatus(self.instance, ctypes.c_int(channel), isEnabled)

    def mlbertmgr_setErrorRate(self, channel, rate, actualrate, applyConfig):
        self._api.mlbertmgr_setErrorRate.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setErrorRate(self.instance, ctypes.c_int(channel), ctypes.c_double(rate), actualrate, ctypes.c_bool(applyConfig))

    def mlbertmgr_setErrorPattern(self, channel, ErrorStruct, applyConfig):
        self._api.mlbertmgr_setErrorPattern.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setErrorPattern(self.instance, ctypes.c_int(channel), ErrorStruct, ctypes.c_bool(applyConfig))

    def mlbertmgr_stopErrorInsertion(self, channel, applyConfig):
        self._api.mlbertmgr_stopErrorInsertion.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_stopErrorInsertion(self.instance, ctypes.c_int(channel), ctypes.c_bool(applyConfig))

    def mlbertmgr_getTxEmulationTapsFromLossAtNyquist(self, taps, lossDb):
        self._api.mlbertmgr_getTxEmulationTapsFromLossAtNyquist.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getTxEmulationTapsFromLossAtNyquist(self.instance, taps, ctypes.c_double(lossDb))

    def mlbertmgr_getTxEmulationTapsFromSParams(self, taps, s2pFilePath):
        self._api.mlbertmgr_getTxEmulationTapsFromSParams.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getTxEmulationTapsFromSParams(self.instance, taps, s2pFilePath)

    def mlbertmgr_loadCalibrationValues(self, channel, mode, data, lenData, applyConfig):
        self._api.mlbertmgr_loadCalibrationValues.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_loadCalibrationValues(self.instance, ctypes.c_int(channel), ctypes.c_int(mode), data, lenData, ctypes.c_bool(applyConfig))

    def mlbertmgr_loadOptimalSettings(self, channel, mode, data, lenData, applyConfig):
        self._api.mlbertmgr_loadOptimalSettings.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_loadOptimalSettings(self.instance, ctypes.c_int(channel), ctypes.c_int(mode), data, lenData, ctypes.c_bool(applyConfig))

    def mlbertmgr_setTapsMode(self, BERTMGR_TAPSMODE, applyConfig):
        self._api.mlbertmgr_setTapsMode.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setTapsMode(self.instance, ctypes.c_int(BERTMGR_TAPSMODE), ctypes.c_bool(applyConfig))

    def mlbertmgr_setDSPMode(self, channel, BERTMGR_DSPMODE, applyConfig):
        self._api.mlbertmgr_setDSPMode.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setDSPMode(self.instance, ctypes.c_int(channel), ctypes.c_int(BERTMGR_DSPMODE), ctypes.c_bool(applyConfig))

    def mlbertmgr_getHistogramData(self, enabledChannels, HistogramData):
        self._api.mlbertmgr_getHistogramData.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_getHistogramData(self.instance, ctypes.c_ushort(enabledChannels), HistogramData)

    def mlbertmgr_captureHistogramData(self, enabledChannels, actualEnabled):
        self._api.mlbertmgr_captureHistogramData.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_captureHistogramData(self.instance, ctypes.c_ushort(enabledChannels), actualEnabled)

    def mlbertmgr_readHistogramData(self, channel, HistogramData):
        self._api.mlbertmgr_readHistogramData.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_readHistogramData(self.instance, ctypes.c_ushort(channel), HistogramData)

    def mlbertmgr_setActiveConfig(self, ConfigurationSettings, forceUpdate):
        self._api.mlbertmgr_setActiveConfig.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setActiveConfig(self.instance, ConfigurationSettings, forceUpdate)

    def mlbertmgr_setNoiseLinerate(self, linerate, applyConfig):
        self._api.mlbertmgr_setNoiseLinerate.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setNoiseLinerate(self.instance, linerate, ctypes.c_bool(applyConfig))

    def mlbertmgr_enableNoise(self, channel, enable, applyConfig):
        self._api.mlbertmgr_enableNoise.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_enableNoise(self.instance, ctypes.c_int(channel), ctypes.c_bool(enable), ctypes.c_bool(applyConfig))

    def mlbertmgr_setNoiseLevel(self, channel, NoiseLevel, applyConfig):
        self._api.mlbertmgr_setNoiseLevel.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setNoiseLevel(self.instance, ctypes.c_int(channel), ctypes.c_int(NoiseLevel), ctypes.c_bool(applyConfig))

    def mlbertmgr_setNoiseTxPattern(self, channel, PatternConfig, applyConfig):
        self._api.mlbertmgr_setNoiseTxPattern.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setNoiseTxPattern(self.instance, ctypes.c_int(channel), PatternConfig, ctypes.c_bool(applyConfig))

    def mlbertmgr_setNoiseEyeMode(self, eyeMode, applyConfig):
        self._api.mlbertmgr_setNoiseEyeMode.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setNoiseEyeMode(self.instance, eyeMode, ctypes.c_bool(applyConfig))

    def mlbertmgr_setShallowLoopback(self, enable, applyConfig):
        self._api.mlbertmgr_setShallowLoopback.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setShallowLoopback(self.instance, ctypes.c_bool(enable), ctypes.c_bool(applyConfig))

    def mlbertmgr_setNoiseStatus(self, enable, applyConfig):
        self._api.mlbertmgr_setNoiseStatus.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setNoiseStatus(self.instance, ctypes.c_bool(enable), ctypes.c_bool(applyConfig))

    def mlbertmgr_setNoiseBurstRate(self, channel, burstRate, actualrate, applyConfig):
        self._api.mlbertmgr_setNoiseBurstRate.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setNoiseBurstRate(self.instance, ctypes.c_int(channel), ctypes.c_double(burstRate), actualrate, ctypes.c_bool(applyConfig))

    def mlbertmgr_configureFECLinks(self, channels, skipReset, applyConfig):
        self._api.mlbertmgr_configureFECLinks.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_configureFECLinks(self.instance, ctypes.c_ushort(channels), ctypes.c_bool(skipReset), ctypes.c_bool(applyConfig))

    def mlbertmgr_setUserDefinedPattern(self, channel, UserDefinedPatternDefinition, applyConfig):
        self._api.mlbertmgr_setUserDefinedPattern.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setUserDefinedPattern(self.instance, ctypes.c_int(channel), UserDefinedPatternDefinition, ctypes.c_bool(applyConfig))

    def mlbertmgr_setAFETrim(self, BERTMGR_AFETRIM_OPT, applyConfig):
        self._api.mlbertmgr_setAFETrim.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setAFETrim(self.instance, BERTMGR_AFETRIM_OPT, ctypes.c_bool(applyConfig))

    def mlbertmgr_setCDRDivider(self, BERTMGR_CDRDIVIDER, applyConfig):
        self._api.mlbertmgr_setCDRDivider.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setCDRDivider(self.instance, ctypes.c_int(BERTMGR_CDRDIVIDER), ctypes.c_bool(applyConfig))

    def mlbertmgr_setCDRChannelSource(self, option, applyConfig):
        self._api.mlbertmgr_setCDRChannelSource.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setCDRChannelSource(self.instance, ctypes.c_int(option), ctypes.c_bool(applyConfig))

    def mlbertmgr_setCTLE(self, channel, CTLE, applyConfig):
        self._api.mlbertmgr_setCTLE.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setCTLE(self.instance, ctypes.c_int(channel), ctypes.c_int(CTLE), ctypes.c_bool(applyConfig))

    # Additional functions for Adapter and Tranceiver

    def mlbertmgr_detectAdapter(self, type):
        self._api.mlbertmgr_detectAdapter.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_detectAdapter(self.instance, type)

    def mlbertmgr_setControlPin(self, ADAPTER_HWSIGNAL_CNTRL, status):
        self._api.mlbertmgr_setControlPin.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setControlPin(self.instance, ctypes.c_int(ADAPTER_HWSIGNAL_CNTRL), ctypes.c_bool(status))

    def mlbertmgr_setExternalAdapterMode(self, isEnabled):
        self._api.mlbertmgr_setExternalAdapterMode.restype = BERTMGR_STATUS
        return self._api.mlbertmgr_setExternalAdapterMode(self.instance, ctypes.c_bool(isEnabled))

    def mltxvr_sequentialRead(self, pageSelect, registerAddress, dataLength, dataBuffer, bankSelect):
        self._api.mltxvr_sequentialRead.restype = BERTMGR_STATUS
        return self._api.mltxvr_sequentialRead(
            self.instance, ctypes.c_ushort(pageSelect), ctypes.c_ushort(registerAddress), ctypes.c_ushort(dataLength), dataBuffer, ctypes.c_ushort(0)
        )

    def mltxvr_sequentialWrite(self, pageSelect, registerAddress, dataLength, dataBuffer, bankSelect):
        self._api.mltxvr_sequentialWrite.restype = BERTMGR_STATUS
        return self._api.mltxvr_sequentialWrite(
            self.instance, ctypes.c_ushort(pageSelect), ctypes.c_ushort(registerAddress), ctypes.c_ushort(dataLength), dataBuffer, ctypes.c_ushort(0)
        )

    def mltxvr_setTxOutputDisable(self, channel, status):
        self._api.mltxvr_setTxOutputDisable.restype = BERTMGR_STATUS
        return self._api.mltxvr_setTxOutputDisable(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setTxDataPathDeInit(self, channel, status):
        self._api.mltxvr_setTxDataPathDeInit.restype = BERTMGR_STATUS
        return self._api.mltxvr_setTxDataPathDeInit(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setTxForceSquelch(self, channel, status):
        self._api.mltxvr_setTxForceSquelch.restype = BERTMGR_STATUS
        return self._api.mltxvr_setTxForceSquelch(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setTxSquelchDisable(self, channel, status):
        self._api.mltxvr_setTxSquelchDisable.restype = BERTMGR_STATUS
        return self._api.mltxvr_setTxSquelchDisable(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setTxPolarityFlip(self, channel, status):
        self._api.mltxvr_setTxPolarityFlip.restype = BERTMGR_STATUS
        return self._api.mltxvr_setTxPolarityFlip(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setTxInputEqualization(self, channel, value):
        self._api.mltxvr_setTxInputEqualization.restype = BERTMGR_STATUS
        return self._api.mltxvr_setTxInputEqualization(self.instance, ctypes.c_int(channel), ctypes.c_int(value))

    def mltxvr_getActiveConfig(self, TXVR_ConfigurationSettings):
        self._api.mltxvr_getActiveConfig.restype = BERTMGR_STATUS
        return self._api.mltxvr_getActiveConfig(self.instance, TXVR_ConfigurationSettings)

    def mltxvr_setRxPolarityFlip(self, channel, status):
        self._api.mltxvr_setRxPolarityFlip.restype = BERTMGR_STATUS
        return self._api.mltxvr_setRxPolarityFlip(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setRxSquelchDisable(self, channel, status):
        self._api.mltxvr_setRxSquelchDisable.restype = BERTMGR_STATUS
        return self._api.mltxvr_setRxSquelchDisable(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setRxOutputDisable(self, channel, status):
        self._api.mltxvr_setRxOutputDisable.restype = BERTMGR_STATUS
        return self._api.mltxvr_setRxOutputDisable(self.instance, ctypes.c_int(channel), ctypes.c_bool(status))

    def mltxvr_setRxPreCursor(self, channel, value):
        self._api.mltxvr_setRxPreCursor.restype = BERTMGR_STATUS
        return self._api.mltxvr_setRxPreCursor(self.instance, ctypes.c_int(channel), ctypes.c_int(value))

    def mltxvr_setRxPostCursor(self, channel, value):
        self._api.mltxvr_setRxPostCursor.restype = BERTMGR_STATUS
        return self._api.mltxvr_setRxPostCursor(self.instance, ctypes.c_int(channel), ctypes.c_int(value))

    def mltxvr_setRxAmplitude(self, channel, TXVR_RX_AMPLITUDE):
        self._api.mltxvr_setRxAmplitude.restype = BERTMGR_STATUS
        return self._api.mltxvr_setRxAmplitude(self.instance, ctypes.c_int(channel), ctypes.c_int(TXVR_RX_AMPLITUDE))

    def mltxvr_getMSAValues(self, TXVR_MSA_PAGE, values, numberOfPages):
        self._api.mltxvr_getMSAValues.restype = BERTMGR_STATUS
        return self._api.mltxvr_getMSAValues(self.instance, TXVR_MSA_PAGE, values, ctypes.c_ubyte(numberOfPages))
