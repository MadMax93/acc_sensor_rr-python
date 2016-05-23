# acc_sensor_rr-python
Python implementation for extracting the respiration rate from three-dimentional-sensor data. It provides methods for plotting the results through Matplotlib. This programm got developed for my bachelor thesis.
The used digital signal processing algorithms are the following:
* Butterworth bandpass filter
  * Default: order = 4, low cutoff frequency = 0.2Hz, High cutoff frequency = 0.4Hz
* Fast Fourier Transformation
* Peakdetektion
* Calculation of the respiration rate

###Required Packages:
* NumPy
* Matplotlib
* SciPy Lib
* PeakUtils by Lucas Hermann Negri - http://pythonhosted.org/PeakUtils/ - requires Python 3.4.x
* Ipython - for visualising the plots

###Useful Information:
* Inputfile should have the following format: 
  * Timestamp, X-Value, Y-Value, Z-Value
* Start of the programm is the Main.py file
* Parameters for the sample rate, low- and high cutoff frequencys for the Bandpassfilter can be changed in the main file.
* Main plot through the Method "Visualization.visualise_signals_and_xyz_and_maximum_power_spectrum()"

###Licence:
The MIT License (MIT)

Copyright (c) 2016 Maximilian Kurscheidt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
