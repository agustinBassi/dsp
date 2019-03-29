"""This module has all needed to plot filters signals with pyplot library.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging

import matplotlib.pyplot as plt

class FiltersView:
    """Plot filters with pyplot and others related functions.

    ===============   =============
    Location String   Location Code
    ===============   =============
    'best'            0
    'upper right'     1
    'upper left'      2
    'lower left'      3
    'lower right'     4
    'right'           5
    'center left'     6
    'center right'    7
    'lower center'    8
    'upper center'    9
    'center'          10
    ===============   =============

    # styles
    plt.plot(x, y_1, '-.', color="#333333")
    plt.plot(x, y_2, '--', color="#999999")
    plt.plot(x, y_3, '-', color="#aaaaaa")

    # save an image of graphic
    plt.save('plot_comb_filter.png', dpi=100)
    """

    @staticmethod
    def plot_single_signal(single_signal, title="Graph title", 
                           label_x="Text X", label_y="Text Y"):
        
        logging.debug("Plot single signal - " \
                      "title: %s, Label X: %s, Label Y: %s, " %                          "limit min: %d, limit_max: %d" %
                      (title, label_x, label_y))

        # plot signals to graphic
        plt.plot(single_signal)
        # set labels to axes
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        # optionally save an image of graphic
        #plt.save('plot_comb_filter.png', dpi=100)
        plt.show()


    @staticmethod
    def plot_multi_signals(*signals, title="Graph title", label_x="Text X", 
                            label_y="Text Y", limit_min=0, limit_max=0):

        if (len(signals) > 0):
            logging.debug("Showing generic plot. Amount of signals: %d, " \
                          "title: %s, Label X: %s, Label Y: %s, " \
                          "limit min: %d, limit_max: %d" %
                          (len(signals), title, label_x, label_y, 
                          limit_min, limit_max))
            # plot signals to graphic
            for signal in signals:
                plt.plot(signal)
            # set labels to axes
            plt.title(title)
            plt.xlabel(label_x)
            plt.ylabel(label_y)
            # set limits only if they are passed as argument
            if (limit_max > 0):
                plt.xlim(limit_min, limit_max)
            # show figure
            plt.show()
        else:
            logging.error("At least one signal must be passed to plot it.")


    @staticmethod
    def plot_comb_filter(frequencies, response_in_frequency, 
                         title="Comb filter response in frecuency", 
                         label_x="Time", label_y="Amplitude",
                         ref_1="Frecuency", ref_2="Response in frecuency",
                         refs_location="best"):

        logging.debug("Showing Comb filter plot - " \
                      "title: %s, Label X: %s, Label Y: %s, " %
                      (title, label_x, label_y))

        # plot signals to graphic
        plt.plot(frequencies)
        plt.plot(response_in_frequency)
        # set labels to axes
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1, ref_2], loc=refs_location)
        # show figure
        plt.show()


    @staticmethod
    def plot_flanger_signals(original_signal, flanger_signal, 
                            title="Flanger signal response", 
                            label_x="Time", label_y="Amplitude",
                            ref_1="Original signal", ref_2="Flanger signal",
                            refs_location="best"):

        logging.debug("Plot flanger signal - " \
                      "title: %s, Label X: %s, Label Y: %s, " %
                      (title, label_x, label_y))
                    
        # plot signals to graphic
        plt.plot(original_signal)
        plt.plot(flanger_signal)
        # set legends to graph
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1, ref_2], loc=refs_location)
        # show figure
        plt.show()


def test_filters_view_class():

    from wav_file import WavFile
    from flanger_filter import FlangerFilter

    ORIGINAL_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz.wav"
    MODIFIED_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz_modified.wav"

    FS = 44100
    MAX_DELAY = 0.004
    SCALE = 0.7
    RATE = 1.2

    flanger_filter = FlangerFilter(FS, MAX_DELAY, SCALE, RATE)

    original_signal = WavFile.convert_to_raw(ORIGINAL_WAV)

    flanger_signal = flanger_filter.apply_filter(original_signal)

    FiltersView.plot_flanger_signals(original_signal, flanger_signal)

    #FiltersView.plot_multi_signals([original_signal, flanger_signal])

    #FiltersView.plot_raw_signal(raw_list, "Wav", "Tiempo", "Amplitud")
    #WavFile.save_raw_into_wav(raw_list, MODIFIED_WAV)
    #WavFile.play(MODIFIED_WAV)
