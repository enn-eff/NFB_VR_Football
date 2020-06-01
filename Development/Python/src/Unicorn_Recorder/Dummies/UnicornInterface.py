from abc import abstractmethod
import logging

# encoding: utf-8
# module UnicornPy
# from C:\Users\Tobias\Documents\gtec\Unicorn Suite\Hybrid Black\Unicorn Python\Lib\UnicornPy.pyd
# by generator 1.145
""" A Python interface for Unicorn brain interfaces """
# no imports

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

class AmplifierChannel(object):
    """ The structure containing information about a single channel of the amplifier. """

    def __init__(self, Enabled=True, Name="Channel", Range=None, Unit=""):  # real signature unknown
        self.Enabled = Enabled
        """The Channel enabled flag. True to enable channel; False to disable channel."""

        self.Name = Name
        """The Name of the channel."""

        self.Range = Range
        """The Range of the channel. First entry min value; Second max value."""

        self.Unit = Unit  # TODO sensful values
        """The unit of the channel."""





class AmplifierConfiguration:
    """ The structure containing the amplifier configuration. """

    def __init__(self, *args, **kwargs):
        """A list of 'AmplifierChannel' representing all channels."""
        self.Channels = []
        for i in range(TotalChannelsCount):
            self.Channels.append(AmplifierChannel(Name=f"EEG Channel {i}"))



class BluetoothAdapterInfo(object):
    """ The structure that holds information about the Bluetooth adapter. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    HasProblem = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Indicates whether the Bluetooth adapter has reported a problem or not. True if the adapter reported a problem; False if the adapter behaves as supposed."""

    IsRecommendedDevice = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The flag indicating if the used Bluetooth adapter is a recommended (delivered) device. True if the adapter is a recommended device; False if the adapter is not a recommended device."""

    Manufacturer = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The manufacturer of the Bluetooth adapter."""

    Name = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The name of the Bluetooth adapter used."""


class DeviceException(Exception):
    # no doc
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    __weakref__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """list of weak references to the object (if defined)"""


class DeviceInformation(object):
    """ The structure that holds additional information about the device. """

    def __init__(self, *args, **kwargs):  # real signature unknown
        pass

    @staticmethod  # known case of __new__
    def __new__(*args, **kwargs):  # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    DeviceVersion = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The device version number."""

    EnclosureVersion = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The enclosure version number."""

    FWVersion = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The firmware version number."""

    NumberOfEegChannels = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The number of EEG channels."""

    PCBVersion = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The PCB version number."""

    Serial = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """The serial number of the device."""


