from Python.EEGAcquisition import UnicornRecorder
from matplotlib.axis import Axis
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import filtfilt
import pyqtgraph as pg
import scipy
from collections import deque
from pyqtgraph.Qt import QtGui, QtCore

import time

class EEG:
    def __init__(self):
        """
        Plotting region
        """
        self.dat = deque()
        self.maxLen = 50  # max number of data points to show on graph
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()

        """ 
            #End Region
        """
        self.rec1 = UnicornRecorder()
        self.rec1.connect()
        self.rec1.start_recording(test_signal_mode=False)
        #time.sleep(1)
        self.fs = 250.0
        self.acquiring_data(self)

    def acquiring_data(self):
        num = 0
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot([], [])
        T = 60
        plt.xlim([0, T])
        # Horizontal window range (should be fixed)
        plt.ylim([-500, 500])
        # Vertical window range (should be fixed)
        #line1, = ax.plot([], [])
        #plt.plot([], [])
        #plt.draw()
        #fig = plt.gcf()
        #fig.show()
        #fig.canvas.draw
        while True:
            self.rec1.refresh()
            data = self.rec1.get_data()
            a = data[1, :]
            b = data[3, :]
            #print(data)

            if a.size > 15:
                filteredSignal = self.filt(self, a)
                # 15000 = self.fs (250) * 1 min (60)
                tim = np.arange(15000 - a.size, 15000)/self.fs
                #tim = np.arange(0, a.size) / self.fs
                # ^ Plot the filtered "a" array against the last samples
                # which are "a.size" in number. In this way the plot curve
                # will move from right to left. If we use instead
                # tim = np.arange(0, a.size)/self.fs, we will not get our
                # desired plot.
                line.set_ydata(filteredSignal)
                line.set_xdata(tim)
                fig.canvas.draw()

                plt.pause(0.01)

            if num == 1000:
                break
            num += 1


    def filt(self, sigA):
        lowcut, highcut = 0.5, 50.0
        nyq = 0.5 * self.fs
        # below lines are converting analog into digital
        low = lowcut/nyq
        high = highcut/nyq
        order = 2
        b, a = scipy.signal.butter(order, [low, high], 'bandpass', analog=False)
        filtSignal = scipy.signal.filtfilt(b, a, sigA)

        return filtSignal

