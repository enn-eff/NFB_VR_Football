import numpy


class Filtering:

    @staticmethod
    def car(data):
        """
            Common Average Referencing
            data needs to be a matrix (n,m) s.t. n -> number of channels and m -> number of samples
        """
        avg = numpy.average(data, axis=0)
        for i in range(data.shape[0]):
            data[i, :] = data[i, :] - avg
        return data

    @staticmethod
    def referencing(data, to_reference):
        avg = numpy.average(data, axis=0)
        for i in range(data.shape[0]):
            to_reference[i, :] = data[i, :] - avg
        return to_reference

    @staticmethod
    def movAvg(data, filter_size=0):
        """A Moving average filter"""
        out = numpy.zeros((data.shape[0], data.shape[1]-2*filter_size))
        for i in range(filter_size, data.shape[1]-filter_size):
            out[:, i - filter_size] = numpy.average(data[:, i-filter_size:i+filter_size], axis=1)
        return out

    @staticmethod
    def zero_mean(data):
        """
        Subtractts the mean for every row from the row
        :return:
        """
        for i in range(data.shape[0]):
            data[i, :] = data[i, :] - numpy.average(data[i, :])
        return data
