"""
Dummy for UnicornPy
Outputs a Sawtooth signal on all channels
"""


from src.Unicorn_Recorder.Dummies.UnicornInterface import Unicorn as superUnicorn
from src.Unicorn_Recorder.Dummies.UnicornInterface import DeviceInformation as superDeviceInformation
from src.Unicorn_Recorder.Dummies.UnicornInterface import DeviceException as superDeviceException
from src.Unicorn_Recorder.Dummies.UnicornInterface import BluetoothAdapterInfo as superBluetoothAdapterInfo
from src.Unicorn_Recorder.Dummies.UnicornInterface import AmplifierChannel as superAmplifierChannel
from src.Unicorn_Recorder.Dummies.UnicornInterface import AmplifierConfiguration as superAmplifierConfiguration



# Variables with simple values

AccelerometerChannelsCount = 3
AccelerometerConfigIndex = 8

BatteryConfigIndex = 14

CounterConfigIndex = 15

DeviceVersionLengthMax = 6

EEGChannelsCount = 8
EEGConfigIndex = 0

ErrorBluetoothInitFailed = 2
ErrorBluetoothSocketFailed = 3
ErrorBufferOverflow = 6
ErrorBufferUnderflow = 7
ErrorConnectionProblem = 9
ErrorInvalidConfiguration = 5
ErrorInvalidHandle = -2
ErrorInvalidParameter = 1
ErrorOpenDeviceFailed = 4
ErrorOperationNotAllowed = 8
ErrorSuccess = 0
ErrorUnknownError = -1
ErrorUnsupportedDevice = 10

FirmwareVersionLengthMax = 12

GyroscopeChannelsCount = 3
GyroscopeConfigIndex = 11

NumberOfDigitalOutputs = 8

RecommendedBluetoothDeviceManufacturer = 'Cambridge Silicon Radio Ltd.'
RecommendedBluetoothDeviceName = 'CSR8510 A10'

SamplingRate = 250

SerialLengthMax = 14

StringLengthMax = 255

SupportedDeviceVersion = '1.'

TotalChannelsCount = 17

ValidationConfigIndex = 16


# functions

def GetApiVersion():  # real signature unknown; restored from __doc__
    """
    GetApiVersion() -> float
    Doc: Gets the current API version.
    Return: The API version.
    """
    return 0.0


def GetAvailableDevices(bool_paired):  # real signature unknown; restored from __doc__
    """
    GetAvailableDevices(bool paired) -> list(string)
    Doc: Discovers available paired or unpaired devices. Estimates the number 
    of available paired or unpaired devices and returns information about discovered devices.
    Parameter paired: Defines whether only paired devices or only unpaired 
    devices should be returned.If only unpaired devices 
    should be returned, an extensive device scan is performed.
    An extensive device scan takes a rather long time.In the 
    meantime, the Bluetooth adapter and the application are 
    blocked.Scanning for paired devices only can be executed 
    faster.If True, only paired devices are discovered.If 
    False, only unpaired devices can be discovered.
    Return: List holding available devices.
    Raises: DeviceException if the available devices could not be determined.
    """
    return ["Dummy"]


def GetBluetoothAdapterInfo():  # real signature unknown; restored from __doc__
    """
    GetBluetoothAdapterInfo() -> BluetoothAdapterInfo
    Doc: Evaluates which Bluetooth adapter is currently in use and whether 
    it is the recommended (delivered) Bluetooth adapter.
    Return: Information about the used Bluetooth adapter.
    Raises: DeviceException if the Bluetooth adapter info can not be read.
    """
    return BluetoothAdapterInfo


def IsDeviceLibraryLoadable(UnicornDLL):  # real signature unknown; restored from __doc__
    """
    IsDeviceLibraryLoadable(UnicornDLL) -> bool

    Doc: Checks if the device Library is loadable.
    Return: True if the device library is loadable.
    False if the device library is not loadable.
    """
    return False


# classes

class AmplifierChannel(superAmplifierChannel):
    """ The structure containing information about a single channel of the amplifier. """
    pass


class AmplifierConfiguration(superAmplifierConfiguration):
    """ The structure containing the amplifier configuration. """
    pass


class BluetoothAdapterInfo(superBluetoothAdapterInfo):
    """ The structure that holds information about the Bluetooth adapter. """
    pass


class DeviceException(superDeviceException):
    pass


class DeviceInformation(superDeviceInformation):
    """ The structure that holds additional information about the device. """
    pass


class Unicorn(superUnicorn):
    """ Unicorn object """

    def GetData(self, uint_numberOfScans, bytearray_destinationBuffer,
                uint_destinationBufferLength):  # real signature unknown; restored from __doc__
        """
        Implements the getData function.
        Produces a sawtooth wave
        :param uint_numberOfScans:
        :param bytearray_destinationBuffer:
        :param uint_destinationBufferLength:
        :return:
        """
        import time
        before = time.time()
        import struct
        for i in range(uint_numberOfScans):
            for j in range(self.GetNumberOfAcquiredChannels()):
                if self.switch:
                    struct.pack_into("f", bytearray_destinationBuffer, (i*self.GetNumberOfAcquiredChannels()+j) * 4, (i * 2) + j)
                else:
                    struct.pack_into("f", bytearray_destinationBuffer, (i*self.GetNumberOfAcquiredChannels()+j) * 4, (i + j))
        self.switch = not self.switch
        computation_time = time.time() - before
        time.sleep(0 if uint_numberOfScans/250 - computation_time < 0 else uint_numberOfScans/250 - computation_time)

    def __init__(self, *args, **kwargs):  # real signature unknown
        superUnicorn.__init__(self, args, kwargs)
        self.switch = False


# variables with complex values

__loader__ = None  # (!) real value is ''

__spec__ = None  # (!) real value is ''

