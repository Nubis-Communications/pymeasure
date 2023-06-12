/**
 * BERT Manager Wrapper Layer Library header.
 */
#pragma once
#ifndef ML_BERT_MANAGER_H__
#define ML_BERT_MANAGER_H__

#ifndef BERTMGRAPICALL
#ifdef __cplusplus
#   ifdef _WIN32
#       ifndef ML_IMPORTS_BERTMGRAPI
#           define BERTMGRAPICALL extern "C" __declspec(dllexport)
#       else
#           define BERTMGRAPICALL extern "C" __declspec(dllimport)
#       endif
#   else
#       define BERTMGRAPICALL extern "C" 
#   endif // WIN32
#else
#   define BERTMGRAPICALL
#endif
#endif

#ifdef __cplusplus
#   ifdef _WIN32
//#define BERTMGRSTACKMODE    __stdcall
#       define BERTMGRSTACKMODE    __cdecl
#   else
#       define BERTMGRSTACKMODE
#   endif //WIN32
#else
#define BERTMGRSTACKMODE
#endif

 //  cdecl convention call prevents mangled function names in the x86 DLL export table.
//#define BERTMGRSTACKMODE   __cdecl

#define     BERMAXITEMSPOP          1024    // Maximum number of BER measurements per acquisition
#define     SERMAXNUMSYMBOLS        31      // Maximum number of SER symbols
#define     FECMAXNUMLINKS          8      // Maximum number of FEC links

// Static version of the library
#define BERTMGR_API_VERSION_MAJOR 1
#define BERTMGR_API_VERSION_MINOR 4
#define BERTMGR_API_VERSION_REVISION 0

struct mlbertmgr_api_version {
	int major;
	int minor;
	int revision;
};

enum { BERTMGRVERSION = 18 };   // Module incremental version

typedef unsigned char byte;

#ifdef _WIN32
typedef unsigned short ushort; // natively defined as unsigned short in Linux (16-bit)
typedef unsigned long uint; // natively defined as unsigned int in Linux (32-bit)
typedef unsigned long long ulong; // natively defined as unsigned long in Linux (64-bit)
#else
#include <sys/types.h>
#endif

#define MAX_ADDR_LEN        256
#define MAXCHANNELS     8


typedef struct mlbertmgr mlbertmgr;   // API wrapper structure

/// <summary>
/// API call status 
/// </summary>
typedef enum BERTMGR_STATUS
{
	BERTMGR_SUCCESS,
	BERTMGR_FAILED,
	BERTMGR_TIMEOUT,
	BERTMGR_UNEXPECTED_ERROR,
	BERTMGR_UNSUPPORTED_OPTION,
	BERTMGR_BER_DISABLED
}BERTMGR_STATUS;

/// <summary>
/// Signal modulation mode 
/// </summary>
typedef enum BERTMGR_SIGMODULATION
{
	BERTMGR_PAM4 = 0,
	BERTMGR_NRZ = 1
}BERTMGR_SIGMODULATION;

/// <summary>
/// Tx and Rx Pattern Type 
/// </summary>
typedef enum BERTMGR_PATTERNTYPE
{
	BERTMGR_PRBS7 = 0,
	BERTMGR_PRBS9_4 = 1,
	BERTMGR_PRBS9_5 = 2,
	BERTMGR_PRBS11 = 3,
	BERTMGR_PRBS13 = 4,
	BERTMGR_PRBS15 = 5,
	BERTMGR_PRBS16 = 6,
	BERTMGR_PRBS23 = 7,
	BERTMGR_PRBS31 = 8,
	BERTMGR_PRBS58 = 9,
	BERTMGR_USERDEFINED = 10,
	BERTMGR_JP03B = 11,
	BERTMGR_LIN = 12,
	BERTMGR_CJT = 13,
	BERTMGR_SSPRQ = 14,
	BERTMGR_SQ16 = 15,
	BERTMGR_SQ32 = 16,
	BERTMGR_IEEE8023BS_2 = 17,
	BERTMGR_IEEE8023BS_4 = 18,
	BERTMGR_OIFCEI311 = 19,
}BERTMGR_PATTERNTYPE;

/// <summary>
/// Clock source either Internal or External 
/// </summary>
typedef enum BERTMGR_CLOCKSOURCE
{
	BERTMGR_EXTERNALCLKSRC = 0,
	BERTMGR_INTERNALCLKSRC = 1
}BERTMGR_CLOCKSOURCE;

/// <summary>
/// Output clock mode 
/// </summary>
typedef enum BERTMGR_CLOCKMODE
{
	BERTMGR_MONITORCLOCK_CH0toCH3 = 0,
	BERTMGR_EXTERNAL = 1,
	BERTMGR_REFCLK = 2,
	BERTMGR_MONITORCLOCK_CH4toCH7 = 3,
	BERTMGR_CDR_CH0toCH3 = 4,
	BERTMGR_CDR_CH4toCH7 = 5,
	BERTMGR_REFCLK2 = 6
}BERTMGR_CLOCKMODE;

/// <summary>
/// Monitor Instrument Flags
/// </summary>
typedef enum BERTMGR_MONITOR_FLAGS
{
	BERTMGR_MONITOR_LOS = 0x1 << 0,             // LOS Enable Flag (bit 0)
	BERTMGR_MONITOR_DSP = 0x1 << 1,             // DSP Monitor Enable Flag (bit 1)
	BERTMGR_MONITOR_SIGNALDETECT = 0x1 << 2,    // Signal Detect Monitor Flag (bit 2)
	BERTMGR_MONITOR_TXLOCK = 0x1 << 3,          // Tx Lock Monitor Flag (bit 3)
	BERTMGR_MONITOR_RXLOCK = 0x1 << 4,          // RX Lock Monitor Flag (bit 4)
	BERTMGR_MONITOR_TEMPERATURE = 0x1 << 5,     // Temperature Monitor Flag (bit 5)
	BERTMGR_MONITOR_SNR = 0x1 << 6,             // SNR Monitor Flag (bit 6), 10*SNR Monitoring value 
	BERTMGR_MONITOR_VOLTAGE = 0x1 << 7,         // Voltage Monitor Flag (bit 7)
	BERTMGR_MONITOR_CURRENT = 0x1 << 8,         // Current Monitor Flag (bit 8)
	BERTMGR_MONITOR_FFETAPS = 0x1 << 9,         // FFE Taps Monitor Flag (bit 9)
    BERTMGR_MONITOR_XT_TXLOCK = 0x1 << 10,
    BERTMGR_MONITOR_ADAPTER = 0x1 << 11,
    BERTMGR_MONITOR_TRANSCEIVER = 0x1 << 12
}BERTMGR_MONITOR_FLAGS;

