__author__ = 'Maximilian Kurscheidt @MadMax93'

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import peakutils
import matplotlib.gridspec as gridspec
from peakutils.plot import plot as pplot
from matplotlib.offsetbox import AnchoredText


class Visualization(object):

    def visualise_raw_data_combined(self, raw_data_array):
        data_x = raw_data_array['X']
        data_y = raw_data_array['Y']
        data_z = raw_data_array['Z']

        array_len = range(0, len(raw_data_array))
        fig, ax = plt.subplots(1, sharex=True)

        xl, = ax.plot(array_len, data_x, 'r', label='X-Axis')
        fig.suptitle('Raw signal all axes combined')
        plt.xlabel('Time in points (50dp/sec)')
        plt.ylabel('Signal value')

        yl, = ax.plot(array_len, data_y, 'b', label='Y-Axis')
        zl, = ax.plot(array_len, data_z, 'g', label='Z-Axis')

        fig.legend((xl, yl, zl), ('X-Axis', 'Y-Axis', 'Z-Axis'),loc='center right', fontsize=9)
        #plt.show()

    def visualise_raw_data_separate(self, raw_data_array):
        data_x = raw_data_array['X']
        data_y = raw_data_array['Y']
        data_z = raw_data_array['Z']

        array_len = range(0, len(raw_data_array))

        fig, ax = plt.subplots(3, sharex=True)

        xl, = ax[0].plot(array_len, data_x, 'r', label='X-Axis')

        fig.suptitle('Raw signal all axes combined', fontsize='large')
        plt.xlabel('Time in points (50dp/sec)')
        plt.ylabel('Signal value')

        yl, = ax[1].plot(array_len, data_y, 'b', label='Y-Axis')
        zl, = ax[2].plot(array_len, data_z, 'g', label='Z-Axis')

        ax[0].set_title('Raw signal - X-Axis', fontsize='medium')
        ax[1].set_title('Raw signal - Y-Axis', fontsize='medium')
        ax[2].set_title('Raw signal - Z-Axis', fontsize='medium')

        fig.legend((xl, yl, zl), ('X-Axis', 'Y-Axis', 'Z-Axis'), loc='center right', fontsize=9)
        #plt.show()

    def visualise_signals_and_xyz_and_maximum_power_spectrum(self, filtered_signal_x, filtered_signal_y, filtered_signal_z, y_x, y_y, y_z, y_max, frq, peak_tupel, rr):
        array_len = range(0, len(filtered_signal_x))
        N = y_x.size

        #plt.xkcd() #HAHA! COMIC STYLE - XKCD
        fig, ax = plt.subplots(2, 1)
        fig.suptitle('Combined plot with the bandpass filtered signals, power spectra and the rr.', fontsize="large")

        ax[0].plot(array_len, filtered_signal_x, 'r', label='Bandpass filtered X')
        ax[0].plot(array_len, filtered_signal_y, 'b', label='Bandpass filtered Y')
        ax[0].plot(array_len, filtered_signal_z, 'g', label='Bandpass filtered Z')
        ax[0].set_xlabel('Time in points (50dp/sec)')
        ax[0].set_ylabel('Amplitude')
        ax[0].legend(loc='best', fontsize=9)
        ax[0].set_title("Bandpass filtered signals for X,Y,Z", fontsize="medium")
        # plotting the spectrum
        ax[1].plot(frq,  2.0/N * np.abs(y_x[0:N/2]), 'r', label='Power spectrum X')
        ax[1].plot(frq, 2.0/N * np.abs(y_y[0:N/2]), 'b', label='Power spectrum Y')
        ax[1].plot(frq, 2.0/N * np.abs(y_z[0:N/2]), 'g', label='Power spectrum Z')
        ax[1].plot(frq, 2.0/N * np.abs(y_max[0:N/2]), 'y', label='Maximum Power spectrum')
        ax[1].plot(peak_tupel[0], peak_tupel[1], 'rx', label='Peak')

        #ax[1].text(0.8, 0, 'RR = %d' % rr)
        anchored_text = AnchoredText('RR = %f' % rr, loc=4)
        ax[1].add_artist(anchored_text)

        ax[1].set_xlabel('Frequency in Hz')
        ax[1].set_ylabel('Power spectrum density')
        ax[1].set_xlim([0.1, 0.6])
        ax[1].legend(loc='best', fontsize=9)
        ax[1].set_title("Power spectra - Marked peak and calculated RR", fontsize="medium")

        # Tight layout often produces nice results
        # but requires the title to be spaced accordingly
        fig.tight_layout()
        fig.subplots_adjust(top=0.88)
        #plt.show()

    def visualise_filtered_signal_combined(self, filtered_array_x, filtered_array_y, filtered_array_z):
        array_len = range(0, len(filtered_array_x))

        fig, ax = plt.subplots(1, sharex=True, sharey=True)

        # Plot all axes in one plot
        fig.suptitle('Bandpass filtered Signal (0.2-0.45hz) - X-, Y-, Z-Axis combined')
        ax.plot(array_len, filtered_array_x, 'r', label='X-Axis')
        ax.plot(array_len, filtered_array_y, 'b', label='Y-Axis')
        ax.plot(array_len, filtered_array_z, 'g', label='Z-Axis')

        plt.xlabel('Time in points  (50dp/sec)')
        plt.ylabel('Signal value')
        plt.legend(loc='best', fontsize=9)
        #plt.show()


    def visualise_filtered_signal_separate(self, filtered_array_x, filtered_array_y, filtered_array_z):
        array_len = range(0, len(filtered_array_x))

        # Plt all three Axis in one Figure using same X- and Y_x- Axis
        fig, ax = plt.subplots(3, sharex=True, sharey=True)
        fig.suptitle('Bandpass filtered signal (0.2-0.45hz) separate for all axes', fontsize='large')
        #fig.tight_layout()

        xl, = ax[0].plot(array_len, filtered_array_x, 'r')
        ax[0].set_title('Bandpass filtered signal - X-Axis', fontsize='medium')

        yl, = ax[1].plot(array_len, filtered_array_y, 'b')
        ax[1].set_title('Bandpass filtered signal - Y-Axis', fontsize='medium')

        zl, = ax[2].plot(array_len, filtered_array_z, 'g')
        ax[2].set_title('Bandpass filtered signal - Z-Axis', fontsize='medium')

        plt.xlabel('Time in points  (50dp/sec)')
        plt.ylabel('Signal value')
        ax[0].legend((xl, yl, zl), ('X-Axis', 'Y-Axis', 'Z-Axis'), loc='upper right', fontsize=9)

        #plt.show()


    def visualise_filter_design(self, b, a, sample_rate):
        # Plot the frequency response for a few different orders.
        plt.figure(1)
        plt.clf()

        w, h = signal.freqz(b, a, worN=2000)
        plt.plot((sample_rate * 0.5 / np.pi) * w, abs(h), label='Butterworth order 4')

        plt.plot([0, 0.5 * sample_rate], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
        plt.title('Bandpass filter design - Butterworth order 4 - 0.2 - 0.45Hz')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain')
        plt.xlim([0, 1])
        plt.ylim([0, 1.1])
        plt.grid(True)
        plt.legend(loc='best', fontsize=9)

        #plt.show()


    def visualise_power_spectrum_combined(self, frq, y_x, **kwargs):
        y_y = kwargs.get('y_y', None)
        y_z = kwargs.get('y_z', None)
        y_max = kwargs.get('y_max', None)
        rr = kwargs.get('rr', None)
        peak_tupel = kwargs.get('peak_tupel', None)

        N = y_x.size

        #plt.xkcd() #HAHA! COMIC STYLE - XKCD
        fig, ax = plt.subplots(1)
        fig.suptitle('Power spectra for X-, Y-, Z-Axis', fontsize="large")

        # plotting the spectrum
        ax.plot(frq,  2.0/N * np.abs(y_x[0:N/2]), 'r', label='Power spectrum X')
        if y_y is not None:
            ax.plot(frq, 2.0/N * np.abs(y_y[0:N/2]), 'b', label='Power spectrum Y')
        if y_z is not None:
            ax.plot(frq, 2.0/N * np.abs(y_z[0:N/2]), 'g', label='Power spectrum Z')
        if y_max is not None:
            ax.plot(frq, 2.0/N * np.abs(y_max[0:N/2]), 'y', label='Maximum Power spectrum')

        if peak_tupel is not None:
            ax.plot(peak_tupel[0], peak_tupel[1], 'rx', label='Peak')
        if rr is not None:
            anchored_text = AnchoredText('RR = %f' % rr, loc=4)
            plt.add_artist(anchored_text)

        plt.xlabel('Frequency in Hz')
        plt.ylabel('Power spectrum density')
        plt.xlim([0.1, 0.6])
        plt.legend(loc='best', fontsize=9)
        #plt.show()


    def visualise_peak(self, frq, y_max, peak_tupel, **kwargs):
        y_x = kwargs.get('y_x', None)
        y_y = kwargs.get('y_y', None)
        y_z = kwargs.get('y_z', None)
        rr = kwargs.get('rr', None)

        N = y_max.size

        #plt.xkcd() #HAHA! COMIC STYLE - XKCD
        fig, ax = plt.subplots(1)
        fig.suptitle('Maximum power spectrum with peak.', fontsize="large")

        # plotting the spectrum
        if y_y is not None:
            ax.plot(frq,  2.0/N * np.abs(y_x[0:N/2]), 'r', label='Power spectrum X')
        if y_y is not None:
            ax.plot(frq, 2.0/N * np.abs(y_y[0:N/2]), 'b', label='Power spectrum Y')
        if y_z is not None:
            ax.plot(frq, 2.0/N * np.abs(y_z[0:N/2]), 'g', label='Power spectrum Z')

        ax.plot(frq, 2.0/N * np.abs(y_max[0:N/2]), 'y', label='Maximum Power spectrum')
        ax.plot(peak_tupel[0], peak_tupel[1], 'rx', label='Peak')

        text = 'Peak = %f ; %f' %(peak_tupel[0], peak_tupel[1])
        #ax.add_artist(anchored_text)
        if rr is not None:
            text += '\n' + 'RR = %f' %rr
        anchored_text = AnchoredText(text, loc=4, prop=dict(color='Black', size=9))
        ax.add_artist(anchored_text)

        ax.set_xlabel('Frequency in Hz')
        ax.set_ylabel('Power spectrum density')
        ax.set_xlim([0.1, 0.6])
        plt.legend(loc='best', fontsize=9)
        #plt.show()