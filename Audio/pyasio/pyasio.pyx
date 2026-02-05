# cython : language = c++
from cython.parallel cimport prange, parallel
from cython.cimports.libc.stdlib cimport malloc, free
from cython.cimports.libc.string import strlen, memcpy
cimport openmp

cdef int num_threads
openmp.omp_set_dynamic(1)
with nogil, parallel():
    num_threads = openmp.omp_get_num_threads()

ctypedef ASIODriverInfo* pASIODriverInfo

cdef extern from "asio.cpp":
    cdef ASIOError ASIOInit(ASIODriverInfo* info)
    cdef ASIOError ASIOExit()
    cdef ASIOError ASIOStart()
    cdef ASIOError ASIOStop()
    cdef ASIOError ASIOGetChannels(long* numInputChannels, long* numOutputChannels)
    cdef ASIOError ASIOGetLatencies(long* inputLatency, long* outputLatency)
    cdef ASIOError ASIOGetBufferSize(long* minSize, long* maxSize, long* preferredSize, long* granularity)
    cdef ASIOError ASIOCanSampleRate(ASIOSampleRate sampleRate)
    cdef ASIOError ASIOGetSampleRate(ASIOSampleRate* currentRate)
    cdef ASIOError ASIOSetSampleRate(ASIOSampleRate sampleRate)
    cdef ASIOError ASIOGetClockSources(ASIOClockSource* clocks, long* numSources)
    cdef ASIOError ASIOSetClockSource(long reference)
    cdef ASIOError ASIOGetSamplePosition(ASIOSamples* sPos, ASIOTimeStamp* tStamp)
    cdef ASIOError ASIOGetChannelInfo(ASIOChannelInfo* info)
    cdef ASIOError ASIOCreateBuffers(ASIOBufferInfo* bufferInfos, long numChannels, long bufferSize, ASIOCallbacks* callbacks)
    cdef ASIOError ASIODisposeBuffers()
    cdef ASIOError ASIOControlPanel()
    cdef void* ASIOFuture(long selector, void* params)
    cdef ASIOError ASIOOutputReady()

def PyASIOInit(info):
    cdef size_t n = sizeof(info)
    cdef ASIODriverInfo* pInfo = <ASIODriverInfo*>malloc(n)
    cdef BYTE* lpInfo = <BYTE*>pInfo
    for i in range(0, n):
        lpInfo[i] = info[i]
    cdef ASIOError result = ASIOInit(pInfo)
    for i in range(0, n):
        info[i] = lpInfo[i]
    free(pInfo)
    return result

def PyASIOExit():
    return ASIOExit()

def PyASIOStart():
    return ASIOStart()

def PyASIOStop():
    return ASIOStop()

def PyASIOGetChannels(numInputChannels, numOutputChannels):
    cdef size_t n = sizeof(numInputChannels)
    cdef size_t n2 = sizeof(numInputChannels)
    cdef long* pNumInputChannels = <long*>malloc(n)
    cdef long* pNumOutputChannels = <long*>malloc(n2)
    cdef BYTE* lpNumInputChannels = <BYTE*>pNumInputChannels
    cdef BYTE* lpNumOutputChannels = <BYTE*>pNumOutputChannels
    for i in range(0, n):
        lpNumInputChannels[i] = numInputChannels[i]
    for i in range(0, n2):
        lpNumOutputChannels[i] = numOutputChannels[i]
    cdef ASIOError result = ASIOGetChannels(pNumInputChannels, pNumOutputChannels)
    for i in range(0, n):
        numInputChannels[i] = lpNumInputChannels[i]
    for i in range(0, n2):
        numOutputChannels[i] = lpNumOutputChannels[i]
    free(pNumInputChannels)
    free(pNumOutputChannels)
    return result

def PyASIOGetLatencies(inputLatency, outputLatency):
    cdef size_t n = sizeof(inputLatency)
    cdef size_t n2 = sizeof(outputLatency)
    cdef long* pInputLatency = <long*>malloc(n)
    cdef long* pOutputLatency = <long*>malloc(n2)
    cdef BYTE* lpInputLatency = <BYTE*>pInputLatency
    cdef BYTE* lpOutputLatency = <BYTE*>pOutputLatency
    for i in range(0, n):
        lpInputLatency[i] = inputLatency[i]
    for i in range(0, n2):
        lpOutputLatency[i] = outputLatency[i]
    cdef ASIOError result = ASIOGetLatencies(pInputLatency, pOutputLatency)
    for i in range(0, n):
        inputLatency[i] = lpInputLatency[i]
    for i in range(0, n2):
        outputLatency[i] = lpOutputLatency[i]
    free(pInputLatency)
    free(pOutputLatency)
    return result

