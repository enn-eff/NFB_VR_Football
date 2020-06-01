from src import Unicorn_Recorder
#from src.Unicorn_Recorder.Dummies import SawTooth as UnicornPy
#from src.Unicorn_Recorder.Dummies import RealData as UnicornPy
#UnicornPy.set_electrodes(UnicornPy.UNICORN_ELECTRODES)
#UnicornPy.set_file_path("C:\\Users\\mare08-admin\\Desktop\\CheckSwitch1510Hz2min")
import UnicornPy
Unicorn_Recorder.set_backend(UnicornPy)
from src.Unicorn_Recorder.unicorn_recorder import Unicorn_recorder
from src.Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass
from multiprocessing import Queue
import mne
import time
mne.set_log_level(verbose=False)
from src.Unicorn_Recorder.Filtering import Filtering


class Controller:

    def __init__(self, duration=-1):
        self.recorder = Unicorn_recorder()
        self.duration = duration

    def start(self):
        self.recorder.connect()

        self.recorder.start_recording()
        info_queue = Queue()
        self.recorder.toggle_plot(0.1, Plotclass, info_queue=info_queue)
        time.sleep(5)
        before = time.time()

        while True if self.duration < 0 else time.time() < before + self.duration:
            print(before + self.duration - time.time())
            before = time.time()
            data = self.recorder.get_data(-750)
            print(data.shape)
            #data = Filtering.car(data)
            data = mne.filter.filter_data(data, sfreq=self.recorder.get_sfreq(), l_freq=3, h_freq=30)

            data = data[:, 125:-125]

        self.recorder.refresh()
        self.recorder.save(filename="10Hz15HzNone15Hz10HzNone--5s--x2VR.fif", overwrite=True)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    c = Controller(duration=-1)
    c.start()
