"""This module has all needed to work with Flanger Filter.

To use this module, first create an instance for it and then 
call the function apply_filter() passing to it a raw signal. 
This signal could be a wav file converted to a numpy array.

Optionally the module has __repr__() and __str__() methods.

Finally, it could be necessary to obtain the delay signal 
applied to original signal, so, the method get_delay_signal()
would be called.

Copyright: Agustin Bassi, 2019.
License: BSD.
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

    def set_parameters (self, fs, max_delay, scale, rate):
        self.__fs = fs
        self.__max_delay = max_delay
        self.__scale = scale
        self.__rate = rate
        logging.debug('Setting new parameters(fs = %d hz, ' \
                      'max_delay = %.4f seg, scale = %.2f, rate = %.2f)' 
                      % (self.__fs, self.__max_delay, 
                         self.__scale, self.__rate))

    def __repr__(self):
        return ("{'fs': '%d', 'max_delay: '%.4f'," \
                "'scale': '%.2f', 'rate': '%f'}" %
                (self.__fs, self.__max_delay, self.__scale, self.__rate))

    def __str__(self):
        return ('FlangerFilter(fs = %d hz, max_delay = %.4f seg, ' \
                'scale = %.2f, rate = %.2f)' 
                % (self.__fs, self.__max_delay, self.__scale, self.__rate))

    def apply_filter(self, raw_signal):
        """Apply flanger signal to raw signal.

        All parameters about the filter should be confired before
        use this function.
        """
        # Create a lambda to call it when process delay later
        sinus_reference = lambda index : math.sin(2 * math.pi * index * 
                                                 (self.__rate/self.__fs))
        # Convert delay in ms to max delay in samples
        max_delay_sample = round(self.__max_delay * self.__fs)
        # Copy original signal into new one that will be returned
        flanger_signal = np.copy(raw_signal)

        try:
            # Iterate over the signal, calculate each delay to be applied
            # and then add it to original signal
            for i in range ((max_delay_sample + 1), len(flanger_signal)):
                current_sinus = sinus_reference(i)

                current_delay = max_delay_sample * current_sinus

                flanger_signal[i] = int((self.__scale * raw_signal[i]) + 
                                        (self.__scale * 
                                        raw_signal[i - int(current_delay)]))
            logging.debug("Flanger filter applied to signal")
        except:
            logging.error("Error while Flanger filter applied to signal")

        return flanger_signal

    def get_delay_signal(self, raw_signal):
        # Create a lambda to call it when process delay later
        sinus_reference = lambda index : math.sin(2 * math.pi * index * 
                                                 (self.__rate/self.__fs))
        # Convert delay in ms to max delay in samples
        max_delay_sample = round(self.__max_delay * self.__fs)
        # Create delay signal as empty list
        delay_signal = []

        try:
            # Fill first elements of array with zeros
            for i in range(0, (max_delay_sample + 1)):
                delay_signal.append(0)
            # Fill with current delay value
            for i in range ((max_delay_sample + 1), len(raw_signal)):
                delay_signal.append(sinus_reference(i) * max_delay_sample)
            logging.debug("Flanger delay signal created correctly")
        except:
            logging.error("Error while creating flanger delay signal")

        return delay_signal

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

    #flanger_signal = flanger_filter.apply_filter(original_signal)

    #WavFile.save_raw_into_wav(flanger_signal, MODIFIED_WAV)

    #WavFile.play(MODIFIED_WAV)

    #flanger_delay_signal = flanger_filter.get_delay_signal(original_signal)

    #flanger_filter.set_parameters(472291, .125, 0.57, 87)