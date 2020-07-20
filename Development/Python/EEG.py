
#from Python.src.Unicorn_Recorder.unicorn_recorder import Unicorn_recorder
# Try activating different plot classes here to see the functionality
from Python.src.Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass
#from Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass

from Python.UnicornRecorder import Unicorn_recorder

from Python.EEGAcquisition import UnicornRecorder
# Note that since we are working with multiple processes this if clause is necessary.
import matplotlib.pyplot as plt

import time

class EEG:
    def __init__(self):
        rec1 = UnicornRecorder()
        rec1.connect()
        rec1.start_recording(test_signal_mode=False)

        #a = rec1.get_data()[1, :]
        #rec1.custom_Plot()

        #rec1.toggle_plot(1, Plotclass)
        rec1.refresh()
        #a = rec1.get_data()[1, :]

        #plt.plot(10, a)
        #plt.show()
        ##rec.get_Configuration()
        ##int(rec.get_Configuration())
        #rec.start_recording(test_signal_mode=False)

        #rec.toggle_plot(1, Plotclass)

        #rec.refresh()
        #a = rec.get_data()[1,:]

        #b = rec.get_data()[3,:]


        #from scipy import signal
        #psd = signal.periodogram(a, 250)
        #abc = signal.periodogram(b, 250)
        #time.sleep(1)


        return b"Nauman"


    #def filter(self, x):

