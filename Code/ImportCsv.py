__author__ = 'Maximilian Kurscheidt @MadMax93'

from datetime import datetime

import numpy as np


class ImportCsv(object):
    """
    Imports 3D acceleration files in .csv format and saves it into a numpy array
    File format: Timestamp, X-Value, Y-Value, Z-Value
    """

    def __init__(self, path):
        self.path = path

    def import_csv(self):
        """
        Imports a .csv file and saves it into as numpy array. Changes the the field timestamp int a date-function
        :return: ndarray - with the needed fields
        """
        # @todo check for format - write test

        datefunc = lambda x: datetime.strptime(x.decode("utf-8"), '%Y/%m/%d %H:%M:%S.%f')
        raw_data_array = np.genfromtxt(self.path, converters={0: datefunc}, dtype=None, delimiter=",", names=True)

        return raw_data_array


    def split_up_data_in_minutes(self, raw_data_array, sample_rate):
        """
        Splits up the imported data into minute blocks. The numpy array contains numpy arrays with the values for one minute
        :param raw_data_array: Insert the full array with your raw data
        :param sample_rate: The sample rate implies the number of points per second, in which the input data is meassured
        :return: A ndarray which contains the split up ndarrays containing the one minute data parts.
        """

        # @todo Find a solution for rest data parts for example when the raw data is 4min and 50 second
        # @todo => maybe make smaller parts 10sec and multiply with 6?

        one_minute_slices = int(len(raw_data_array) / (sample_rate * 60))
        split_up_raw_data = np.array_split(raw_data_array, one_minute_slices)
        return split_up_raw_data