def PyASIOGetBufferSize(minSize, maxSize, preferredSize, granularity):
    cdef size_t n = sizeof(minSize)
    cdef size_t n2 = sizeof(maxSize)
    cdef size_t n3 = sizeof(preferredSize)
    cdef size_t n4 = sizeof(granularity)
    cdef long* pMinSize = <long*>malloc(n)
    cdef long* pMaxSize = <long*>malloc(n2)
    cdef long* pPreferredSize = <long*>malloc(n3)
    cdef long* pGranularity = <long*>malloc(n4)
    cdef BYTE* lpMinSize = <BYTE*>pMinSize
    cdef BYTE* lpMaxSize = <BYTE*>pMaxSize
    cdef BYTE* lpPreferredSize = <BYTE*>pPreferredSize
    cdef BYTE* lpGranularity = <BYTE*>pGranularity
    for i in range(0, n):
        lpMinSize[i] = minSize[i]
    for i in range(0, n2):
        lpMaxSize[i] = maxSize[i]
    for i in range(0, n3):
        lpPreferredSize[i] = preferredSize[i]
    for i in range(0, n4):
        lpGranularity[i] = granularity[i]
    cdef ASIOError result = ASIOGetBufferSize(pMinSize, pMaxSize, pPreferredSize, pGranularity)
    for i in range(0, n):
        minSize[i] = lpMinSize[i]
    for i in range(0, n2):
        maxSize[i] = lpMaxSize[i]
    for i in range(0, n3):
        preferredSize[i] = lpPreferredSize[i]
    for i in range(0, n4):
        granularity[i] = lpGranularity[i]
    free(pMinSize)
    free(pMaxSize)
    free(pPreferredSize)
    free(pGranularity)
    return result

def PyASIOCanSampleRate(sampleRate):
    return ASIOCanSampleRate(sampleRate)

def PyASIOGetSampleRate(currentRate):
    cdef size_t n = sizeof(ASIOSampleRate)
    cdef ASIOSampleRate* pCurrentRate = <ASIOSampleRate*>malloc(n)
    cdef BYTE* lpCurrentRate = <BYTE*>pCurrentRate
    for i in range(0, n):
        lpCurrentRate[i] = currentRate[i]
    cdef ASIOError result = ASIOGetSampleRate(pCurrentRate)
    for i in range(0, n):
        currentRate[i] = lpCurrentRate[i]
    free(pCurrentRate)
    return result

def PyASIOSetSampleRate(sampleRate):
    return ASIOSetSampleRate(<ASIOSampleRate>sampleRate)

def PyASIOGetClockSources(clocks, numSources):
    cdef size_t n = sizeof(ASIOClockSource)
    cdef size_t n2 = sizeof(long)
    cdef ASIOClockSource* pClocks = <ASIOClockSource*>malloc(n)
    cdef long* pNumSources = <long*>malloc(n2)
    cdef BYTE* lpClocks = <BYTE*>pClocks
    cdef BYTE* lpNumSources = <BYTE*>pNumSources
    for i in range(0, n):
        lpClocks[i] = clocks[i]
    for i in range(0, n2):
        lpNumSources[i] = numSources[i]
    cdef ASIOError result = ASIOGetClockSources(pClocks, pNumSources)
    for i in range(0, n):
        clocks[i] = lpClocks[i]
    for i in range(0, n2):
        numSources[i] = lpNumSources[i]
    free(pClocks)
    free(pNumSources)
    return result

def PyASIOSetClockSource(reference):
    return ASIOSetClockSource(reference)

def PyASIOGetSamplePosition(sPos, tStamp):
    cdef size_t n = sizeof(ASIOSamples)
    cdef size_t n2 = sizeof(ASIOTimeStamp)
    cdef ASIOSamples* pSPos = <ASIOSamples*>malloc(n)
    cdef ASIOTimeStamp* pTStamp = <ASIOTimeStamp*>malloc(n2)
    cdef BYTE* lpSPos = <BYTE*>pSPos
    cdef BYTE* lpTStamp = <BYTE*>pTStamp
    for i in range(0, n):
        lpSPos[i] = sPos[i]
    for i in range(0, n2):
        lpTStamp[i] = tStamp[i]
    cdef ASIOError result = ASIOGetSamplePosition(pSPos, pTStamp)
    for i in range(0, n):
        sPos[i] = lpSPos[i]
    for i in range(0, n2):
        tStamp[i] = lpTStamp[i]
    free(pSPos)
    free(pTStamp)
    return result

def PyASIOGetChannelInfo(info):
    return ASIOGetChannelInfo(<ASIOChannelInfo*>info)

def PyASIOCreateBuffers(bufferInfos, numChannels, bufferSize, callbacks):
    return ASIOCreateBuffers(<ASIOBufferInfo*>bufferInfos, numChannels, bufferSize, <ASIOCallbacks*> callbacks)