/// <summary>
/// Error Insertion mode 
/// </summary>
typedef enum BERTMGR_ERRORINSERTIONMODES
{
	BERTMGR_ERRINJ_PAT_BIT0,    // bit 0 one MSB
	BERTMGR_ERRINJ_PAT_BIT1,    // bit 1 one LSB
	BERTMGR_ERRINJ_PAT_BIT01,   // bit 0 and 1 one PAM4 (MSB and LSB)
	BERTMGR_ERRINJ_PAT_MSBS,    // all MSBs
	BERTMGR_ERRINJ_PAT_LSBS,    // all LSBs
	BERTMGR_ERRINJ_PAT_ALL      // all bits
}BERTMGR_ERRORINSERTIONMODES;

/// <summary>
/// Error Struct 
/// </summary>
struct ErrorStruct
{
	BERTMGR_ERRORINSERTIONMODES pattern;
	byte gap;
	byte duration;
};

/// <summary>
/// FEC Mode 
/// </summary>
typedef enum BERTMGR_FECMODE
{
	BERTMGR_FECDISABLED = -1,
	BERTMGR_400G_KP8_TO_KP4 = 0,
	BERTMGR_200G_KP4_TO_KP2 = 1,
	BERTMGR_200G_KP4_TO_KP4 = 2,
	BERTMGR_100G_KP2_TO_KP1 = 3,
	BERTMGR_100G_KP4_TO_KP4 = 4,
	BERTMGR_100G_KP4_TO_KP2 = 5,
	BERTMGR_100G_PCS4_TO_KR1 = 6,
	BERTMGR_50G_KP1_TO_KP1 = 7,
	BERTMGR_50G_KP2_TO_KP2 = 8,
	BERTMGR_50G_KR2_TO_KR1 = 9,
	BERTMGR_25G_KR1_TO_KR1 = 10,
	BERTMGR_25G_KP1_TO_KP1 = 11,
	BERTMGR_50G_KS = 20,
	BERTMGR_50G_KR = 21,
	BERTMGR_50G_KP = 22,
	BERTMGR_100G_KR = 23,
	BERTMGR_100G_KP = 24,
	BERTMGR_200G_KP = 25,
	BERTMGR_400G_KP = 26,
	//  ML4054B FEC Modes
    BERTMGR_25G_FC = 40,
    BERTMGR_25G_KR4 = 41,
    BERTMGR_25G_KP4 = 42,
    BERTMGR_50G_FC = 43,
    BERTMGR_50G_KR4 = 44,
    BERTMGR_50G_KP4 = 45,
    BERTMGR_100G_FC = 46,
    BERTMGR_100G_KR4 = 47,
    BERTMGR_100G_KP4 = 48,
    BERTMGR_200G_FC = 49,
    BERTMGR_200G_KR4 = 50,
    BERTMGR_200G_KP4 = 51
}BERTMGR_FECMODE;

/// <summary>
/// FEC pattern 
/// </summary>
typedef enum BERTMGR_FECPATTERN
{
    BERTMGR_FECPATTERN_DISABLED = -1,
    BERTMGR_FECPATTERN_IDLE = 0,
    BERTMGR_FECPATTERN_LOCALFAULT = 1,
    BERTMGR_FECPATTERN_REMOTEFAULT = 2
}BERTMGR_FECPATTERN;

/// <summary>
/// Calibration modes
/// </summary>
typedef enum BERTMGR_CALIBRATIONMODE
{
	BERTMGR_CALMODE_ADV = -1,   // Advanced mode
	BERTMGR_CALMODE_LRLV = 0,   // Low-rate/low-voltage
	BERTMGR_CALMODE_LRHV = 1,   // Low-rate/high-voltage
	BERTMGR_CALMODE_HRLV = 2,   // High-rate/low-voltage
	BERTMGR_CALMODE_HRHV = 3,   // High-rate/high-voltage
}BERTMGR_CALIBRATIONMODE;

/// <summary>
/// Adapter type 
/// </summary>
typedef enum ADAPTER_TYPE
{
    ADAPTER_TYPE_UNDETECTED = -1,
    ADAPTER_TYPE_NOADAPTER = 0,
    ADAPTER_TYPE_QDD = 1,
    ADAPTER_TYPE_OSFP = 2,
    ADAPTER_TYPE_QSFP = 3,
    ADAPTER_TYPE_SFP = 4,
    ADAPTER_TYPE_CFP2 = 5,
    ADAPTER_TYPE_SFP_DD = 6,
}ADAPTER_TYPE;

/// <summary>
/// Adapter hardware signal control 
/// </summary>
typedef enum ADAPTER_HWSIGNAL_CNTRL
{
    ADAPTER_HWSIGNAL_CNTRL_QDD_MODSEL_L,
    ADAPTER_HWSIGNAL_CNTRL_QDD_RESET_L,
    ADAPTER_HWSIGNAL_CNTRL_QDD_INITMODE,
    ADAPTER_HWSIGNAL_CNTRL_QSFP_MODSEL_L,
    ADAPTER_HWSIGNAL_CNTRL_QSFP_RESET_L,
    ADAPTER_HWSIGNAL_CNTRL_QSFP_LPMODE,
    ADAPTER_HWSIGNAL_CNTRL_OSFP_LPWn,
    ADAPTER_HWSIGNAL_CNTRL_OSFP_RSTn,
}ADAPTER_HWSIGNAL_CNTRL;

/// <summary>
/// Adapter external mode 
/// </summary>
typedef enum ADAPTER_EXTERNALMODE
{
    ADAPTER_EXTERNALMODE_DISABLED,
    ADAPTER_EXTERNALMODE_HW_ENABLED,
    ADAPTER_EXTERNALMODE_SW_ENABLED,
}ADAPTER_EXTERNALMODE;

/// <summary>
/// Transceiver Rx amplitude 
/// </summary>
typedef enum TXVR_RX_AMPLITUDE
{
    TXVR_RX_AMPLITUDE_100_400 = 0,
    TXVR_RX_AMPLITUDE_300_600 = 1,
    TXVR_RX_AMPLITUDE_400_800 = 2,
    TXVR_RX_AMPLITUDE_600_1200 = 3,
    TXVR_RX_AMPLITUDE_RESERVED = 4,
    TXVR_RX_AMPLITUDE_CUSTOM = 15,
}TXVR_RX_AMPLITUDE;

