if __name__ == "__main__":
    # The backend needs to be set BEFORE importing the Unicorn_recorder module
    from src import Unicorn_Recorder
    from src.Unicorn_Recorder.Dummies import SawTooth
    Unicorn_Recorder.set_backend(SawTooth)

    # Copies the example use_a_plot
    from src.Unicorn_Recorder.unicorn_recorder import Unicorn_recorder
    from src.Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass

    rec = Unicorn_recorder()
    rec.connect()
    rec.start_recording(test_signal_mode=True)
    rec.toggle_plot(1, Plotclass)
    while True:
        pass
