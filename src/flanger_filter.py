"""
TODO: Explain how the module works
"""
import logging
import os
import math

import numpy as np


class FlangerFilter:
    """TODO: Comment here
    """

    def __init__(self, fs, max_delay, scale, rate):
        self.__fs = fs
        self.__max_delay = max_delay
        self.__scale = scale
        self.__rate = rate

    def __repr__(self):
        return ("{'fs': '%d', 'max_delay: '%.4f'," \
                "'scale': '%.2f', 'rate': '%f'}" %
                (self.__fs, self.__max_delay, self.__scale, self.__rate))

    def __str__(self):
        return ('FlangerFilter(fs = %d hz, max_delay = %.4f seg, ' \
                'scale = %.2f, rate = %.2f)' 
                % (self.__fs, self.__max_delay, self.__scale, self.__rate))

    def apply_filter(self, raw_signal):
        max_index = len(raw_signal)

        sin_ref = lambda index : math.sin(2 * math.pi * index * 
                                         (self.__rate/self.__fs))
        
        max_delay_sample = round(self.__max_delay * self.__fs)

        flanger_signal = np.copy(raw_signal)

        for i in range ((max_delay_sample + 1), len(flanger_signal)):
            #current_sin = math.fabs(math.sin(2 * math.pi * i * 
             #                               (self.__rate/self.__fs)))
            current_sin = sin_ref(i)

            current_delay = max_delay_sample * current_sin

            flanger_signal[i] = int((self.__scale * raw_signal[i]) + 
                                (self.__scale * 
                                raw_signal[i - int(current_delay)]))

        return flanger_signal


def test_flanger_filter_class():
    from wav_file import WavFile

    
    ORIGINAL_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz.wav"
    MODIFIED_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz_modified.wav"

    FS = 44100
    MAX_DELAY = 0.004
    SCALE = 0.7
    RATE = 1.2

    flanger_filter = FlangerFilter(FS, MAX_DELAY, SCALE, RATE)

    logging.debug("Testing FlangerFilter.__repr__(): %s" % 
                  repr(flanger_filter))

    logging.debug("Testing FlangerFilter.__str__(): %s" % 
                  str(flanger_filter))

    original_signal = WavFile.convert_to_raw(ORIGINAL_WAV)

    flanger_signal = flanger_filter.apply_filter(original_signal)

    WavFile.save_raw_into_wav(flanger_signal, MODIFIED_WAV)

    WavFile.play(MODIFIED_WAV)