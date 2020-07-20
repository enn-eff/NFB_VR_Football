import UnicornPy
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
                print(self.__data)
        elif isinstance(device_id, str):
            self.__eeg = UnicornPy.Unicorn(device_id) #TODO Can I be sure that it exists?
            logging.info(f"Successfully connected device {device_id}")
        else:
            print(f"device_id needs to be either int or string, got {type(device_id)}")

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

    def __plotting_loop(self, ref_interval, plot_class, info_queue=None, event_queue=None):
        """
        Starts the Plotter in a separate process and continuously feeds it newly acquired data.
        :param ref_interval:
        :param plot_class:
        :return:    #TODO close plots
        """
        plot_process = Process(name="PlotProcess", target=Unicorn_recorder.plot_wrapper,
                               args=(self.__plot_queue, plot_class, self.__SFREQ, info_queue, event_queue))
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

    #def get_sfreq(self):
    #    """
    #    Returns the sampling frequency
    #    """
    #    return self.__SFREQ