/// <summary>
/// Transceiver MSA page 
/// </summary>
typedef enum TXVR_MSA_PAGE
{
    TXVR_MSA_PAGE_LOWERMEMORY = 0,
    TXVR_MSA_PAGE_0 = 1,
    TXVR_MSA_PAGE_1 = 2,
    TXVR_MSA_PAGE_2 = 3,
    TXVR_MSA_PAGE_3 = 4,
    TXVR_MSA_PAGE_16 = 5,
    TXVR_MSA_PAGE_17 = 6,
}TXVR_MSA_PAGE;

/// <summary>
/// Monitor Clock Divider Values 
/// </summary>
typedef enum BERTMGR_MONITORDIVIDER
{
	BERTMGR_MONITOR_DIV1 = 1 << 0,
	BERTMGR_MONITOR_DIV4 = 1 << 2,
	BERTMGR_MONITOR_DIV8 = 1 << 3,
	BERTMGR_MONITOR_DIV16 = 1 << 4,
	BERTMGR_MONITOR_DIV32 = 1 << 5,
	BERTMGR_MONITOR_DIV64 = 1 << 6,
	BERTMGR_MONITOR_DIV128 = 1 << 7,
}BERTMGR_MONITORDIVIDER;

/// <summary>
/// CDR Divider Values 
/// </summary>
typedef enum BERTMGR_CDRDIVIDER
{
	BERTMGR_CDR_DIV32 = 1 << 5,
	BERTMGR_CDR_DIV64 = 1 << 6,
	BERTMGR_CDR_DIV128 = 1 << 7,
	BERTMGR_CDR_DIV256 = 1 << 8,
	BERTMGR_CDR_DIV512 = 1 << 9,
	BERTMGR_CDR_DIV1024 = 1 << 10,
	BERTMGR_CDR_DIV2048 = 1 << 11,
	BERTMGR_CDR_DIV4096 = 1 << 12,
}BERTMGR_CDRDIVIDER;

/// <summary>
/// Struct for pattern configuration
/// </summary>
struct PatternConfig
{
	BERTMGR_PATTERNTYPE pattern;
	bool invert;
	ulong userDefined[2];
	int repetition;
};

/// <summary>
/// Struct for Board FW information
/// </summary>
struct Board_Info
{
public:
	ushort boardID;
	ushort HWRev;
	ushort FWRev;
	ushort SilabRev;
	uint ipAddress;
	uint Mask;
	uint Gateway;
	ulong MAC;
	byte SN[10];
	bool Bootloader_Flag;
    bool isAdapterMode;
    ADAPTER_TYPE adapterType;
};

/// <summary>
/// Struct for BER channels measurements
/// </summary>
struct BERData
{
	bool enabled;
	bool enabledChannels[MAXCHANNELS];      // Channels enabled indicator
	bool lockedChannels[MAXCHANNELS];       // Channels lock indicator
	double Time[MAXCHANNELS];               // Constructed time data
	ulong BitCount[MAXCHANNELS];            // Bit Count data MSB/LSB
	uint ErrorCount_MSB[MAXCHANNELS];
	uint ErrorCount_LSB[MAXCHANNELS];
	ulong ErrorCount[MAXCHANNELS];
	//  Constructed data
	ulong AccumulatedErrorCount_MSB[MAXCHANNELS];
	double BER_MSB_Interval[MAXCHANNELS];
	double BER_MSB_Realtime[MAXCHANNELS];
	ulong AccumulatedErrorCount_LSB[MAXCHANNELS];
	double BER_LSB_Interval[MAXCHANNELS];
	double BER_LSB_Realtime[MAXCHANNELS];
	ulong AccumulatedErrorCount[MAXCHANNELS];
	double BER_Interval[MAXCHANNELS];
	double BER_Realtime[MAXCHANNELS];
    ulong TotalBitCount[MAXCHANNELS];            // Total Bit Count data MSB+LSB

};

/// <summary>
/// Struct for SER measurements
/// </summary>
struct SERData
{
	int nSymbols;
	uint InstantSER[SERMAXNUMSYMBOLS];
	ulong AccumulatedSER[SERMAXNUMSYMBOLS];

};

/// <summary>
/// Struct for real FEC link measurements
/// </summary>
struct RealFECData
{
	bool enabled;
	bool enabledLinks[FECMAXNUMLINKS];      // Links enabled indicator
	bool lockedLinks[FECMAXNUMLINKS];       // Links lock indicator
	double Time[FECMAXNUMLINKS];            // Constructed time data
	ulong BitCount[FECMAXNUMLINKS];         // Bit Count data LSB/MSB
	uint FEC_Skew[FECMAXNUMLINKS];
	uint FEC_Corrected_Ones_Interval[FECMAXNUMLINKS];
	uint FEC_Corrected_Zeros_Interval[FECMAXNUMLINKS];
	ulong FEC_ErrorCount_Interval[FECMAXNUMLINKS];
	uint FEC_Symbol_ErrorCount_Interval[FECMAXNUMLINKS];
	uint FEC_CorrectedBitCount_Interval[FECMAXNUMLINKS];
	double FEC_Symbol_ErrorRate_Interval[FECMAXNUMLINKS];
	double FEC_CorrectedBitRate_Interval[FECMAXNUMLINKS];
	double FEC_Frame_ErrorRate_Interval[FECMAXNUMLINKS];
	uint FEC_CW_UnCorrectedCount_Interval[FECMAXNUMLINKS];
	uint FEC_CW_CorrectedCount_Interval[FECMAXNUMLINKS];
	uint FEC_CW_ProcessedCount_Interval[FECMAXNUMLINKS];
	double FEC_CW_UncorrectedErrorRate_Interval[FECMAXNUMLINKS];
	ulong AccumulatedFEC_Corrected_Ones[FECMAXNUMLINKS];
	ulong AccumulatedFEC_Corrected_Zeros[FECMAXNUMLINKS];
	ulong AccumulatedFEC_ErrorCount[FECMAXNUMLINKS];
	ulong AccumulatedFEC_Symbol_ErrorCount[FECMAXNUMLINKS];
	ulong AccumulatedFEC_CorrectedBitCount[FECMAXNUMLINKS];
	double AveragedFEC_Symbol_ErrorRate[FECMAXNUMLINKS];
	double AveragedFEC_CorrectedBitRate[FECMAXNUMLINKS];
	double AveragedFEC_Frame_ErrorRate[FECMAXNUMLINKS];
	ulong AccumulatedFEC_CW_UnCorrectedCount[FECMAXNUMLINKS];
	ulong AccumulatedFEC_CW_CorrectedCount[FECMAXNUMLINKS];
	ulong AccumulatedFEC_CW_ProcessedCount[FECMAXNUMLINKS];
	double AccumulatedFEC_CW_UncorrectedErrorRate[FECMAXNUMLINKS];
	SERData SER[FECMAXNUMLINKS];
    ulong TotalBitCount[MAXCHANNELS];            // Total Bit Count data MSB + LSB
};

