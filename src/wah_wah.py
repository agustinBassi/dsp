
import logging
import os
import math

import matplotlib.pyplot as plt
import numpy
from numpy import ndarray as np
import scipy.signal as signal
from scipy.io import wavfile
from numpy  import array
from playsound import playsound

class WahWahFilter():

    # For limit the amplitude of wah wah signal for int16 wav file format
    MAX_INT16_VALUE = 32000

    def __init__(self, damping, min_f, max_f, wah_f):
        self.__damping = damping
        self.__min_f = min_f
        self.__max_f = max_f
        self.__wah_f = wah_f

    def __repr__(self):
        return ("{'damping': '%f', 'min_f': '%d','max_f': '%d','wah_f': '%d'}" %
                (self.__damping, self.__min_f, self.__max_f, self.__wah_f))

    def __str__(self):
        return (
            "WahWahFilter(damping = %f, min_f = %d, max_f = %d, wah_f = %d)" %
             (self.__damping, self.__min_f, self.__max_f, self.__wah_f))

    def create_triangle_waveform(self, lenght, fs):
        # establish signal period from fs and wah wah frecuency
        signal_period = fs/self.__wah_f
        # steps which triangle signal will do, considering the minummum
        # and max value that it has to reach. Also signal period is taken in account 
        # and finally it is multiplied by 2, because the signal will have to 
        # increase and decrease it's value in 1 signal period
        step = float( ((self.__max_f - self.__min_f)/signal_period) * 2 )
        # This is internal function that will create the signal, from the min value
        # to max value. It's a generator to make it memory efficient.
        def generator():
            index = 0
            while index < lenght:
                signal_value = self.__min_f
                while signal_value < self.__max_f:
                    signal_value += step
                    index += 1
                    yield signal_value
                
                while signal_value > self.__min_f:
                    signal_value -= step
                    index += 1
                    yield signal_value

        # Call the generator of the function and create a list from it
        triangle_signal = list(generator())
        # Trim triangle signal to lenght of original signal
        triangle_signal = triangle_signal[:lenght]
        # return triangle singla.
        return triangle_signal

    def apply_filter(self, original_signal, fs):
        # Create triangle signal
        cuttoff_frequencies = self.create_triangle_waveform(len(original_signal), fs)
        # equation coefficients
        f1 = 2 * math.sin((math.pi * cuttoff_frequencies[0])/fs)
        # size of band pass filter
        q1 = 2 * self.__damping
        # initialize filters arrays with zero values
        highpass = numpy.zeros(len(original_signal))
        bandpass = numpy.zeros(len(original_signal))
        lowpass = numpy.zeros(len(original_signal))
        # assign first values
        highpass[0] = original_signal[0]
        bandpass[0] = f1 * highpass[0]
        lowpass[0] = f1 * bandpass[0]
        # loop to reach the lenght of original signal
        for n in range (1, len(original_signal)):
            highpass[n] = original_signal[n] - lowpass[n-1] - (q1 * bandpass[n - 1])
            bandpass[n] = (f1 * highpass[n]) + bandpass[n - 1]
            lowpass[n] = (f1 * bandpass[n]) + lowpass[n - 1]
            # recalculate equation coefficients
            f1 = 2 * math.sin((math.pi * cuttoff_frequencies[n])/fs)
        # Obtain the max value of YB
        max_bandpass = numpy.amax(bandpass)
        # Establish a relation between max YB value and INT 16 max value
        normalized_relation = WahWahFilter.MAX_INT16_VALUE/max_bandpass
        # adapt wahwah signal to original signal amplitude
        normalized_bandpass = [int(x * normalized_relation) for x in bandpass]
        # create an scipy array to reproduce it then
        wahwah_signal = array(normalized_bandpass)
        
        #############################
        # STATICS
        print("- F1: {}".format(f1))
        print("- Q1: {}".format(q1))
        print("- Len cuttoff freqs: {}".format(len(cuttoff_frequencies)))
        print("- Len highpass: {}".format(len(highpass)))
        print("- Len bandpass: {}".format(len(bandpass)))
        print("- Len lowpass: {}".format(len(lowpass)))
        print("- Max bandpass: {}".format(max_bandpass))
        print("- Scale relation: {}".format(normalized_relation))
        #############################
        
        return wahwah_signal

    def plot_triangle_waveform(self, triangle_signal,
                         title="Triangle waveform",
                         label_x="Samples", label_y="Frecuency (Hz)",
                         ref_1="Response in frecuency", refs_location="best"):

        # plot signals to graphic
        plt.plot(triangle_signal)
        # set labels to axes
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1], loc=refs_location)
        # show figure
        plt.show()

    def plot_wahwah_signals(self, original_signal, wahwah_signal,
                             title="Wahwah signal response",
                             label_x="Time", label_y="Amplitude",
                             ref_1="Original signal", ref_2="Wahwah signal",
                             refs_location="best"):

        # plot signals to graphic
        plt.plot(original_signal)
        plt.plot(wahwah_signal)
        # set legends to graph
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1, ref_2], loc=refs_location)
        # show figure
        plt.show()

    @staticmethod
    def save_raw_to_wav(raw_data, wav_file, fs):
        print("\n==================================================\n")
        print("Converting raw data to wav file: %s" % wavfile)
        wavfile.write(wav_file, fs, raw_data.astype(numpy.dtype('i2')))
        print("\n==================================================\n")

    @staticmethod
    def convert_wav_to_raw(wav_file):
        print("\n==================================================\n")
        data = None
        fs, data = wavfile.read(wav_file)
        print("Creating raw data from wav file: %s - FS: %d" % (wavfile, fs))
        print("\n==================================================\n")

        return fs, data

    @staticmethod
    def play_audio(audio_file):
        print("\n==================================================\n")
        os.system("aplay %s" % audio_file)
        print("\n==================================================\n")

def main():
    # Filter settings
    DAMPING = 0.05
    MIN_F = 300
    MAX_F = 4000
    WAH_F = 0.4
    # Program settings
    ORIGINAL_WAV = "/home/juan.bassi/personalProjects/dsp_controller/wavs/guitars.wav"
    WAHWAH_WAV = "/home/juan.bassi/personalProjects/dsp_controller/wavs/guitars_modified.wav"

    # WahWahFilter.play_audio(ORIGINAL_WAV)

    wahwah = WahWahFilter(DAMPING, MIN_F, MAX_F, WAH_F)

    fs, original_signal = WahWahFilter.convert_wav_to_raw(ORIGINAL_WAV)

    # triangle_signal = wahwah.create_triangle_waveform(len(original_signal), fs)
    # wahwah.plot_triangle_waveform(triangle_signal)

    wahwah_signal = wahwah.apply_filter(original_signal, fs)

    wahwah.plot_wahwah_signals(original_signal, wahwah_signal)

    WahWahFilter.save_raw_to_wav(wahwah_signal, WAHWAH_WAV, fs)

    WahWahFilter.play_audio(WAHWAH_WAV)
    

if __name__ == "__main__":
    main()