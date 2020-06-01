eeg_backend = None


def set_backend(backend):
    global eeg_backend
    eeg_backend = backend


def get_backend():
    global eeg_backend
    print("Backend: ", eeg_backend)
    if eeg_backend is None:
        import UnicornPy
        return UnicornPy
    else:
        return eeg_backend