/// <summary>
/// Parsed emulator FEC link data
/// </summary>
struct EmulatorFECData
{
	bool enabled;
    bool enabledLinks[FECMAXNUMLINKS];  // Enabled link channel indicator
	bool lockedLinks[FECMAXNUMLINKS];   // Links lock indicator
	uint FEC_CorrectedBitError[FECMAXNUMLINKS];
	uint FEC_BlockCount[FECMAXNUMLINKS];
	uint FEC_SaturatedSymbolError[FECMAXNUMLINKS];
	ulong AccumulatedFEC_CorrectedBitError[FECMAXNUMLINKS];
	ulong AccumulatedFEC_BlockCount[FECMAXNUMLINKS];
	ulong AccumulatedFEC_SaturatedSymbolError[FECMAXNUMLINKS];
	SERData SER[FECMAXNUMLINKS];
};

/// <summary>
/// Struct for ML4054B FEC link measurements
/// </summary>
struct RealFECData_4044
{
    bool enabled;
    bool enabledLinks[FECMAXNUMLINKS];        // Links enabled indicator
    bool lockedLinks[FECMAXNUMLINKS];         // Links lock indicator
    double Time[FECMAXNUMLINKS];              // Constructed time data
    ulong BitCount[FECMAXNUMLINKS];           // Bit Count data
    uint FEC_CorrectedBitCount_Interval[FECMAXNUMLINKS];
    uint FEC_CW_UnCorrectedCount_Interval[FECMAXNUMLINKS];
    uint FEC_CW_CorrectedCount_Interval[FECMAXNUMLINKS];
    uint FEC_CW_ProcessedCount_Interval[FECMAXNUMLINKS];
    double FEC_CW_UncorrectedErrorRate_Interval[FECMAXNUMLINKS];
    ulong AccumulatedFEC_CW_UnCorrectedCount[FECMAXNUMLINKS];
    ulong AccumulatedFEC_CW_CorrectedCount[FECMAXNUMLINKS];
    ulong AccumulatedFEC_CW_ProcessedCount[FECMAXNUMLINKS];
    double AccumulatedFEC_CW_UncorrectedErrorRate[FECMAXNUMLINKS];
    SERData SER[FECMAXNUMLINKS];
    ulong TotalBitCount[FECMAXNUMLINKS];            // Total Bit Count data
};

/// <summary>
/// Struct for measurements data
/// </summary>
struct MeasurementsData
{
	BERData berData;                    // BER Channels Measurements
	RealFECData realFecData;            // Real FEC Links Measurements
	EmulatorFECData emulatorFecData;    // Emulator FEC Links Measurements
    RealFECData_4044 realFecData_4044;            // Real FEC Links Measurements for ML4054B
};

/// <summary>
/// Tx Taps mode 
/// </summary>
typedef enum BERTMGR_TAPSMODE
{
	BERTMGR_3TAPS = 0,
	BERTMGR_7TAPS = 1,
}BERTMGR_TAPSMODE;

/// <summary>
/// All available DSP modes.
/// Please check unit's docs to get list of supported modes.
/// </summary>
typedef enum BERTMGR_DSPMODE
{
	BERTMGR_DSP_MODE_SLC1 = 0,                  // PAM4 Slicer
	BERTMGR_DSP_MODE_SLC1_LDEQ = 1,             // PAM4 Slicer + Level-dependent equalizer (LDEQ)
	BERTMGR_DSP_MODE_SLC1_RC_SLC2 = 2,          // PAM4 Slicer + Reflection canceller (RC)
	BERTMGR_DSP_MODE_SLC1_RC_LDEQ = 3,          // PAM4 Slicer + LDEQ + RC
	BERTMGR_DSP_MODE_DFE1 = 4,                  // Decision Feedback Equalizer (DFE)
	BERTMGR_DSP_MODE_DFE1_RC_DFE2 = 7,          // DFE + RC
	BERTMGR_DSP_MODE_SLC1_MPICAN_SLC2 = 8,      // PAM4 Slicer + Multipath interference canceller (MPICAN)
	BERTMGR_DSP_MODE_SLC1_MPICAN_LDEQ = 9,      // PAM4 Slicer + LDEQ + MPICAN
	BERTMGR_DSP_MODE_SLC1_RC_MPICAN_SLC2 = 10,  // PAM4 Slicer + RC + MPICAN
	BERTMGR_DSP_MODE_SLC1_RC_MPICAN_LDEQ = 11,  // PAM4 Slicer + LDEQ + RC + MPICAN
	BERTMGR_DSP_MODE_DFE1_MPICAN_DFE2 = 13,     // DFE + MPICAN
	BERTMGR_DSP_MODE_DFE1_RC_MPICAN_DFE2 = 15,  // DFE + RC + MPICAN
}BERTMGR_DSPMODE;

/// <summary>
/// Struct for advanced amplitude configuration
/// </summary>
struct AdvancedAmplitude
{
	int mainTap;
	int postEmphasis;
	int preEmphasis;
	int innerLevel;
	int outerLevel;
	int scalingLevel;
	int advancedTaps[7];
};

/// <summary>
/// Struct for pattern definition
/// </summary>
struct FixedPatternDefinition
{
public:
    ulong Pattern;
    byte Repetition;
};

/// <summary>
/// Struct for user defined pattern definition 
/// </summary>
struct UserDefinedPatternDefinition
{
public:
    FixedPatternDefinition Pattern1;
    FixedPatternDefinition Pattern2;
};

/// <summary>
/// Struct for Noise Settings
/// </summary>
struct NoiseSettings
{
	double NoiseLinerate;
	bool NoiseStatus;
	bool NoiseChannelEnabled[MAXCHANNELS];
	int NoiseLevel[MAXCHANNELS];
	BERTMGR_PATTERNTYPE txPatternNoise[MAXCHANNELS];
	BERTMGR_SIGMODULATION NoiseeyeMode;
    UserDefinedPatternDefinition NoiseUserDefinedPattern[MAXCHANNELS];
};

/// <summary>
/// Struct for optimal amplitude range
/// </summary>
struct AmpRange
{
	int min;                            // Minimum optimal amplitude value
	int max;                            // Maximum optimal amplitude value
	BERTMGR_CALIBRATIONMODE calMode;    // Calibration mode    
};



/// <summary>
/// AFE Trim options values.
/// </summary>
typedef enum BERTMGR_AFETRIM_OPT
{
	BERTMGR_AFETRIM_NEG4DB = 0,
	BERTMGR_AFETRIM_NEG10DB = 1,
}BERTMGR_AFETRIM_OPT;

