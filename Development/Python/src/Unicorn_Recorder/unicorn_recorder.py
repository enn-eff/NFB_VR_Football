"""
The Unicorn Recorder
Author: Tobias Jungbluth
This class is supposed to help with recording with the gtec Unicorn device.
The manual mentioned throughout the documentation is the "User Manual for Unicorn Brain Interface Hybrid Black".
Manual Version Number: 1.18.00
"""
import multiprocessing
if multiprocessing.current_process().name == "MainProcess":  # TODO this solution is terrible
    from Python.src.Unicorn_Recorder import get_backend
    UnicornPy = get_backend()
else:
    from Python.src.Unicorn_Recorder.Dummies import UnicornInterface
    UnicornPy = UnicornInterface

import numpy
import struct
import threading
from enum import Enum
import statistics
from scipy import signal
from scipy import fftpack
import mne
import time
from multiprocessing import Queue, Process
import logging
import os


class Signal_quality(Enum):
    """
    A simple enum to differentiate between different signal qualities
    """

    BAD =           0b00
    GOOD =          0b01

    STD_FAILED =    0b10
    BPMD_PASSED =   0b11

class Unicorn_recorder:

    # The space needed to store a single value from any channel
    # See manual 16.6.5.2.3
    __BYTES_PER_CHANNEL = 4
    __BANDWITH = 4 #TODO find good bandwith

    # Path to save to if None is given
    DEFAULT_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\')

    # The sampling frequency of the EEG
    # See manual 15.6.1, 2.1
    # This should always be 250
    __SFREQ = UnicornPy.SamplingRate

    def __init__(self, path=None):
        self.__eeg = None

        # The recorded EEG data and events.
        self.__data = None
        self.__data_lock = threading.Lock()
        self.__events = []

        self.__unpacked_data = []
        self.__unpacked_data_lock = threading.Lock()
        self.__recording_thread = None
        self.__plotting_thread = None

        # Length of the data since last get_new_data call
        self.__new_data_index = 0

        # The path to save eeg data and events to.
        # If set to none will attempt to save at default path.
        self.path = path
        self.__plot_queue = Queue()

    def connect(self, device_id=0, paired=True):
        """
        Connects to the specified device.
        Throws an IndexError if specified device was not found
        :param device_id: Can either be string, to connect to a device with a specific name or int specifying an index
                          of all available devices
        :param paired: Whether to check for paired or unpaired devices.
                       If you have knowledge on Bluetooth feel free to experiment with this.
                       If not, then pair the device via the Unicorn Suite first and leave it True.
                       See manual 15.6.4.2
        :return: None
        """
        if isinstance(device_id, int):
            devices = UnicornPy.GetAvailableDevices(paired)
            if len(devices) <= device_id >= 0:
                raise IndexError(f"ID: {device_id} is not valid. "
                                 f"ID is either wrong or devicce was not found."
                                 f"Number of available devices: {devices}")
            else:
                self.__eeg = UnicornPy.Unicorn(devices[0])
                logging.info(f"Successfully connected device {device_id}")
                self.__data = numpy.zeros((self.__eeg.GetNumberOfAcquiredChannels(), 1))
        elif isinstance(device_id, str):
            self.__eeg = UnicornPy.Unicorn(device_id) #TODO Can I be sure that it exists?
            logging.info(f"Successfully connected device {device_id}")
        else:
            print(f"device_id needs to be either int or string, got {type(device_id)}")

    def get_Configuration(self):
        """
        Returns the Configuration so that easy changes can be made to it.
        :return: the eeg channels, the accelarator channels, the gyroscope hannels, battery, counter and val ind. #TODO Beleg
        """
        configuration = UnicornPy.AmplifierConfiguration() #TODO macht das Sinn?
        channels = configuration.Channels
        eeg_channels = channels[:8]
        acc_channels = channels[8:11]
        gyro_channels = channels[11:14]
        battery_channel = channels[14]
        counter_channel = channels[15]
        val_ind_channel = channels[16]
        return eeg_channels

    def start_recording(self, frame_length=10, test_signal_mode=False):
        """ TODO frame_length default value
            Starts a recording.
            Note, that the Unicorn is continuously capturing data.
        :return:
        """
        if test_signal_mode:
            logging.warning("TEST SIGNAL MODE IS ENABLED, YOU WILL NOT RECORD REAL EEG DATA!")
        self.__eeg.StartAcquisition(test_signal_mode)
        self.__recording_thread = threading.Thread(name="RecordingThread", target=self.__recording_loop, args=(frame_length,))
        self.__recording_thread.start()

    def stop_recording(self, wait=True):
        """
        Stops the recording. Waits for it to end if wait is set to true.
        :return:None
        """
        self.__recording_thread.is_running = False
        if wait:
            self.__recording_thread.join()

    def __recording_loop(self, frame_length=1):
        """
        Starts a continuous recording.
        See manual 15.5.4 and 15.6.5.2.3
        :return:None
        """
        current_thread = threading.currentThread()

        buffer_length = frame_length * self.__eeg.GetNumberOfAcquiredChannels() * self.__BYTES_PER_CHANNEL
        while getattr(current_thread, "is_running", True):
            buffer = bytearray(buffer_length)
            self.__eeg.GetData(frame_length, buffer, buffer_length)
            with self.__unpacked_data_lock:
                self.__unpacked_data.append(buffer)

    def refresh(self):
        """
        Get the data that was recorded since the last call to refresh.
        If there was no previous call to refresh, since the last call to start_recording
        !WARNING! THIS FUNCTION WILL NOT WORK IF NO EEG IS CONNECTED
        :return: None
        """
        # Get the recorded data and remove it from the buffer
        with self.__unpacked_data_lock:
            unpacked_data = self.__unpacked_data
            self.__unpacked_data = []
        # Since the old data is no longer new, set the new index to its maximum

        """
        Unpack the data and write it to the data matrix.
        The unpacking is specified in manual 16.6.5.2.3
        Note, that the accuracy of the sample is 24 bit. The 32 bit float values are generated because python expects 
        that size in the struct library.
        The whole packed data consists of a number of (channels * bytes per channel * number of samples) bytes.
        """

        eff = struct.Struct("f" * self.__eeg.GetNumberOfAcquiredChannels())
        samples = []
        for buffer in unpacked_data: # TODO Is this safe?
            for sample in eff.iter_unpack(buffer):
                samples.append(sample)
            del buffer
        if len(samples) > 0:
            with self.__data_lock:
                self.__data = numpy.append(self.__data, numpy.matrix(samples).transpose(), axis=1).getA()

    def get_sfreq(self):
        """
        Returns the sampling frequency
        """
        return self.__SFREQ

    def get_data(self, cutoff=0):
        """
        Returns a copy of the data recorded since the last refresh.
        Note that by Default the data is filtered by a 0Hz Highpass, so no highpass, and a 10.23kHz lowpass filter,
        see manual 7.2
        Also note that the data is measured in millivolt, see manual 7.2
        For transformation to Volt multiply by 10e-3
        :return:
        """
        with self.__data_lock:
            data = self.__data[:, cutoff:].copy()
        return data

    def get_new_data(self, index=None):
        """
        Returns the new data acquired since the last call to refresh
        :return:
        """
        with self.__data_lock:
            if index is None:
                return self.__data[:, self.__new_data_index:].copy()
            else:
                return self.__data[:, index:].copy()

    def set_event(self, event_id, caller_offset=0, real_time=False):
        """
        Sets an event with event_id.
        The sample set for the event is given by the the number of the last data sample
        :param event_id: The unigue integer id of the event
        :param caller_offset: Offsets the saved sample by the current amount. If an event is found 1 s after it occurred
                              use -sfreq to offset the saved event correctly
        :param real_time: Whether to place the event at the last sample record in real time
                          or the last time refresh was called
        :return: None
        """
        with self.__data_lock:
            event_sample = len(self.__data) + caller_offset
        if real_time:
            with self.__unpacked_data_lock:
                pack_length = len(self.__unpacked_data)
            event_sample += pack_length / 4 / self.__eeg.getNumberOfAcquiredChannels()
        self.__events.append(numpy.array([event_id, 0, event_sample]))  # TODO mne events beleg

    def clear(self):
        """
        Resets the data and event lists.
        Note that data refresh will still add data that was recorded before the call to clear.
        !WARNING! EVENTS WILL START AT SAMPLE ZERO AFTERWASRDS
        :return: None
        """
        self.__events = numpy.empty((0, 3))
        with self.__data_lock:
            self.__data = numpy.empty((17, 0)) #TODO zero array
        self.__new_data_index = 0

    def save(self, filename, overwrite=False, path=None):
        """
        Saves the data between the last clear and the last refresh to a a file.
        File is saved at path with filename name as a fif file.
        For help with mne, see:
        RawArray:
        https://mne.tools/stable/generated/mne.io.RawArray.html

        Creating an object:
        - https://mne.tools/stable/generated/mne.create_info.html#mne.create_info

        Creating a montage:
        - https://mne.tools/stable/generated/mne.Info.html#mne.Info.set_montage
        - https://mne.tools/stable/generated/mne.channels.make_dig_montage.html#mne.channels.make_dig_montage

        :return: None
        """
        if path is None:
            path = self.path
            if path is None:
                logging.warning("Function did not specify path to save to, neither did the class."
                                f"Attempting to save to {self.DEFAULT_PATH}")
                path = self.DEFAULT_PATH

        configuration = self.__eeg.GetConfiguration()
        channels = configuration.Channels
        enabled_channels = [channel for channel in channels if channel.Enabled]

        channel_names = [channel.Name for channel in enabled_channels]
        channel_types = ['eeg' for channel in channels[:UnicornPy.EEGChannelsCount] if channel.Enabled]
        channel_types += ['misc' for channel in channels[UnicornPy.EEGChannelsCount:] if channel.Enabled]

        info = mne.create_info(channel_names, self.__SFREQ, channel_types)
        print("Events", self.__events)
        info['events'] = [{'list': event} for event in self.__events]

        #montage = mne.channels.make_dig_montage() #TODO electrode positions aren't in the docs. Measure them ourselves?
        #info.set_montage([])

        data = self.get_data()

        print(data, info['ch_names'])
        raw = mne.io.RawArray(data, info) #TODO Beleg

        if overwrite:
            logging.warning("Overwriting saved file")
        raw.save(path + filename, overwrite=overwrite)
        print("File successfully saved")

    def disconnect(self):
        """
        Disconnects the currently connected device.
        It is not necessary to call this function explicitly.
        The garbage collector will disconnect it automatically.
        Use only, if you need to connect to it repeatedly.
        See manual 15.5.5 and 15.5.6
        :return: None
        """
        del self.__eeg

    def toggle_plot(self, ref_interval, plot_class, info_queue=None, event_queue=None):
        """
        Enables an automatic plot for the incoming EEG data
        :param ref_interval: the interval in which the plot should be updated.
        :return:
        """
        if self.__plotting_thread is None:
            self.__plotting_thread = threading.Thread(name="PlottingThread", target=self.__plotting_loop,
                                                      args=(ref_interval, plot_class, info_queue, event_queue))
            self.__plotting_thread.start()
        else:
            self.__plotting_thread.is_running = False
            self.__recording_thread.join()
            self.__plotting_thread = None

    @staticmethod
    def plot_wrapper(queue, plot_class, sfreq, info_queue=None, event_queue=None):
        """
        A simple wrapping function for starting a plot in another Process
        :param queue: a multiprocessing queue EXCLUSIVELY used for transferring EEG data
        :param sfreq: the sampling frequency
        :param plot_class: The class defining a Plot
        :return:
        """
        plot = plot_class(queue, sfreq, info_queue, event_queue)
        plot.start()

    def __plotting_loop(self, ref_interval, plot_class, info_queue=None, event_queue=None):
        """
        Starts the Plotter in a separate process and continuously feeds it newly acquired data.
        :param ref_interval:
        :param plot_class:
        :return:    #TODO close plots
        """
        plot_process = Process(name="PlotProcess", target=Unicorn_recorder.plot_wrapper,
                               args=(self.__plot_queue, plot_class, self.get_sfreq(), info_queue, event_queue))
        plot_process.start()

        with self.__data_lock:
            observer_index = self.__data.shape[1]

        while plot_process.is_alive():
            before = time.time()
            self.refresh()
            data = self.get_new_data(observer_index)
            self.__plot_queue.put(data)

            observer_index += data.shape[1]
            t = ref_interval - (time.time() - before)
            time.sleep(0 if t <= 0 else t)

    @staticmethod
    def check_signal_quality(data, sfreq):
        """
        The quality check described in 18.8.2 in the manual
        :param data: the data matrix. Tobe in accordance with the manual, input exactly 2 seconds of material
        :return: The signal quality in BAD=0 POOR=1 and GOOD=2
        """
        std_checks = Unicorn_recorder.check_std(data)
        bpmd_checks = Unicorn_recorder.check_bpmd(data, sfreq)
        return [Signal_quality.GOOD if std_checks[i] and bpmd_checks[i] else
                (Signal_quality.POOR if std_checks[i] or bpmd_checks[i] else Signal_quality.BAD)
                for i in range(len(data))]

    @staticmethod
    def check_std(data):
        """
        The standard deviation check as described in 18.8.2 in the manual.
        :param data: the data matrix
        :return: a boolean array indicating good(True) and bad(False) signal quality for each channel
        """
        return [7 < statistics.stdev(row) < 50 for row in data]

    @staticmethod
    def check_bpmd(data, sfreq):
        """
        The standard bandpass median difference check as described in 18.8.2 in the manual.
        Should only be called on 1s of material TODO manual?
        :param data: the data matrix
        :return: a boolean array indicating good(True) and bad(False) signal quality for each channel
        """

        # Apply Notch filters
        fif_num, fif_dem = signal.iirnotch(50, 50 / Unicorn_recorder.__BANDWITH, fs=sfreq)
        six_num, six_dem = signal.iirnotch(60, 60 / Unicorn_recorder.__BANDWITH, fs=sfreq)#TODO This is a problem. The filter will just look weird
        notch_data = [signal.lfilter(six_num, six_dem, signal.lfilter(fif_num, fif_dem, row)) for row in data]
        notch_freqs = [fftpack.rfft(row) for row in notch_data]
        notch_mean = [sum(row[51 - 2:51 + 2]) / len(row[51 - 2:51 + 2]) +
                      sum(row[61 - 2:61 + 2]) / len(row[61 - 2:61 + 2])
                      for row in notch_freqs]
        notch_mean = [val / 2 for val in notch_mean]

        # Apply Band Pass
        band_num, band_dem = signal.butter(2, [0.1 / (sfreq / 2), 30 / (sfreq / 2)], output='ba', btype="bandpass") # TODO WHat is a good filter here?
        band_data = [signal.lfilter(band_num, band_dem, signal.lfilter(band_num, band_dem, row)) for row in data]
        band_freqs = [fftpack.rfft(row) for row in band_data]
        band_mean = [sum(row[1:30]) / len(row[1:30])
                     for row in band_freqs]

        return [band_mean[i] - notch_mean[i] > 0.1 for i in range(len(band_mean))]
