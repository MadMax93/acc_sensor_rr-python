__author__ = 'Maximilian Kurscheidt @MadMax93'

import math

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import peakutils
from peakutils.plot import plot as pplot
from scipy.fftpack import fft, rfft, fftshift

class Signalprocessing(object):
    def butter_bandpass_design(self, low_cut, high_cut, sample_rate, order=4):
        """
        Defines the Butterworth bandpass filter-design
        :param low_cut: Lower cut off frequency in Hz
        :param high_cut: Higher cut off frequency in Hz
        :param sample_rate: Sample rate of the signal in Hz
        :param order: Order of the filter-design
        :return: b, a : ndarray, ndarray - Numerator (b) and denominator (a) polynomials of the IIR filter. Only returned if output='ba'.

        """
        nyq = 0.5 * sample_rate
        low = low_cut / nyq
        high = high_cut / nyq
        b, a = signal.butter(order, [low, high], btype='band')

        return b, a


    def butter_bandpass_filter(self, signal_array, low_cut, high_cut, sample_rate, order=4):
        """
        Apply's the filter design on the signal_array.
        :param signal_array: signal, which should get filtered - as ndarray
        :param low_cut: Lower cut off frequency in Hz
        :param high_cut: Higher cut off frequency in Hz
        :param sample_rate: Sample rate of the signal in Hz
        :param order: Order of the filter-design
        :return: ndarray - The filtered output, an array of type numpy.float64 with the same shape as signal_array.
        """
        b, a = self.butter_bandpass_design(low_cut, high_cut, sample_rate, order=order)
        y = signal.filtfilt(b, a, signal_array)

        return y


    def fast_fourier_transformation(self, signal_array, sample_rate):
        """
        Apply's the Fast Furier Transformation. This transforms the signal into an power spectrum in frequency domain.
        :param signal_array: signal as ndarray
        :param sample_rate: Sample rate of the signal in Hz
        :return: yf : complex ndarray - Results of the FFT
                 xf : ndarray - frequency parts in an equally interval
        """
        N = signal_array.size  # number of sample points
        T = 1 / sample_rate  # sample spacing
        yf = fft(signal_array)

        # xf = fftfreq(N, T)  # for all frequencies
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)  # for positive frequencies only

        return yf, xf

    def power_of_the_spectrum(self, yf):
        """
        Calculate the power of the power spectrum.
        :param yf: complex ndarray - Complex results of the FFT
        :return: power of the power spectrum
        """
        power = np.power(yf.real, 2) + np.power(yf.imag, 2)

        return power


    def maximum_power_of_xyz_spectrum(self, power_x, power_y, power_z, sample_rate):
        """
        Calculate the maximum power spectrum of the power spectra xyz.
        :param power_x: power of x
        :param power_y: power of y
        :param power_z: power of z
        :param sample_rate: Sample rate of the signal in Hz
        :return: maximum_power_spectrum : ndarray - maximum power spectrum
                 xf : ndarray - frequency parts in an equally interval
        """
        maximum_power_spectrum = power_x + power_y + power_z

        N = maximum_power_spectrum.size
        #maximum_power_spectrum = 2.0 / N * np.abs(sum[0:N / 2])

        T = 1 / sample_rate
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N / 2)  # for positiv frequencies only

        return maximum_power_spectrum, xf


    def positive_power_spectrum_for_peak_detection(self, power_spectrum):
        """
        Returns positive power of the complete spectrum
        :param power_spectrum: complete power spectrum with positive and negative parts
        :return: positive power of the spectrum
        """
        N = power_spectrum.size
        positive_power = 2.0 / N * np.abs(power_spectrum[0:N / 2])

        return positive_power


    def find_peak_and_frequency(self, power_max, xf_max):
        """
        Peak detection with the PeakUtils library
        :param power_max: ndarray - maximum power spectrum
        :param xf_max: ndarray - frequency parts in an equally interval
        :return: peak: ndarray - a pair of power and frequency
        """
        # @todo if more than one maximum find biggest one - check for none

        indexes = peakutils.indexes(power_max, thres=0.9, min_dist=30)
        peak = np.hstack((xf_max[indexes], power_max[indexes]))

        return peak


    def calculate_rr_from_power_spectrum(self, peak_tupel):
        """
        Calculate the respiration rate from the power spectrum.
        :param peak_tupel: ndarray - peak tupel of frequency and power
        :return: respiration rate
        """

        # rr = round(peak_tupel[0] * 60)  # rounded
        # rr = math.ceil(peak_tupel[0] * 60)  # rounded up
        rr = peak_tupel[0] * 60
        return rr