/// <summary>
/// All BERT configuration settings
/// </summary>
struct ConfigurationSettings
{
public:
	//  Parametes linerate configuration
	double linerate;
	BERTMGR_SIGMODULATION eyeMode;
	bool grayMaping;
	bool preCoding;
	bool chipMode;
	BERTMGR_CLOCKSOURCE clockSource;
	BERTMGR_CLOCKMODE clockType;
	int divider;
	bool FEC;
	BERTMGR_FECMODE FECMode;
    BERTMGR_FECPATTERN FECPattern;
	BERTMGR_TAPSMODE Tapsmode;
	bool IEEEMode;
	bool allTaps[7];

	//  Parameters for PRBS pattern configuration
	BERTMGR_PATTERNTYPE txPattern[MAXCHANNELS];
	BERTMGR_PATTERNTYPE rxPattern[MAXCHANNELS];
	bool txInvert[MAXCHANNELS];
	bool rxInvert[MAXCHANNELS];
	bool txEnable[MAXCHANNELS];
	bool rxEnable[MAXCHANNELS];

	//  Parameters for channel's TX amplitude
	int amplitude[MAXCHANNELS];
	AdvancedAmplitude advancedAmplitude[MAXCHANNELS];
	AmpRange amplitudeRange[MAXCHANNELS];

	// Parameters for error insertion
	BERTMGR_ERRORINSERTIONMODES Errormodes[MAXCHANNELS];
	byte duration[MAXCHANNELS];
	byte gap[MAXCHANNELS];
	bool errorState[MAXCHANNELS];

	//  Parameters for DFE mode
	BERTMGR_DSPMODE DSPmode[MAXCHANNELS];

	//  Calibration validation status
	bool calIsValid;

	//  Noise settings
	NoiseSettings noiseSettings;

	//  Shallow loopback
	bool ShallowLoopback;

    //  Enabled FEC links
	ushort FECLinks;

    //  User Defined patterns definitions
	UserDefinedPatternDefinition UserDefinedPattern[MAXCHANNELS];

    //  AFE Trim option
	BERTMGR_AFETRIM_OPT   AFE_Trim;

	bool FECAvailability;
    int MonitorDivider;
    int CDRDivider;
    int CDRSource;
    int CTLE[MAXCHANNELS];

    bool PMenable;
    bool PMRJenable;
    ushort PMamplitude;
    ulong PMfrequency;
    ushort PMRJamplitude;
    ushort PhaseShift;
    ushort PMPRBSamplitude;
    ushort PMdataswing;
    ushort PMpattern;

    bool FMenable;
    bool FMRJenable;
    ushort FMamplitude;
    ulong FMfrequency;
    ushort FMRJamplitude;
    ushort FMShift;


};

/// <summary>
/// Configure mlbertmgr object parameters
/// </summary>
struct InstanceParams
{
public:
	char saveConfig[MAX_ADDR_LEN];
	char saveBathtub[MAX_ADDR_LEN];
	char saveEye[MAX_ADDR_LEN];
	int saveBathtubEnable;
	int saveEyeEnable;
};

/// <summary>
/// Histogram Data
/// </summary>
struct HistogramData
{
	uint values[256];
};

/// <summary>
/// Transceiver configuration settings
/// </summary>
struct TXVR_ConfigurationSettings{
public:
    bool DataPathDeInit[MAXCHANNELS];
    bool TXOuputDisable[MAXCHANNELS];
    bool TXPolarityFlip[MAXCHANNELS];
    bool TXSquelchDisable[MAXCHANNELS];
    bool TXForceSquelch[MAXCHANNELS];
    byte TXEqualization[MAXCHANNELS];
    bool RXOutputDisable[MAXCHANNELS];
    bool RXPolarityFlip[MAXCHANNELS];
    bool RXSquelchDisable[MAXCHANNELS];
    TXVR_RX_AMPLITUDE RXOutputAmplitude[MAXCHANNELS];
    byte RXOutputPreCursor[MAXCHANNELS];
    byte RXOutputPostCursor[MAXCHANNELS];
};

/// <summary>
/// Get a runtime version of the library.
/// </summary>
/// <returns>Pointer to statically allocated struct API version</returns>
BERTMGRAPICALL const  struct mlbertmgr_api_version* mlbertmgr_APIVersion(void);

/// <summary>
/// Creates an instance of the library
/// </summary>
/// <returns>Pointer to the mlbertmgr instance</returns>
BERTMGRAPICALL mlbertmgr* BERTMGRSTACKMODE mlbertmgr_createInstance();

/// <summary>
/// Destroys library instance.
/// </summary>
/// <param name="instance">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL void BERTMGRSTACKMODE mlbertmgr_destroyInstance(mlbertmgr* inst);

/// <summary>
/// Opens connection.
/// </summary>
/// <param name="instance">Pointer to instance.</param>
/// <param name="address">Address to connect to (IP, PXI resource name,...).</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_openConnection(mlbertmgr * inst, char * address);

/// <summary>
/// Initialize instance.
/// </summary>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_initializeInstance(mlbertmgr * inst, InstanceParams t_params);

/// <summary>
/// Closes connection to instance.
/// </summary>
/// <param name="instance">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_closeConnection(mlbertmgr * inst);

/// <summary>
/// Initializes the boards default settings.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getActiveConfig(mlbertmgr * inst, ConfigurationSettings* initConfig);

/// <summary>
/// Applies the configuration parameters.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_applyConfiguration(mlbertmgr * inst);

/// <summary>
/// Sets the linerate.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="linerate"> The linerate.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default is false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setLinerate(mlbertmgr * inst, double * linerate, bool applyConfig);

/// <summary>
/// Sets the tx pattern.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="txPattern">The tx pattern.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setTxPattern(mlbertmgr * inst, int channel, PatternConfig txPattern, bool applyConfig = false);

/// <summary>
/// Sets the rx pattern.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="rxPattern">The rx pattern.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setRxPattern(mlbertmgr * inst, int channel, PatternConfig rxPattern, bool applyConfig = false);

/// <summary>
/// Sets the eye mode.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="eyeMode">The eye mode.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default is false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setEyeMode(mlbertmgr * inst, BERTMGR_SIGMODULATION eyeMode, bool applyConfig);

/// <summary>
/// Sets Clock Source.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="clockSource">clock source: 1 internal, 0 external..</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default is false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setClockSource(mlbertmgr * inst, BERTMGR_CLOCKSOURCE clockSource, bool applyConfig);

/// <summary>
/// Commits the configuration settings.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_commitConfig(mlbertmgr * inst);