class Unicorn(object):
    """ Unicorn object """

    def GetChannelIndex(self, string_channelName):  # real signature unknown; restored from __doc__
        """
        GetChannelIndex(string channelName) -> uint channelIndex
        Doc: Uses the currently set 'AmplifierConfiguration' to get the index of the requested
        channel in an acquired scan.
        Parameter channelName: The name of the requested channel
        The default names are:
            EEG 1|2|3|4|5|6|7|8
            Accelerometer X|Y|Z
            Gyroscope X|Y|Z
            Counter
            Battery Level
            Validation Indicator
        Return: The index of the requested channel in an acquired scan.
        Raises: DeviceException if the channel index could not be determined.
        """
        pass

    def GetConfiguration(self):  # real signature unknown; restored from __doc__
        """
        GetConfiguration() -> AmplifierConfiguration configuration
        Retrieves the current amplifier configuration from the device as 'AmplifierConfiguration'
        Return: The 'AmplifierConfiguration' which stores the current configuration of the amplifier.
        Raises: DeviceException if the configuration could not be read.
        """
        return self.amplifier_configuration

    @abstractmethod
    def GetData(self, uint_numberOfScans, bytearray_destinationBuffer,
                uint_destinationBufferLength):  # real signature unknown; restored from __doc__
        """
        GetData(uint numberOfScans, bytearray destinationBuffer, uint destinationBufferLength)
        Doc: Reads a specific number of scans into the specified destination buffer of known length.
        Checks whether the destination buffer is big enough to hold the requested number of scans.
        Parameter numberOfScans: The number of scans to read. The number of scans must be greater than zero.
        A scan consists of one 32-bit floating point number for each currently acquired channel.
        Parameter destinationBuffer: The destination buffer to store data at. The destination buffer 
        must provide enough memory to hold the requested number of scans multiplied by the number of acquired channels.
        Call 'GetNumberOfAcquiredChannels()' to determine the number of acquired channels.
        Call 'GetChannelIndex(string channelName)' to determine the index of a channel in the acquisition buffer.
        Example: The sample of the battery level channel in the n-th scan is:
        n*GetNumberOfAcquiredChannels()+GetChannelIndex('Battery Level')
        Parameter destinationBufferLength: The number of floats fitting into the destination buffer.
        Raises: DeviceException if the data could not be read.
        """
        pass


    def GetDeviceInformation(self):  # real signature unknown; restored from __doc__
        """
        GetDeviceInformation() -> DeviceInformation deviceInformation
        Doc: Reads the device information.
        Return: A 'DeviceInformation' which holds information about the device.
        Raises: DeviceException if the device information could not be read.
        """
        return DeviceInformation

    def GetDigitalOutputs(self):  # real signature unknown; restored from __doc__
        """
        GetDigitalOutputs() -> byte digitalOutputs
        Doc: Reads the digital output states.
        Return: The state of the digital output channels to set in bits.
        Each bit represents one digital output channel. Set a bit to set the
        corresponding digital output channel's value to high. Clear a bit to
        set the corresponding digital output channel's value to low.
           Examples (the binary representation of each decimal value is shown in parentheses):
              0   (0b00000000) -> all digital outputs set to low.
              170 (0b10101010) -> digital outputs 2, 4, 6, 8 are set to high.
              255 (0b11111111) -> all digital outputs set to high.
        Raises: DeviceException if the digital outputs could not be read.
        """
        return b""

    def GetNumberOfAcquiredChannels(self):  # real signature unknown; restored from __doc__
        """
        GetNumberOfAcquiredChannels() -> uint numberOfAcquiredChannels
        Doc: Get number of acquired channels according to the currently set amplifier configuration.
        Return: The number of acquired channels.Raises: DeviceException if the number of acquired channels could not be determined.
        """
        return TotalChannelsCount #TODO this is just total

    def SetConfiguration(self, AmplifierConfiguration_configuration):  # real signature unknown; restored from __doc__
        """
        SetConfiguration(AmplifierConfiguration configuration)
        Doc: Sets an amplifier configuration.
        Parameter configuration: The 'AmplifierConfiguration' to set
        Raises: DeviceException if the configuration could not be set.
        """
        pass

    def SetDigitalOutputs(self, byte_digitalOutputs):  # real signature unknown; restored from __doc__
        """
        SetDigitalOutputs(byte digitalOutputs)
        Doc: Sets the digital outputs to high or low.
        Parameter digitalOutputs: The digital output states in bits.
        Each bit represents one digital output channel.
        If a bit is set, the corresponding digital output channel's value is
        set to high. If a bit is cleared, the corresponding digital output
        channel's value is set to low.
           Examples (the binary representation of each decimal value is shown in parentheses):
              0   (0b00000000) -> all digital outputs set to low.
              170 (0b10101010) -> digital outputs 2, 4, 6, 8 are set to high.
              255 (0b11111111) -> all digital outputs set to high.
        Raises: DeviceException if the digital outputs could not be set.
        """
        pass

    def StartAcquisition(self, bool_testSignalEnabledFlag):  # real signature unknown; restored from __doc__
        """
        StartAcquisition(bool testSignalEnabledFlag)
        Doc: Starts a data acquisition in testsignal or measurement mode.
        Parameter testSignalEnabledFlag: Enables or disables the test signal mode.
        True to start the data acquisition in test signal mode; Falseto start 
        the data acquisition in measurement mode.
        Raises: DeviceException if the data acquisition could not be started.
        """
        pass

    def StopAcquisition(self):  # real signature unknown; restored from __doc__
        """
        StopAcquisition()
        Doc: Terminates a running data acquisition.
        Raises: DeviceException if the data acquisition could not be stopped.
        """
        pass

    def __init__(self, *args, **kwargs):  # real signature unknown
        device = args[0]
        self.name = device
        self.amplifier_configuration = AmplifierConfiguration()

        # Whether the EEG is currently acquiring data
        self.aquisition_state = False

        logging.warning("DUMMY EEG IS ACTIVATED, YOU WILL NOT RECORD REAL EEG DATA!")


# variables with complex values

__loader__ = None  # (!) real value is ''

__spec__ = None  # (!) real value is ''

