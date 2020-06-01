
from src.Unicorn_Recorder.unicorn_recorder import Unicorn_recorder

# Try activating different plot classes here to see the functionality
from src.Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass
#from Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass

# Note that since we are working with multiple processes this if clause is necessary.




class EEG:
    def __init__(self):
        rec = Unicorn_recorder()
        rec.connect()
        rec.start_recording(test_signal_mode=False)
        rec.toggle_plot(1, Plotclass)

        return b"Nauman"