/// <summary>
/// Sets the clock mode.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="clockMode">The clock mode.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setClockMode(mlbertmgr * inst, BERTMGR_CLOCKMODE clockMode, bool applyConfig);

/// <summary>
/// Sets the divider.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="divider">The divider.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setMonitorDivider(mlbertmgr * inst, BERTMGR_MONITORDIVIDER divider, bool applyConfig);

/// <summary>
/// Gets the clock out rate.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="clockOutRate">The clock out rate.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getClockOut(mlbertmgr * inst, double * clockOutRate); // ToDo

/// <summary>
/// Sets Amplitude for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="mainTap">Amplitude in mV.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setAmplitude(mlbertmgr * inst, int channel, int amplitude, bool applyConfig);

/// <summary>
/// Gets FW info
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="info">Board info.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getInfo(mlbertmgr * inst, Board_Info* info);

/// <summary>
/// Sets Main Tap for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="mainTap">Main tap value.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setMainTap(mlbertmgr * inst, int channel, int mainTap, bool applyConfig);

/// <summary>
/// Sets post emphasis for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="postEmphasis">Post emphasis value.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setPostEmphasis(mlbertmgr * inst, int channel, int postEmphasis, bool applyConfig);

/// <summary>
/// Sets pre emphasis for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="preEmphasis">Pre emphasis value.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setPreEmphasis(mlbertmgr * inst, int channel, int preEmphasis, bool applyConfig);

/// <summary>
/// Sets inner eye level for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="innerLevel">Inner eye level value.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setInnerEyeLevel(mlbertmgr * inst, int channel, int innerLevel, bool applyConfig);

/// <summary>
/// Sets outer eye level for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="outerLevel">Outter eye level value.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setOuterEyeLevel(mlbertmgr * inst, int channel, int outerLevel, bool applyConfig);

/// <summary>
/// Sets scaling level for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="scalingLevel">Scaling level value.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setScalingLevel(mlbertmgr * inst, int channel, int scalingLevel, bool applyConfig);

/// <summary>
/// Sets advanced amplitude values for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="advAmplitude">Advanced amplitude values.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <param name="output">Output reference variable to contain calculated approximate amplitude.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setAdvancedAmplitude(mlbertmgr * inst, int channel, AdvancedAmplitude advAmplitude, int *output, bool applyConfig);

/// <summary>
/// Enables/Disables Gray Coding
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="enable">Gray Coding enabling status.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setGrayCoding(mlbertmgr * inst, bool enable, bool applyConfig);


/// <summary>
/// Set FEC mode.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="mode">FEC mode.</param>
/// <param name="pattern">FEC pattern (ML4054B only).</param>
/// <param name="applyConfig">Configuration pipeline execution.</param>
/// <returns>Operation success.</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setFECMode(mlbertmgr * inst, BERTMGR_FECMODE mode, BERTMGR_FECPATTERN pattern, bool applyConfig);

/// <summary>
/// Reads Gray Coding status
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="isEnabled">Returned Gray Coding status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getGrayCoding(mlbertmgr * inst, bool* isEnabled);

/// <summary>
/// Set enabled monitoring flags.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="enabledFlagsValue">
/// Monitoring flags setter. Refer to `MONITOR_FLAGS` enum for bits order.
/// </param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_enableMonitor(mlbertmgr * inst, int enabledFlagsValue);

/// <summary>
/// Set individual monitoring flag status.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="flag">Monitoring flag.</param>
/// <param name="isEnabled">Enable status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_enableMonitorFlag(mlbertmgr * inst, BERTMGR_MONITOR_FLAGS flag, bool isEnabled);

/// <summary>
/// Read individual monitoring type values.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="flag">Monitoring flag.</param>
/// <param name="value">Output array for flag value for all channels.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_singleReadMonitor(mlbertmgr * inst, BERTMGR_MONITOR_FLAGS flag, ushort value[]);

/// <summary>
/// Read multiple monitoring types values.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="enabledFlagsValue">
/// Monitoring flags setter. Refer to `MONITOR_FLAGS` enum for bits order.
/// </param>
/// <param name="value">
/// Output array for flag values for all channels.
/// Serialised by grouping values for each enabled flag for all channels sequentially.
/// (Compatible with C#'s 2-dimensional array [,]).
/// </param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_multiReadMonitor(mlbertmgr * inst, int enabledFlagsValue, ushort values[]);

/// <summary>
/// Get LoS monitoring flag status.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="value">Output value for LoS.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_readLOS(mlbertmgr * inst, ushort &value);

/// <summary>
/// Start BER capture loop. Blocking Mode
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channels">
/// 16-bit flags for each channel. To enable a channel set its corresponding bit to 1.
/// 0 otherwise.
/// </param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_startBERCaptureLoop(mlbertmgr * inst, ushort channels, bool accumulate=true);

/// <summary>
/// Start BER capture in non-blocking mode. Background thread
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channels">
/// 16-bit flags for each channel. To enable a channel set its corresponding bit to 1.
/// 0 otherwise.
/// </param>
/// <returns>Operation status</returns>
BERTMGRAPICALL void BERTMGRSTACKMODE mlbertmgr_startBER(mlbertmgr * inst, ushort channels, bool accumulate);

/// <summary>
/// Get available BER data.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="data">Output array of data (maximum size BERMAXITEMSPOP).</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getAvailableBERData(mlbertmgr * inst, MeasurementsData data[BERMAXITEMSPOP], int &datacount);



/// <summary>
/// Stops the BER acquisition.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_stopBER(mlbertmgr * inst);

/// <summary>
/// Enables/Disables the RX line.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="status">The status of the RX line.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_RxEnable(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Reads RX status.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="isEnabled">The status of the RX line.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getRxStatus(mlbertmgr * inst, int channel, bool * isEnabled);

/// <summary>
/// Enables/Disables the TX line.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="status">The status of the TX line.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_TxEnable(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Reads TX status.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="isEnabled">The status of the TX line.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getTxStatus(mlbertmgr * inst, int channel, bool * isEnabled);

/// <summary>
/// Sets error rate.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="rate">The rate.</param>
/// <param name="actualrate">Output calculated actual rate (on success only)</param>
/// <param name="applyConfig"></param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setErrorRate(mlbertmgr * inst, int channel, double rate, double* actualrate, bool applyConfig);

/// <summary>
/// Sets error insertion.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="error">Error insertion parameters</param>
/// <param name="applyConfig"></param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setErrorPattern(mlbertmgr * inst, int channel, ErrorStruct error, bool applyConfig);

