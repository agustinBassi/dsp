"""This module has all needed to work with Comb Filter.

Optionally the module has __repr__() and __str__() methods.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging

import scipy.signal as signal


class CombFilter:
    """TODO: Comment here
    """
    
    def __init__(self, delay, scale):
        self.__delay = delay
        self.__scale = scale
        

    def set_parameters (self, delay, scale):
        self.__delay = delay
        self.__scale = scale
        self.__numerator = [1] + (self.__delay - 1) * [0] + [self.__scale]
        
        logging.debug('Setting new parameters(delay = %d samples, ' \
                      'scale = %.2f' % (self.__delay, self.__scale)) 

    def __repr__(self):
        return ("{'delay': '%d', 'scale: '%.2f'}"  %
                (self.__delay, self.__scale)) 

    def __str__(self):
        return str('CombFilter(delay = %d samples, scale = %.2f)' %
                (self.__delay, self.__scale))

    def get_response_in_frecuency (self):
        logging.debug("Calculating response in frecuency of comb filter")
        
        frequencies, response_in_frequency = signal.freqz(self.__numerator, 
                                                          self.__denominator)
        return frequencies, response_in_frequency

def test_comb_filter_class():
    from filters_view import FiltersView

    COMB_DELAY        = 8
    COMB_SCALE_FACTOR = 1

    comb_filter = CombFilter(COMB_DELAY, COMB_SCALE_FACTOR)

    print (str(comb_filter))
    print (repr(comb_filter))

    freqs, response_in_freq = comb_filter.get_response_in_frecuency()

    FiltersView.plot_comb_filter(freqs, response_in_freq)

    comb_filter.set_parameters(5, 0.7)

    freqs, response_in_freq = comb_filter.get_response_in_frecuency()

    FiltersView.plot_comb_filter(freqs, response_in_freq)
    

    

