"""This module has all needed to plot filters signals with pyplot library.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging

import matplotlib.pyplot as plt

class FiltersView:
    """Plot filters with pyplot and others related functions.

    TODO: Se podria hacer una funcion de plot que reciba
    una lista de parametros y en funcion de los mismos los 
    vaya ploteando. De esta manera se necesitaria solo una funcion 
    de plot.
    """

    @staticmethod
    def plot_comb_filter(freqs, resps_in_freq, title, labelx, labely):
        # plot signals to graphic
        plt.plot(freqs)
        plt.plot(resps_in_freq)
        # set labels to axes
        plt.title(title)
        plt.xlabel(labelx)
        plt.ylabel(labely)
        # optionally save an image of graphic
        #plt.save('plot_comb_filter.png', dpi=100)
        plt.show()


    @staticmethod
    def plot_raw_signal(raw_signal, title, labelx, labely):
        # plot signals to graphic
        plt.plot(raw_signal)
        # set labels to axes
        plt.title(title)
        plt.xlabel(labelx)
        plt.ylabel(labely)
        # optionally save an image of graphic
        #plt.save('plot_comb_filter.png', dpi=100)
        plt.show()


    @staticmethod
    def plot_flanger_signals(raw_signal, flanger_signal, 
                            title, labelx, labely):
        # plot signals to graphic
        plt.plot(raw_signal)
        plt.plot(flanger_signal)
        # set labels to axes
        plt.title(title)
        plt.xlabel(labelx)
        plt.ylabel(labely)
        # optionally save an image of graphic
        #plt.save('plot_comb_filter.png', dpi=100)
        plt.show()
    

def test_filters_view_class():
    from wav_file import WavFile
    from flanger_filter import FlangerFilter

    ORIGINAL_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz.wav"
    MODIFIED_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz_modified.wav"


    FIGURE1_TITLE   = "Respuesta en frecuencia filtro comb"
    FIGURE1_LABEL_X = "Frecuencia"
    FIGURE1_LABEL_Y = "Amplitud"

    FIGURE2_TITLE   = "Senial WAV"
    FIGURE2_LABEL_X = "Tiempo"
    FIGURE2_LABEL_Y = "Amplitud"

    Color = {
        "RED"  : 'r',
        "GREEN": 'g',
        "BLUE" : 'b'
    }

    ORIGINAL_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz.wav"
    MODIFIED_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz_modified.wav"

    FS = 44100
    MAX_DELAY = 0.004
    SCALE = 0.7
    RATE = 1.2

    flanger_filter = FlangerFilter(FS, MAX_DELAY, SCALE, RATE)

    original_signal = WavFile.convert_to_raw(ORIGINAL_WAV)

    flanger_signal = flanger_filter.apply_filter(original_signal)

    FiltersView.plot_flanger_signals(original_signal, flanger_signal, 
                                    "title", "eje x", "eje y")

    #FiltersView.plot_raw_signal(raw_list, "Wav", "Tiempo", "Amplitud")
    #WavFile.save_raw_into_wav(raw_list, MODIFIED_WAV)
    #WavFile.play(MODIFIED_WAV)
