if __name__ == "__main__":
    from src.Plotter.Plots.SwitchPlot import SwitchPlot as Plotclass
    from src import Unicorn_Recorder
    from src.Unicorn_Recorder.Dummies import RealData
    Unicorn_Recorder.set_backend(RealData)
    RealData.set_file_path("C:\\Users\\mare08-admin\\Desktop\\10Hz30s15Hz30sVR.fif")  # Set your own file path here
    RealData.set_electrodes(RealData.UNICORN_ELECTRODES)

    from src.Unicorn_Recorder.unicorn_recorder import Unicorn_recorder

    rec = Unicorn_recorder()
    rec.connect()
    rec.start_recording()
    rec.toggle_plot(1, Plotclass)
