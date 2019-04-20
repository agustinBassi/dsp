
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
        step = int( ((self.__max_f - self.__min_f)/signal_period) * 2 )
        # the times that signal triangle waveform will be executed is related to 
        # the FS/signal period multiplied by the duration in seconds of the original signal
        times = int((fs/signal_period) * (lenght/fs))
        # This is internal function that will create the signal, from the min value
        # to max value. It's a generator to make it memory efficient.
        def generator():
            # The signal periods
            for i in range (times):
                # Times which signal increase the values dictated by step
                for j in range(self.__min_f, self.__max_f, step):
                    yield j
                # Times which signal decrrease the values dictated by step
                for j in range(self.__max_f*-1, self.__min_f*-1, step):
                    yield j * -1
        # Call the generator of the function and create a list from it
        triangle_signal = list(generator())
        # Trim triangle signal to lenght of original signal
        triangle_signal = triangle_signal[:lenght]
        # return triangle singla.
        return triangle_signal

    def apply_filter(self, x, triangle_signal, fs):
        # equation coefficients
        f1 = 2 * math.sin((math.pi * triangle_signal[0])/fs)
        # size of band pass filter
        q1 = 2 * self.__damping
        # initialize filters arrays with zero values
        yh = numpy.zeros(len(x))
        yb = numpy.zeros(len(x))
        yl = numpy.zeros(len(x))
        # assign first values
        yh[0] = x[0]
        yb[0] = f1 * yh[0]
        yl[0] = f1 * yb[0]

        print("- F1: {}".format(f1))
        print("- Q1: {}".format(q1))
        
        print("- Len triangle: {}".format(len(triangle_signal)))

        coefficients = []

        for n in range (1, len(x)):
            yh[n] = x[n] - yl[n-1] - (q1 * yb[n - 1])
            yb[n] = (f1 * yh[n]) + yb[n - 1]
            yl[n] = (f1 * yb[n]) + yl[n - 1]
            # recalculate equation coefficients
            f1 = 2 * math.sin((math.pi * triangle_signal[n])/fs)
            coefficients.append(f1)

        print("- Len yh: {}".format(len(yh)))
        print("- Len yb: {}".format(len(yb)))
        print("- Len yl: {}".format(len(yl)))

        # normalize signal
        max_yb = numpy.amax(yb)
        print("- Max yb: {}".format(max_yb))

        
        normalized_relation = WahWahFilter.MAX_INT16_VALUE/max_yb
        print("Scale relation from int32 to YB is: {}".format(normalized_relation))

        # adapt wahwah signal to original signal amplitude
        # normalized_yb = yb
        normalized_yb = [int(x * normalized_relation) for x in yb]

        npa = array(normalized_yb)

        return npa, coefficients

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
    MIN_F = 500
    MAX_F = 3000
    WAH_F = 2.5
    # Program settings
    ORIGINAL_WAV = "/home/juan.bassi/personalProjects/dsp_controller/wavs/guitars.wav"
    WAHWAH_WAV = "/home/juan.bassi/personalProjects/dsp_controller/wavs/guitars_modified.wav"

    # WahWahFilter.play_audio(ORIGINAL_WAV)

    wahwah = WahWahFilter(DAMPING, MIN_F, MAX_F, WAH_F)

    fs, original_signal = WahWahFilter.convert_wav_to_raw(ORIGINAL_WAV)

    triangle_signal = wahwah.create_triangle_waveform(len(original_signal), fs)

    WahWahFilter.play_audio(ORIGINAL_WAV)

    # wahwah.plot_triangle_waveform(original_signal)
    # wahwah.plot_triangle_waveform(triangle_signal)

    wahwah_signal, coefficients = wahwah.apply_filter(original_signal, triangle_signal, fs)

    # wahwah.plot_triangle_waveform(coefficients)
    # wahwah.plot_wahwah_signals(triangle_signal, coefficients)

    WahWahFilter.save_raw_to_wav(wahwah_signal, WAHWAH_WAV, fs)

    WahWahFilter.play_audio(WAHWAH_WAV)
    # playsound(WAHWAH_WAV)
    

if __name__ == "__main__":
    main()


# def create_triangle_waveform_old(self, period, amplitude):
#     section = period // 4

#     # pone sentido a la direccion de la onda
#     for direction in (1, -1):
#         # por una seccion pone valores positivos (o crecientes mejor dicho)
#         for i in range(section):
#             yield i * (amplitude / section) * direction
#         # por una seccion pone valores negativos (o decrecientes mejor dicho)    
#         for i in range(section):
#             yield (amplitude - (i * (amplitude / section))) * direction

# def create_triangle_waveform2(self):
#     min_f = 500
#     max_f = 3000
#     wah_f = 2000
#     lenght = 220500
#     fs = 44100

#     signal_period = fs/wah_f

#     step = int((max_f-min_f)/signal_period)
#     step *= 2

#     # times = int(1/((lenght/fs)/wah_f))
#     times = int((fs/signal_period) * (lenght/fs)) # int((lenght/fs) * signal_period)
    
#     for i in range (times):
#         for j in range(min_f, max_f, step):
#             yield j
#         for j in range(max_f*-1, min_f*-1, step):
#             yield j * -1

#     #TODO: Trimear la señal al lenght