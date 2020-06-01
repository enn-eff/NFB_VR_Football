import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib import pyplot
from src.Unicorn_Recorder.Filtering import Filtering
import  mne
from scipy import signal
from scipy.fftpack import fft
import scipy
import numpy
from enum import Enum


class DetectionMode(Enum):
    """
    An auxillary class for MPLPrinter.
    Sets which domain values should be displayed in.
    """
    TIME = 0
    PSD = 1
    FFT = 2


class MPLPrinter:
    """
    A class to output EEG data in a graph using interactive matplotlib
    """

    def __init__(self, sfreq):
        #The sampling frequency
        self.sfreq = sfreq

        self.fig, self.axe = pyplot.subplots(1,1)

    def plot(self, data, zero_mean=False, car=False, bandpass=None, cutoff=(0, -1), mode=DetectionMode.TIME,
             label_detail=100, channels=None, label_freq_detail=2, title="", movAvgFilter=0):
        """
        Plots EEG data to a graph
        :param data: The EEG data given as a numpy matrix of shape(channels, samples)
        :param zero_mean: Whether to subtract the mean from the time signal. (Useless when bandpass filtering)
        :param car: Whether to apply common average referencing
        :param bandpass: when set to none no filter is applied. When seet to (x,y) sets a bandpass filter between xHz and YHz
        :param cutoff: To cutoff data in the beginning of the signal
        :param mode: The domain to display the data in
        :return: None
        """
        self.axe.set_title(title)
        channels = [] if channels is None else channels

        data = data[:, cutoff[0]:cutoff[1] if cutoff[1] > -1 else data.shape[1]]

        if car:
            data = Filtering.car(data)

        if zero_mean:
            data = Filtering.zero_mean(data)

        if bandpass is not None:
            data = mne.filter.filter_data(data, sfreq=self.sfreq, l_freq=bandpass[0], h_freq=bandpass[1])

        if movAvgFilter > 0:
            data = Filtering.movAvg(data, filter_size=20)

        if mode == DetectionMode.TIME:
            for channel in channels:
                self.axe.plot(data[channel, :])
        elif mode == DetectionMode.PSD:
            for channel in channels:
                psd = signal.periodogram(data[channel, :], self.sfreq)
                labels = []
                positions = []
                for j in range(len(psd[0])):
                    if j % label_detail == 0:
                        positions.append(j)
                        labels.append(f"{psd[0][j]:.{label_freq_detail}f}")

                self.axe.set_xticks(positions)
                self.axe.set_xticklabels(labels)
                self.axe.plot(psd[1])
        elif mode == DetectionMode.FFT:
            for channel in channels:
                fft_results = fft(data[channel, :])

                positions = numpy.array(range(1,len(fft_results)+1, label_detail))
                label_freqs = positions / len(fft_results) * self.sfreq
                labels = [f"{pos:.{label_freq_detail}f}" for pos in label_freqs]

                self.axe.set_xticks(positions)
                self.axe.set_xticklabels(labels)
                self.axe.plot(numpy.real(fft_results))
                self.axe.plot(numpy.imag(fft_results))
                self.axe.plot(numpy.absolute(fft_results))


    def show(self):
        pyplot.show(self.axe)
        self.axe.clear()
        self.fig, self.axe = pyplot.subplots(1,1)

