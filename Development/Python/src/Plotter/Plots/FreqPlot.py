import pyqtgraph as pg
from src.Plotter.Plot import Plot
from PyQt5 import QtCore, QtGui
import numpy
from src.Plotter.utils import generate_color
from scipy import signal


class FreqPlot(Plot):
    """
    Main GUI window class. Defines the window and initializes the graphs
    for the data from each electrode coming from the EEG headset.
    """

    def __init__(self, queue, info_queue=None):
        Plot.__init__(self, queue, info_queue)
        self.win = pg.GraphicsWindow(size=(1500, 1000))
        self.win.setWindowTitle('EEG signals')

        # create 8 subplots, one for each eeg electrode.

        self.plots = [self.win.addPlot(col=1, row=r, xRange=[0, 1250], yRange=[-1, 1]) for r in range(8)]

        print("set plots")
        for index, plot in enumerate(self.plots):
            plot.setLabel(axis='left', text=f"electrode {index + 1}")
        # add one curve to each subplot
        self.curves = [plot.plot() for plot in self.plots]

        # until proper color are chosen, using random ones.
        self.colors = [generate_color() for _ in range(8)]
        text = '<span style="font-size:20pt;font-weight:600;">Prediction confidence: 0.00</span>'
        self.confidence_label = self.win.addLabel(text, col=1, row=9)

        self.data = None

    def start(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        # Since our EEG headset only has a frequency of 250 hz, it should
        # suffice to use a timer of 4 ms to keep track of the incoming data.
        timer.start(4)  # strangely everything below 100 ms is the same.
        QtGui.QApplication.instance().exec_()  # may store the app handle?

    def update(self):
        """ GUI update procedure. Currently working on the global numpy array
            containing the data. Not a clean implementation, but currently the
            best.
        """
        #text = f'<span style="font-size:20pt;font-weight:600;">Prediction confidence: {self.data.confidence:.2f}</span>'
        #self.confidence_label.setText(text)

        if not self.queue.empty():
            if self.data is None:
                self.data = self.queue.get()
            else:
                self.data = numpy.append(self.data, self.queue.get(), axis=1)
            if self.data.shape[1] >= 250:
                data_to_display = self.data[:, -250:]

                # schedule a repaint for each subplot.
                for index, curve in enumerate(self.curves):
                    pen = pg.mkPen(self.colors[index], style=QtCore.Qt.SolidLine)
                    # get the last 1250 elements
                    try:
                        psd = signal.periodogram(data_to_display, 250)
                        curve.setData(psd[1][index][:], pen=pen)
                    except Exception:
                        # out of bound exception. We can just ignore it and wait until
                        # the buffer has enough elements in it.
                        pass
        # apply the render events.
        pg.QtGui.QApplication.processEvents()  # not sure if necessary or useful?!