def PyASIODisposeBuffers():
    return ASIODisposeBuffers()

def PyASIOControlPanel():
    return ASIOControlPanel()

def PyASIOFuture(selector, params):
    return <long>(ASIOFuture(selector, <void*>params))

def PyASIOOutputReady():
    return PyASIOOutputReady()

cdef extern from "asiodrivers.cpp":
    cdef cppclass AsioDrivers:
        AsioDrivers() except +
        bool getCurrentDriverName(char* name)
        long getDriverNames(char** names, long maxDrivers)
        bool loadDriver(char* name)
        void removeCurrentDriver()
        long getCurrentDriverIndex()
        unsigned long connID
        long curIndex

cdef class PyAsioDrivers:
    cdef AsioDrivers c_instance

    def getCurrentDriverName(self, name):
        cdef size_t n = len(name)
        cdef char* pName = <char*>malloc(n)
        cdef BYTE* lpName = <BYTE*>pName
        result = self.c_instance.getCurrentDriverName(pName)
        for i in range(0, n):
            name[i] = lpName[i]
        free(pName)
        return result

    def getDriverNames(self, names, maxDrivers):
        cdef size_t n = len(names)
        cdef char** pNames = <char**>malloc(n)
        cdef BYTE* lpNames = <BYTE*>pNames
        for i in range(0, n):
            lpNames[i] = names[i]
        result = self.c_instance.getDriverNames(pNames, maxDrivers)
        for i in range(0, n):
            names[i] = lpNames[i]
        free(pNames)
        return result

    def loadDriver(self, name):
        cdef size_t n = len(name)
        cdef char* pName = <char*>malloc(n)
        cdef BYTE* lpName = <BYTE*>pName
        for i in range(0, n):
            lpName[i] = name[i]
        result = self.c_instance.loadDriver(pName)
        for i in range(0, n):
            name[i] = lpName[i]
        free(pName)
        return result

    def removeCurrentDriver(self):
        return self.c_instance.removeCurrentDriver()

    def getCurrentDriverIndex(self):
        return self.c_instance.getCurrentDriverIndex()

cdef extern from "asiolist.cpp":
    ctypedef asiodrvstruct* lpasiodrvstruct

    cdef struct asiodrvstruct:
        int drvID
        CLSID clsid
        char dllPath[512]
        char drvName[128]
        LPVOID asiodrv
        lpasiodrvstruct next

    ctypedef asiodrvstruct ASIODRVSTRUCT
    ctypedef ASIODRVSTRUCT* LPASIODRVSTRUCT

    cdef cppclass AsioDriverList:
        AsioDriverList() except +
        LONG asioOpenDriver(int drvID, LPVOID* asiodrv)
        LONG asioCloseDriver(int drvID)
        LONG asioGetNumDev()
        LONG asioGetDriverName(int drvID, char* drvname, int drvnamesize)
        LONG asioGetDriverPath(int drvID, char* dllpath, int dllpathsize)
        LONG asioGetDriverCLSID(int drvID, CLSID* clsid)
        LPASIODRVSTRUCT lpdrvlist
        int numdrv

    ctypedef AsioDriverList* LPASIODRIVERLIST

cdef class PyAsioDriverList:
    cdef AsioDriverList c_instance

    def asioOpenDriver(self, drvID, asiodrv):
        cdef size_t n = len(asiodrv)
        cdef VOID** pAsiodrv = <VOID**>malloc(n)
        cdef BYTE* lpAsiodrv = <BYTE*>pAsiodrv
        result = self.c_instance.asioOpenDriver(drvID, pAsiodrv)
        for i in range(0, n):
            asiodrv[i] = lpAsiodrv[i]
        free(pAsiodrv)
        return result

    def asioCloseDriver(self, drvID):
        return self.c_instance.asioCloseDriver(drvID)

    def asioGetNumDev(self):
        return self.c_instance.asioGetNumDev()

    def asioGetDriverName(self, drvID, drvname, drvnamesize):
        cdef size_t n = drvnamesize
        cdef char* pDrvname = <char*>malloc(n)
        cdef BYTE* lpDrvname = <BYTE*>pDrvname
        result = self.c_instance.asioGetDriverName(drvID, pDrvname, drvnamesize)
        n = strlen(pDrvname)
        for i in range(0, n):
            drvname[i] = lpDrvname[i]
        drvname = None
        free(pDrvname)
        return result

    def asioGetDriverPath(self, drvID, dllpath, dllpathsize):
        return self.c_instance.asioGetDriverPath(drvID, dllpath, dllpathsize)

    def asioGetDriverCLSID(self, drvID, clsid):
        return self.c_instance.asioGetDriverCLSID(drvID, <CLSID*>clsid)