/// <summary>
/// Stops error insertion.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_stopErrorInsertion(mlbertmgr * inst, int channel, bool applyConfig);

/// <summary>
/// Calculates TX Emulation Taps from Loss at Nyquist.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="Taps">Output taps array</param>
/// <param name="lossDb">Loss value at Nyquist</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getTxEmulationTapsFromLossAtNyquist(mlbertmgr * inst, int* taps, double lossDb);

/// <summary>
/// Calculates TX Emulation Taps from Loss at Nyquist.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="Taps">Output taps array</param>
/// <param name="lossDb">Loss value at Nyquist</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getTxEmulationTapsFromSParams(mlbertmgr * inst, int* taps, char s2pFilePath[255]);

/// <summary>
/// Save Calibration Values. FOR USE ONLY BY MULTILANE
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="mode">mode</param>
/// <param name="Ndata">Data length</param>
/// <param name="Data">Values</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_saveCalibrationValues(mlbertmgr * inst, int channel, int mode, double* Data, int lenData, bool applyConfig);

/// <summary>
/// Save Optimal Settings. FOR USE ONLY BY MULTILANE
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="mode">mode</param>
/// <param name="Ndata">Data length</param>
/// <param name="Data">Values</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_saveOptimalSettings(mlbertmgr * inst, int channel, int mode, int * Data, int lenData, bool applyConfig);

/// <summary>
/// Load Calibration Values.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="mode">mode</param>
/// <param name="Ndata">Data length</param>
/// <param name="Data">Values</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_loadCalibrationValues(mlbertmgr * inst, int channel, int mode, double * data, int* lenData, bool applyConfig);

/// <summary>
/// Load Optimal Settings.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">The channel.</param>
/// <param name="mode">mode</param>
/// <param name="Ndata">Data length</param>
/// <param name="Data">Values</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_loadOptimalSettings(mlbertmgr * inst, int channel, int mode, int * data, int* lenData, bool applyConfig);

/// <summary>
/// Set taps mode.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="mode">mode</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setTapsMode(mlbertmgr * inst, BERTMGR_TAPSMODE mode, bool applyConfig);

/// <summary>
/// Save Checksum Calibration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="address">Address enum to write to.</param>
/// <param name="data">Data to write.</param>
/// <param name="length">Data length (number of words) to write.</params>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_writeAddress(mlbertmgr * inst, int address, ushort data[], int length);

/// <summary>
/// Set channel's equalizer block mode.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel's index.</param>
/// <param name="DSPmode">Equalizer block mode.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setDSPMode(mlbertmgr * inst, int channel, BERTMGR_DSPMODE DSPmode, bool applyConfig);

/// <summary>
/// Get histogram data for enabled channels.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="enabledChannels">Enabled channel flags (1 bit/channel)</param>
/// <param name="output">Output array of Histogram data per channel</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_getHistogramData(mlbertmgr * inst, ushort enabledChannels, HistogramData output[]);

/* Advanced Histogram Control */

/// <summary>
/// Request a histogram samples capture for enabled channels.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="enabledChannels">Enabled channel flags (1 bit/channel).</param>
/// <param name="actualEnabled">Actually enabled channel flags (1 bit/channel) output.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_captureHistogramData(mlbertmgr * inst, ushort enabledChannels, ushort* actualEnabled);

/// <summary>
/// Read channel Histogram data. Typically called after a capture request.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel index.</param>
/// <param name="output">Output channel's Histogram data.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_readHistogramData(mlbertmgr * inst, int channel, HistogramData* output);

/// <summary>
/// Initializes the boards default settings.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setActiveConfig(mlbertmgr * inst, ConfigurationSettings initConfig, bool forceUpdate);

/// <summary>
/// Read FW options
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="options">Output array of 39 items</param>
/// <param name="forceUpdate">Force loading options from hardware (as opposed to cached values)</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_readFWOptions(mlbertmgr * inst, ulong* options, bool forceUpdate);

/// <summary>
/// Set noise linerate
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="linerate"> The linerate.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default is false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setNoiseLinerate(mlbertmgr * inst, double * linerate, bool applyConfig);

/// <summary>
/// Enable or disable noise
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_enableNoise(mlbertmgr * inst, int channel, bool enable, bool applyConfig);

/// <summary>
/// Set noise level
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setNoiseLevel(mlbertmgr * inst, int channel, int NoiseLevel, bool applyConfig);

/// <summary>
/// Set TX pattern for noise
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setNoiseTxPattern(mlbertmgr * inst, int channel, PatternConfig txPattern, bool applyConfig);

/// <summary>
/// Set noise eye mode
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setNoiseEyeMode(mlbertmgr * inst, BERTMGR_SIGMODULATION eyeMode, bool applyConfig);

/// <summary>
/// Set Shallow Loopback
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setShallowLoopback(mlbertmgr * inst, bool enable, bool applyConfig);

/// <summary>
/// Set noise status
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setNoiseStatus(mlbertmgr * inst, bool enable, bool applyConfig);

/// <summary>
/// Set noise burst Rate
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Index</param>
/// <param name="burstRate">Burst Rate</param>
/// <param name="actualrate">Output calculated actual rate (on success only)</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setNoiseBurstRate(mlbertmgr * inst, int channel, double burstRate, double* actualrate, bool applyConfig);

/// <summary>
/// Configure FEC links channels
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channels">
/// 16-bit flags for each channel. To enable a channel set its corresponding bit to 1.
/// 0 otherwise.
/// </param>
/// <param name="skipReset">If true skips reset, applies it otherwise.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default is false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_configureFECLinks(mlbertmgr * inst, ushort channels, bool skipReset, bool applyConfig);

/// <summary>
/// Set User-Defined Pattern
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channels">Channel Index</param>
/// <param name="userDefinedPattern">Object holding the pre-defined pattern</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default is false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setUserDefinedPattern(mlbertmgr * inst, int channel, UserDefinedPatternDefinition userDefinedPattern, bool applyConfig);
/**/

/// <summary>
/// Set AFE Trim option.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="value">AFE Trim option value.</param>
/// <param name="applyConfig"></param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setAFETrim(mlbertmgr * inst, BERTMGR_AFETRIM_OPT value, bool applyConfig);

/// <summary>
/// Set CDR divider.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="value">divider value.</param>
/// <param name="applyConfig"></param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setCDRDivider(mlbertmgr * inst, BERTMGR_CDRDIVIDER divider, bool applyConfig);

