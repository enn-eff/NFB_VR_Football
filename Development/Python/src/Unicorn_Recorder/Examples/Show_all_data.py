if __name__ == "__main__":
    from src.Plotter.MPLPrinter import MPLPrinter
    from src.Plotter.MPLPrinter import DetectionMode
    from src.Unicorn_Recorder.Dummies import RealData
    import mne
    import os
    PATH = "C:\\Users\\mare08-admin\\Desktop\\"

    printer = MPLPrinter(250)

    files = os.listdir(PATH)
    while True:
        print("Type a command: <plot>, <show>, <exit>")
        command = input()
        if command == "plot":
            print("Select a file:")
            for i in range(len(files)):
                print(f"[{i}]: {files[i]}")
            selection = int(input())
            raw = mne.io.read_raw_fif(PATH + files[selection], preload=True)
            data = raw.get_data(RealData.UNICORN_ELECTRODES)
            print(data.shape)
            printer.plot(data, bandpass=(2, 40), mode=DetectionMode.TIME, car=False, cutoff=(250, -1), label_detail=5,
                         channels=[6], label_freq_detail=2, movAvgFilter=-1)
        elif command == "show":
            printer.show()
        elif command == "exit":
            break
