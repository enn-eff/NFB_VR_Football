import pyqtgraph as pg
from Python.src.Plotter.Plot import Plot
import numpy
from Python.src.Plotter.utils import generate_color
from scipy import signal
from PyQt5 import QtCore, QtGui
import mne
import time
from Python.src.Unicorn_Recorder.Filtering import Filtering


class SwitchPlot(Plot):
    """
    Main GUI window class. Defines the window and initializes the graphs
    for the data from each electrode coming from the EEG headset.
    """

    def __init__(self, queue, sfreq, info_queue=None, event_queue=None, no_plots=8):
        Plot.__init__(self, queue, sfreq, info_queue, event_queue)

        # Create the switch button
        self.window_length = 250
        self.freq_cutoff = 250

        # The field holding data
        self.data = None

        # Bandpass values
        self.lowcut = -1
        self.highcut = -1

        """GUI"""

        self.win = pg.GraphicsWindow(size=(1500, 1000))
        self.win.setWindowTitle('EEG signals')

        # until proper color are chosen, using random ones.
        self.colors = [generate_color() for _ in range(8)]

        # create 8 subplots, one for each eeg electrode.

        self.plots = [self.win.addPlot(col=1, row=1, xRange=[0, 1250], yRange=[-1, 1])]
        self.plots += [self.win.addPlot(col=2, row=1, xRange=[0, 1250], yRange=[-1, 1])]

        for index, plot in enumerate(self.plots):
            plot.setLabel(axis='left', text=f"electrode {index + 1}")
        # add one curve to each subplot
        self.curves = [plot.plot() for plot in self.plots]

        layout = self.win.addLayout(col=1, row=9)

        self.switch_button = QtGui.QPushButton("Switch Plots")
        self.switch_button.setCheckable(True)
        switch_button_container = QtGui.QGraphicsProxyWidget()
        switch_button_container.setWidget(self.switch_button)

        self.window_button = QtGui.QPushButton("Set window length")
        def clicked(): self.window_length = int(self.edit.text())
        self.window_button.clicked.connect(clicked)
        window_length_button_container = QtGui.QGraphicsProxyWidget()
        window_length_button_container.setWidget(self.window_button)

        self.edit = QtGui.QLineEdit("250")
        edit_container = QtGui.QGraphicsProxyWidget()
        edit_container.setWidget(self.edit)

        self.cutoff_button = QtGui.QPushButton("Set Frequency cutoff")
        def clicked(): self.freq_cutoff = int(self.cutoff_edit.text())
        self.cutoff_button.clicked.connect(clicked)
        cutoff_button_container = QtGui.QGraphicsProxyWidget()
        cutoff_button_container.setWidget(self.cutoff_button)

        self.cutoff_edit = QtGui.QLineEdit("250")
        cutoff_edit_container = QtGui.QGraphicsProxyWidget()
        cutoff_edit_container.setWidget(self.cutoff_edit)

        layout.addItem(switch_button_container)
        layout.addItem(window_length_button_container)
        layout.addItem(edit_container)
        layout.addItem(cutoff_button_container)
        layout.addItem(cutoff_edit_container)

        # Bandpass GUI

        layout = self.win.addLayout(col=1, row=10)

        self.edit_lowcut = QtGui.QLineEdit("-1")
        edit_lowcut_container = QtGui.QGraphicsProxyWidget()
        edit_lowcut_container.setWidget(self.edit_lowcut)

        self.edit_highcut = QtGui.QLineEdit("-1")
        edit_highcut_container = QtGui.QGraphicsProxyWidget()
        edit_highcut_container.setWidget(self.edit_highcut)

        self.bandpass_button = QtGui.QPushButton("Set Bandpass")
        def clicked(): self.highcut = int(self.edit_highcut.text()); self.lowcut = int(self.edit_lowcut.text())
        self.bandpass_button.clicked.connect(clicked)
        bandpass_button_container = QtGui.QGraphicsProxyWidget()
        bandpass_button_container.setWidget(self.bandpass_button)

        self.car_button = QtGui.QPushButton("Toggle Car")
        self.car_enabled = False
        def clicked(): self.car_enabled = not self.car_enabled
        self.car_button.clicked.connect(clicked)
        car_button_container = QtGui.QGraphicsProxyWidget()
        car_button_container.setWidget(self.car_button)

        # Events

        self.event_button = QtGui.QPushButton("Send Event")
        def clicked(): self.event_queue.put((int(self.event_edit.text()), time.time()))
        self.event_button.clicked.connect(clicked)
        event_button_container = QtGui.QGraphicsProxyWidget()
        event_button_container.setWidget(self.event_button)

        self.event_edit = QtGui.QLineEdit("0")
        event_edit_container = QtGui.QGraphicsProxyWidget()
        event_edit_container.setWidget(self.event_edit)

        layout.addItem(car_button_container)
        layout.addItem(bandpass_button_container)
        layout.addItem(bandpass_button_container)
        layout.addItem(edit_lowcut_container)
        layout.addItem(edit_highcut_container)
        layout.addItem(event_button_container)
        layout.addItem(event_edit_container)

        # Confidence Labels

        text = ''
        self.confidence_label = self.win.addLabel(text, col=2, row=9)

    def start(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        mne.set_log_level(verbose="WARNING")
        # Since our EEG headset only has a frequency of 250 hz, it should
        # suffice to use a timer of 4 ms to keep track of the incoming data.
        timer.start(4)  # strangely everything below 100 ms is the same.
        QtGui.QApplication.instance().exec_()  # may store the app handle?

    def update(self):
        """ GUI update procedure. Currently working on the global numpy array
            containing the data. Not a clean implementation, but currently the
            best.
        """
        if not self.queue.empty():
            if self.data is None:
                self.data = self.queue.get()

            else:
                self.data = numpy.append(self.data, self.queue.get(), axis=1)
            if self.data.shape[1] >= self.window_length:
                data_to_display = self.data[:, -self.window_length:]
                if self.car_enabled:
                    data_to_display = Filtering.car(data_to_display[:8])

                if 0 < self.lowcut < self.highcut and self.highcut > 0:
                    data_to_display = mne.filter.filter_data(data_to_display, sfreq=self.sfreq, l_freq=self.lowcut, h_freq=self.highcut)

                # schedule a repaint for each subplot.
                for index, curve in enumerate(self.curves):
                    pen = pg.mkPen(self.colors[index], style=QtCore.Qt.SolidLine)
                    # get the last 1250 elements
                    try:
                        print(index)
                        if index == 0:
                            sel = 1
                        else :
                            sel = 3
                        if self.switch_button.isChecked():
                            psd = signal.periodogram(data_to_display, 250)
                            curve.setData(psd[1][sel][:self.freq_cutoff], pen=pen)
                        else:
                            curve.setData(data_to_display[sel][:], pen=pen)
                    except Exception:
                        # out of bound exception. We can just ignore it and wait until
                        # the buffer has enough elements in it.
                        pass

        if self.info_queue is not None and not self.info_queue.empty():
            infos = self.info_queue.get()
            text = ""
            if "Conf" in infos.keys():
                confidence = infos["Conf"]
                text += "<font size=\"50\"><table>"
                text += f"<tr><th>Frequency</th> <th>Confidence</th></tr>"
                for freq, con in confidence:
                    text += f"<tr><td>{freq}</td><td>{con:.2f}</td></tr>"
                text += "</table></font>"
            #if "Stats" in infos.keys():
            #    stats = infos["Stats"]
            #    for stat in stats:
            #        text += "<p>"
            #        text += str(stat) + " "
            #        text += "</p>"
            self.confidence_label.setText(text)

        # apply the render events.
        pg.QtGui.QApplication.processEvents()  # not sure if necessary or useful?!
