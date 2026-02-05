cdef extern from "asio.cpp":
    ctypedef bint bool
    ctypedef long LONG
    ctypedef void VOID
    ctypedef void* LPVOID
    ctypedef unsigned short WORD
    ctypedef unsigned long DWORD
    ctypedef unsigned char BYTE
    ctypedef struct GUID:
        DWORD Data1
        WORD Data2
        WORD Data3
        BYTE Data[8]
    ctypedef GUID CLSID

    ctypedef double ASIOSampleRate
    ctypedef long long ASIOSamples
    ctypedef long long int ASIOTimeStamp

    ctypedef long ASIOBool
    ctypedef enum:
        ASIOFalse = 0
        ASIOTrue = 1

    ctypedef long ASIOError
    ctypedef enum:
        ASE_OK = 0
        ASE_SUCCESS = 0x3f4847a0
        ASE_NotPresent = -1000
        ASE_HWMalfunction
        ASE_InvalidParameter
        ASE_InvalidMode
        ASE_SPNotAdvancing
        ASE_NoClock
        ASE_NoMemory

    ctypedef long ASIOSampleType
    ctypedef enum:
        ASIOSTInt16MSB = 0
        ASIOSTInt24MSB = 1
        ASIOSTInt32MSB = 2
        ASIOSTFloat32MSB = 3
        ASIOSTFloat64MSB = 4

        ASIOSTInt32MSB16 = 8
        ASIOSTInt32MSB18 = 9
        ASIOSTInt32MSB20 = 10
        ASIOSTInt32MSB24 = 11
	
        ASIOSTInt16LSB = 16
        ASIOSTInt24LSB = 17
        ASIOSTInt32LSB = 18
        ASIOSTFloat32LSB = 19
        ASIOSTFloat64LSB = 20

        ASIOSTInt32LSB16 = 24
        ASIOSTInt32LSB18 = 25
        ASIOSTInt32LSB20 = 26
        ASIOSTInt32LSB24 = 27

        ASIOSTDSDInt8LSB1 = 32
        ASIOSTDSDInt8MSB1 = 33
        ASIOSTDSDInt8NER8 = 40

        ASIOSTLastEntry

    ctypedef struct ASIOTimeCode:
        double speed
        ASIOSamples timeCodeSamples
        unsigned long flags
        char future[64]

    ctypedef enum ASIOTimeCodeFlags:
        kTcValid = 1
        kTcRunning = 1 << 1
        kTcReverse = 1 << 2
        kTcOnspeed = 1 << 3
        kTcStill = 1 << 4
        kTcSpeedValid = 1 << 8

    ctypedef struct AsioTimeInfo:
        double speed
        ASIOTimeStamp systemTime
        ASIOSamples samplePosition
        ASIOSampleRate sampleRate
        unsigned long flags
        char reserved[12]

    ctypedef enum AsioTimeInfoFlags:
        kSystemTimeValid = 1
        kSamplePositionValid = 1 << 1
        kSampleRateValid = 1 << 2
        kSpeedValid = 1 << 3
        kSampleRateChanged = 1 << 4
        kClockSourceChanged = 1 << 5

    ctypedef struct ASIOTime:
        long reserved[4]
        AsioTimeInfo timeInfo
        ASIOTimeCode timeCode

    ctypedef struct ASIOCallbacks:
        void (*bufferSwitch)(long doubleBufferIndex, ASIOBool directProcess)
        void (*sampleRateDidChange)(ASIOSampleRate sRate)
        long (*asioMessage)(long selector, long value, void* message, double* opt)
        ASIOTime* (*bufferSwitchTimeInfo)(ASIOTime* params, long doubleBufferIndex, ASIOBool directProcess)

    ctypedef struct ASIODriverInfo:
        long asioVersion
        long driverVersion
        char name[32]
        char errorMessage[124]
        void* sysRef

    ctypedef struct ASIOClockSource:
        long index
        long associatedChannel
        long associatedGroup
        ASIOBool isCurrentSource
        char name[32]

    ctypedef struct ASIOChannelInfo:
        long channel
        ASIOBool isInput
        ASIOBool isActive
        long channelGroup
        ASIOSampleType type
        char name[32]

    ctypedef struct ASIOBufferInfo:
        ASIOBool isInput
        long channelNum
        void* buffers[2]

    ctypedef struct ASIOInputMonitor:
        long input
        long output
        long gain
        ASIOBool state
        long pan

    ctypedef struct ASIOChannelControls:
        long channel
        ASIOBool isInput
        long gain
        long meter
        char future[32]

    ctypedef struct ASIOTransportParameters:
        long command
        ASIOSamples samplePosition
        long track
        long trackSwitches[16]
        char future[64]

    ctypedef enum:
        kTransStart
        kTransStop
        kTransLocate
        kTransPunchIn
        kTransPunchOut
        kTransArmOn
        kTransArmOff
        kTransMonitorOn
        kTransMonitorOff
        kTransArm
        kTransMonitor

    ctypedef long int ASIOIoFormatType
    ctypedef enum ASIOIoFormatType_e:
        kASIOFormatInvalid = -1,
        kASIOPCMFormat = 0,
        kASIODSDFormat = 1,

    ctypedef struct ASIOIoFormat_s:
        ASIOIoFormatType FormatType;
        char future[512]
    ctypedef ASIOIoFormat_s ASIOIoFormat;

    ctypedef struct ASIOInternalBufferInfo:
        long inputSamples
        long outputSamples