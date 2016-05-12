__author__ = 'Maximilian Kurscheidt @MadMax93'

import os

import matplotlib.pyplot as plt

from Code import ImportCsv
from Code import Signalprocessing
from Code import Visualization

SAMPLE_RATE = 50
LOW_CUT = 0.2  # @todo Find suitable filter criteria
HIGH_CUT = 0.45


class Main(object):

    import_csv = None
    visualization = Visualization.Visualization()
    signalprocessing = Signalprocessing.Signalprocessing()

    def initialize_import(self):

        '''Import csv file'''
        directory = os.path.dirname(__file__)

        filename = os.path.join(directory, '../files/case1.csv')

        import_csv = ImportCsv.ImportCsv(filename)
        raw_data_array = import_csv.import_csv()

        #visualization.visualise_raw_data_combined(raw_data_array)

        '''Split up import data'''
        split_up_raw_data_array = import_csv.split_up_data_in_minutes(raw_data_array, SAMPLE_RATE)

        return split_up_raw_data_array

    def pipeline_for_one_minute_data(self, split_up_raw_data_array):

        '''
        Digital signal processing pipeline for the one minute data
        :param split_up_raw_data_array: ndarray - split up signal array
        '''

        #visualization.visualise_raw_data_combined(split_up_raw_data_array)
        #visualization.visualise_raw_data_separate(split_up_raw_data_array)

        '''Band-Pass Filter X,Y,Z Axis'''

        filtered_signal_x = Main.signalprocessing.butter_bandpass_filter(split_up_raw_data_array['X'], LOW_CUT, HIGH_CUT,
                                                                    SAMPLE_RATE)
        filtered_signal_y = Main.signalprocessing.butter_bandpass_filter(split_up_raw_data_array['Y'], LOW_CUT, HIGH_CUT,
                                                                    SAMPLE_RATE)
        filtered_signal_z = Main.signalprocessing.butter_bandpass_filter(split_up_raw_data_array['Z'], LOW_CUT, HIGH_CUT,
                                                                    SAMPLE_RATE)
        #visualization.visualise_filtered_signal_combined(filtered_signal_x, filtered_signal_y, filtered_signal_z)
        #visualization.visualise_filtered_signal_separate(filtered_signal_x, filtered_signal_y, filtered_signal_z)

        #b, a = signalprocessing.butter_bandpass_design(LOW_CUT, HIGH_CUT, SAMPLE_RATE, 4)
        #visualization.visualise_filter_design(b, a, SAMPLE_RATE)


        '''Spectrum analysis'''
        yf_x, frq_x = Main.signalprocessing.fast_fourier_transformation(filtered_signal_x, SAMPLE_RATE)
        yf_y, frq_y = Main.signalprocessing.fast_fourier_transformation(filtered_signal_y, SAMPLE_RATE)
        yf_z, frq_z = Main.signalprocessing.fast_fourier_transformation(filtered_signal_z, SAMPLE_RATE)

        power_x = Main.signalprocessing.power_of_the_spectrum(yf_x)
        power_y = Main.signalprocessing.power_of_the_spectrum(yf_y)
        power_z = Main.signalprocessing.power_of_the_spectrum(yf_z)

        power_max, frq_max = Main.signalprocessing.maximum_power_of_xyz_spectrum(power_x, power_y, power_z, SAMPLE_RATE)
        #visualization.visualise_power_spectrum_combined(frq_x, power_x, y_y=power_y, y_z=power_z)
        #visualization.visualise_power_spectrum_combined(frq_x, power_x, y_y=power_y, y_z=power_z, y_max=power_max)

        positive_max_ps_for_peak_detection = Main.signalprocessing.positive_power_spectrum_for_peak_detection(power_max)

        peak_tupel = Main.signalprocessing.find_peak_and_frequency(positive_max_ps_for_peak_detection, frq_max)
        #visualization.visualise_peak(frq_x, power_max, peak_tupel, y_x=power_x)

        rr = Main.signalprocessing.calculate_rr_from_power_spectrum(peak_tupel)
        print(rr)
        #visualization.visualise_peak(frq_x, power_max, peak_tupel, y_x=power_x, rr=rr)

        Main.visualization.visualise_signals_and_xyz_and_maximum_power_spectrum(filtered_signal_x, filtered_signal_y, filtered_signal_z, power_x, power_y, power_z, power_max, frq_x, peak_tupel, rr)

if __name__ == "__main__":
    split_up_raw_data_array = Main().initialize_import()
    for i in range(len(split_up_raw_data_array)):
        print(i)
        Main().pipeline_for_one_minute_data(split_up_raw_data_array[i])
    plt.show()
    #plt.draw()