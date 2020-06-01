from abc import abstractmethod


class Plot:
    """
        This class provides the general structure a plotting class must have to work with the  unicorn_recorder.
    """

    def __init__(self, queue, sfreq, info_queue=None, event_queue=None):
        """
        :param queue: The queue needs to be a python multiprocessing queue
        """
        self.queue = queue
        self.sfreq = sfreq
        self.info_queue = info_queue
        self.event_queue = event_queue

    @abstractmethod
    def start(self):
        """
        The method to start the GUI
        """
        pass
