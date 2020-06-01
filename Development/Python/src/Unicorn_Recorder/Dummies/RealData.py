"""
Dummy for UnicornPy
Outputs data from a fif file on all electrodes.
The PATH for the file needs to be set before hand with set_file_path and the electrodes with set_electrodes
"""

from src.Unicorn_Recorder.Dummies.UnicornInterface import Unicorn as superUnicorn
from src.Unicorn_Recorder.Dummies.UnicornInterface import DeviceInformation as superDeviceInformation
from src.Unicorn_Recorder.Dummies.UnicornInterface import DeviceException as superDeviceException
from src.Unicorn_Recorder.Dummies.UnicornInterface import BluetoothAdapterInfo as superBluetoothAdapterInfo
from src.Unicorn_Recorder.Dummies.UnicornInterface import AmplifierChannel as superAmplifierChannel
from src.Unicorn_Recorder.Dummies.UnicornInterface import AmplifierConfiguration as superAmplifierConfiguration
from src.Unicorn_Recorder.Dummies import UnicornInterface

import mne
PATH = None
ELECTRODES = None
UNICORN_ELECTRODES = list(range(17))


def set_file_path(path):
    global PATH
    PATH = path


def set_electrodes(electrodes):
    global ELECTRODES
    ELECTRODES = electrodes


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

GetApiVersion = UnicornInterface.GetApiVersion

GetAvailableDevices = UnicornInterface.GetAvailableDevices

GetBluetoothAdapterInfo =  UnicornInterface.GetBluetoothAdapterInfo

IsDeviceLibraryLoadable = UnicornInterface.IsDeviceLibraryLoadable


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
                uint_destinationBufferLength):
        """
        Implements the getData function.
        Uses self.data to output a signal
        :param uint_numberOfScans:
        :param bytearray_destinationBuffer:
        :param uint_destinationBufferLength:
        :return:
        """
        import time
        before = time.time()
        import struct
        for value_index in range(uint_numberOfScans):
            index = (value_index + self.head) % self.data.shape[1]
            for channel_index in range(self.GetNumberOfAcquiredChannels()):
                struct.pack_into("f", bytearray_destinationBuffer, (channel_index + TotalChannelsCount * value_index) * 4,
                                 self.data[channel_index, index])
        self.head += uint_numberOfScans
        self.head %= self.data.shape[1]
        computation_time = time.time() - before
        time.sleep(0 if uint_numberOfScans/250 - computation_time < 0 else uint_numberOfScans/250 - computation_time)

    def __init__(self, *args, **kwargs):  # real signature unknown
        superUnicorn.__init__(self, args, kwargs)

        global PATH
        global ELECTRODES

        # Load a fif file specified in PATH and retrieve its content
        if PATH is None:
            raise Exception("No file path was given. Please set the path with set_file_path() before using the dummy")
        else:
            raw = mne.io.read_raw_fif(PATH, preload=True)
            print("Events: ", raw.info["events"])

        if ELECTRODES is None:
            raise Exception("No file path was given. Please set the path with set_file_path() before using the dummy")
        else:
            self.data = raw.get_data(ELECTRODES)


        # The point at which to look for new data in getData
        self.head = 0

# variables with complex values


__loader__ = None  # (!) real value is ''

__spec__ = None  # (!) real value is ''