/// <summary>
/// Set CDR source.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="option">Rx channel source. This option is availabel on the 1st channel only.</param>
/// <param name="applyConfig"></param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setCDRChannelSource(mlbertmgr * inst, int option, bool applyConfig);
// <summary>
/// Sets CTLE for selected channel
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Selected channel.</param>
/// <param name="preEmphasis">CTLE value.</param>
/// <param name="applyConfig">If true calls 'ApplyConfiguration', by default it's false.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setCTLE(mlbertmgr * inst, int channel, int CTLE, bool applyConfig);


/// <summary>
/// Set TX Optimization.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="key">taps values.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_SetTXOptimization(mlbertmgr * inst, short * taps);

/// <summary>
/// Read Adapter Type./// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="type">Adapter type returned value.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_detectAdapter(mlbertmgr * inst, ADAPTER_TYPE * type);

/// <summary>
/// Sets adapter control pin.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="cntrl">Pin Selection.</param>
/// <param name="Status">Pin status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setControlPin(mlbertmgr * inst, ADAPTER_HWSIGNAL_CNTRL cntrl, bool Status);

/// <summary>
/// Sets Adapter in external mode.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="isEnabled">External mode enabler.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mlbertmgr_setExternalAdapterMode(mlbertmgr * inst, bool isEnabled);

/// <summary>
/// Transceiver I2C/MDIO Sequential Read.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="pageSelect">Page Selection.</param>
/// <param name="registerAddress">Address to start reading from.</param>
/// <param name="dataLength">Length of data to be read.</param>
/// <param name="dataBuffer">Returned data.</param>
/// <param name="bankSelect">Bank Selection (default = 0).</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_sequentialRead(mlbertmgr * inst, ushort pageSelect, ushort registerAddress, ushort dataLength, ushort* dataBuffer, ushort bankSelect = 0);

/// <summary>
/// Transceiver I2C/MDIO Sequential Write.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="pageSelect">Page Selection.</param>
/// <param name="registerAddress">Address to start writing to.</param>
/// <param name="dataLength">Length of data to be written.</param>
/// <param name="dataBuffer">Data to write.</param>
/// <param name="bankSelect">Bank Selection (default = 0).</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_sequentialWrite(mlbertmgr * inst, ushort pageSelect, ushort registerAddress, ushort dataLength, ushort* dataBuffer, ushort bankSelect = 0);

/// <summary>
/// Transceiver Tx Output Disable Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">Tx Disable status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setTxOutputDisable(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver DataPathDeInit Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">DataPathDeInit status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setTxDataPathDeInit(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver Tx Force Squelch Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">Tx Force Squelch status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setTxForceSquelch(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver Tx Squelch Disable Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">Tx Squelch Disable status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setTxSquelchDisable(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver Tx Polarity Flip Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">Tx Polarity Flip status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setTxPolarityFlip(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver Tx input equalization Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="value">Input Equalization value.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setTxInputEqualization(mlbertmgr * inst, int channel, int value);

/// <summary>
/// Reads Transceiver active Confguration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="activeConfig">Active Transceiver configuration.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_getActiveConfig(mlbertmgr * inst, TXVR_ConfigurationSettings* activeConfig);

/// <summary>
/// Transceiver Rx Polarity Flip Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">Rx Polarity Flip status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setRxPolarityFlip(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver Rx Squelch Disable Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">Rx Squelch Disable status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setRxSquelchDisable(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver Rx Output Disable Configuration.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="Status">Rx Disable status.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setRxOutputDisable(mlbertmgr * inst, int channel, bool status);

/// <summary>
/// Transceiver Rx Output Pre-Cursor.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="value">Rx Output Pre-Cursor value.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setRxPreCursor(mlbertmgr * inst, int channel, int value);

/// <summary>
/// Transceiver Rx Output Post-Cursor.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="value">Rx Output Post-Cursor value.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setRxPostCursor(mlbertmgr * inst, int channel, int value);

/// <summary>
/// Transceiver Rx Output Amplitude.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="channel">Channel Selection.</param>
/// <param name="value">Rx Output Amplitude range.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_setRxAmplitude(mlbertmgr * inst, int channel, TXVR_RX_AMPLITUDE value);

/// <summary>
/// Reads Transceiver MSA pages.
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <param name="pages">Pages to read.</param>
/// <param name="Vales">Returned values.</param>
/// <returns>Operation status</returns>
BERTMGRAPICALL BERTMGR_STATUS BERTMGRSTACKMODE mltxvr_getMSAValues(mlbertmgr * inst, TXVR_MSA_PAGE pages[], ushort values[], byte numberOfPages);

/// <summary>
/// Enable or disable PM
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_EnablePM(mlbertmgr * inst, bool enable, bool applyConfig);

/// <summary>
/// Set PM amplitude
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetPMamplitude(mlbertmgr * inst, ushort amplitude, bool applyConfig);

/// <summary>
/// Set PM frequency
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetPMfrequency(mlbertmgr * inst, ulong frequency, bool applyConfig);

/// <summary>
/// Enable PM RJ
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_EnablePMRJ(mlbertmgr * inst, int status, bool applyConfig);

/// <summary>
/// Set PM RJ amplitude
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetPMRJamplitude(mlbertmgr * inst, ushort amplitude, bool applyConfig);

/// <summary>
/// Set PM phase shift
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetPMPhaseShift(mlbertmgr * inst, ushort value, bool applyConfig);

/// <summary>
/// Set PM PRBS amplitude
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetPMPRBBSamplitude(mlbertmgr * inst, ushort amplitude, bool applyConfig);

/// <summary>
/// Set PM data swing
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetPMdataSwing(mlbertmgr * inst, ushort amplitude, bool applyConfig);

/// <summary>
/// Set PM data pattern
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetPMdataPattern(mlbertmgr * inst, ushort pattern, bool applyConfig);

/// <summary>
/// Enable FM
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_EnableFM(mlbertmgr * inst, int status, bool applyConfig);

/// <summary>
/// Set FM amplitude
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetFMamplitude(mlbertmgr * inst, ushort amplitude, bool applyConfig);

/// <summary>
/// Set FM Frequency
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetFMfrequency(mlbertmgr * inst, ulong frequency, bool applyConfig);

/// <summary>
/// Enable FM RJ
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_EnableFMRJ(mlbertmgr * inst, int status, bool applyConfig);

/// <summary>
/// Set FM RJ amplitude
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetFMRJamplitude(mlbertmgr * inst, ushort amplitude, bool applyConfig);

/// <summary>
/// Set FM Shift
/// </summary>
/// <param name="inst">Pointer to instance.</param>
/// <returns>Returns true on success, false on failure.</returns>
BERTMGRAPICALL bool BERTMGRSTACKMODE mlbertmgr_SetFMPhaseShift(mlbertmgr * inst, ushort value, bool applyConfig);

#endif // !ML_BERT_MANAGER_H__
