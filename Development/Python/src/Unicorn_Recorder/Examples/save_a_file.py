if __name__ == "__main__":
    from src import Unicorn_Recorder
    from src.Unicorn_Recorder.Dummies import SawTooth
    from src.Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass
    Unicorn_Recorder.set_backend(SawTooth)

    from src.Unicorn_Recorder.unicorn_recorder import Unicorn_recorder
    import time

    rec = Unicorn_recorder()
    rec.connect()
    rec.start_recording()
    rec.toggle_plot(1, Plotclass)
    rec.set_event(0)
    time.sleep(20)
    rec.refresh()
    rec.set_event(1)
    rec.stop_recording(wait=True)                  # Set this to wait until the recording was actually stopped
    rec.refresh()                                  # the save function only considers values that were refreshed
    rec.save("test.fif", overwrite=True)           # Saves to desktop per default.
