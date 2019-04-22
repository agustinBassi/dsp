import logging
import os
import math
import os
import json
import configparser

from numpy import ndarray
import scipy.signal as signal
from scipy.io import wavfile
import numpy as numpy
from numpy import array as np_array


class Configuration:
    """TODO: Comment here
    """

    def __init__(self, welcome_message, wav_original, wav_modified):
        self.__welcome_message = welcome_message
        self.__wav_original = wav_original
        self.__wav_modified = wav_modified

    def __repr__(self):
        return ("{'welcome_message': '%s', 'wav_original': '%s', "
                "'wav_modified': '%s'}" % (self.__welcome_message,
                                           self.__wav_original, self.__wav_modified))

    def __str__(self):
        return (
            "Configuration(welcome_message = %s, wav_original "
            "= %s, wav_modified = %s)" %
            (self.__welcome_message, self.__wav_original, self.__wav_modified))

    @property
    def welcome_message(self):
        return self.__welcome_message

    @welcome_message.setter
    def welcome_message(self, welcome_message):
        self.__welcome_message = welcome_message

    @welcome_message.getter
    def welcome_message(self):
        return self.__welcome_message

    @property
    def wav_original(self):
        return self.__wav_original

    @wav_original.setter
    def wav_original(self, wav_original):
        self.__wav_original = wav_original

    @wav_original.getter
    def wav_original(self):
        return self.__wav_original

    @property
    def wav_modified(self):
        return self.__wav_original

    @wav_modified.setter
    def wav_modified(self, wav_modified):
        self.__wav_modified = wav_modified

    @wav_modified.getter
    def wav_modified(self):
        return self.__wav_modified


class FlangerFilter:
    """TODO Comment
    """

    def __init__(self, max_delay, scale, rate):
        self.__max_delay = max_delay
        self.__scale = scale
        self.__rate = rate

    def __repr__(self):
        return ("{'max_delay: '%.4f',"
                "'scale': '%.2f', 'rate': '%.2f'}" %
                (self.__max_delay, self.__scale, self.__rate))

    def __str__(self):
        return ('FlangerFilter(max_delay = %.4f seg, '
                'scale = %.2f, rate = %.2f)'
                % (self.__max_delay, self.__scale, self.__rate))

    def apply_filter(self, original_signal, fs):
        """Apply flanger signal to raw signal.

        All parameters about the filter should be confired before
        use this function.
        """
        SAFE_BOUND_LIMIT = 1000

        flanger_signal = None

        if len(original_signal) > 0:
            # Create a lambda to call it when process delay later
            def sinus_reference(index): return math.sin(2 * math.pi * index *
                                                        (self.__rate / fs))
            # Convert delay in ms to max delay in samples
            max_delay_sample = round(self.__max_delay * fs)
            # Copy original signal into new one that will be returned
            flanger_signal = ndarray.copy(original_signal)

            # for i in range ((max_delay_sample + 1), len(original_signal)-SAFE_BOUND_LIMIT):
            
            i = max_delay_sample + 1
            while i < len(original_signal)-SAFE_BOUND_LIMIT:
                current_sinus = sinus_reference(i)

                current_delay = max_delay_sample * current_sinus

                flanger_signal[i] = int((self.__scale * original_signal[i]) + 
                                        (self.__scale * 
                                        original_signal[i - int(current_delay)]))
                
                i += 1

        return flanger_signal

    @property
    def max_delay(self):
        return self.__max_delay

    @max_delay.setter
    def max_delay(self, max_delay):
        self.__max_delay = max_delay

    @max_delay.getter
    def max_delay(self):
        return self.__max_delay

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        self.__scale = scale

    @scale.getter
    def scale(self):
        return self.__scale

    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, rate):
        self.__rate = rate

    @rate.getter
    def rate(self):
        return self.__rate


class CombFilter:
    """TODO: Comment here
    """

    def __init__(self, delay, scale):
        self.__delay = delay
        self.__scale = scale

    def __repr__(self):
        return ("{'delay': '%d', 'scale: '%.2f'}" %
                (self.__delay, self.__scale))

    def __str__(self):
        return str('CombFilter(delay = %d samples, scale = %.2f)' %
                   (self.__delay, self.__scale))

    def get_response_in_frecuency(self):
        logging.debug("Calculating response in frecuency of comb filter")

        numerator = [1] + (self.__delay - 1) * [0] + [self.__scale]
        denominator = 1.0

        _, response_in_frequency = signal.freqz(numerator, denominator)
        
        return response_in_frequency

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, delay):
        self.__delay = delay

    @delay.getter
    def delay(self):
        return self.__delay

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        self.__scale = scale

    @scale.getter
    def scale(self):
        return self.__scale


class WahWahFilter():

    # For limit the amplitude of wah wah signal for int16 wav file format
    MAX_INT16_VALUE = 32767

    def __init__(self, damping, min_cutoff, max_cutoff, frequency):
        self.__damping = damping
        self.__min_cutoff = min_cutoff
        self.__max_cutoff = max_cutoff
        self.__frequency = frequency

    def __repr__(self):
        return ("{'damping': '%f', 'min_f': '%d','max_f': '%d','wah_f': '%d'}" %
                (self.__damping, self.__min_cutoff, self.__max_cutoff, self.__frequency))

    def __str__(self):
        return (
            "WahWahFilter(damping = %f, min_f = %d, max_f = %d, wah_f = %d)" %
             (self.__damping, self.__min_cutoff, self.__max_cutoff, self.__frequency))

    def __create_triangle_waveform(self, original_signal_lenght, fs):
        # establish signal period from fs and wah wah frecuency
        signal_period = fs/self.__frequency
        # steps which triangle signal will do, considering the minummum
        # and max value that it has to reach. Also signal period is taken in account 
        # and finally it is multiplied by 2, because the signal will have to 
        # increase and decrease it's value in each signal period
        step = ((self.__max_cutoff - self.__min_cutoff)/signal_period) * 2
        # This is internal function that will create the signal, from the min value
        # to max value. It's a generator to make it memory efficient.
        def generator():
            index = 0
            # loop until to reach the lenght of original signal
            while index < original_signal_lenght:
                # each iteration start with an initial value
                signal_value = self.__min_cutoff
                # create ascendent part of triangle
                while signal_value < self.__max_cutoff:
                    signal_value += step
                    index += 1
                    yield signal_value
                # create desscendent part of triangle
                while signal_value > self.__min_cutoff:
                    signal_value -= step
                    index += 1
                    yield signal_value

        # Call the generator of the function and create a list from it
        triangle_signal = list(generator())
        # Trim triangle signal to lenght of original signal
        triangle_signal = triangle_signal[:original_signal_lenght]
        # return triangle singla.
        return triangle_signal

    def apply_filter(self, original_signal, fs):
        # Create triangle signal
        cuttoff_frequencies = self.__create_triangle_waveform(len(original_signal), fs)
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
        # create an np array to reproduce it then
        wahwah_signal = np_array(normalized_bandpass)
        
        return wahwah_signal

    @property
    def damping(self):
        return self.__damping

    @damping.setter
    def damping(self, value):
        self.__damping = value

    @damping.getter
    def damping(self):
        return self.__damping

    @property
    def min_cutoff(self):
        return self.__min_cutoff

    @min_cutoff.setter
    def min_cutoff(self, value):
        self.__min_cutoff = value

    @min_cutoff.getter
    def min_cutoff(self):
        return self.__min_cutoff

    @property
    def max_cutoff(self):
        return self.__max_cutoff

    @max_cutoff.setter
    def max_cutoff(self, value):
        self.__max_cutoff = value

    @max_cutoff.getter
    def max_cutoff(self):
        return self.__max_cutoff

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value

    @frequency.getter
    def frequency(self):
        return self.__frequency

    

class Model:

    DEFAULT_CONFIG_WELCOME_MESSAGE = "DSP Controller!"
    DEFAULT_CONFIG_WAV_ORIGINAL = "wavs/guitars.wav"
    DEFAULT_CONFIG_WAV_MODIFIED = "wavs/guitars_modified.wav"
    DEFAULT_COMB_DELAY = 8
    DEFAULT_COMB_SCALE = 1.0
    DEFAULT_FLANGER_MAX_DELAY = 0.003
    DEFAULT_FLANGER_SCALE = 0.5
    DEFAULT_FLANGER_RATE = 1.0
    DEFAULT_WAHWAH_DAMPING = 0.05
    DEFAULT_WAHWAH_MIN_CUTOFF = 500
    DEFAULT_WAHWAH_MAX_CUTOFF = 3000
    DEFAULT_WAHWAH_FREQUENCY = 1.1

    def __init__(self, db):
        self.__db = db
        # Set default parameters
        self.__load_default_values()

    def load_data_from_db(self):
        config_data = configparser.ConfigParser()
        config_data.read(self.__db)

        self.__config = Configuration(
            config_data['GENERAL']['config_welcome_message'],
            config_data['GENERAL']['config_wav_original'],
            config_data['GENERAL']['config_wav_modified'])

        self.__comb = CombFilter(int(config_data['COMB']['comb_delay']),
                                 float(config_data['COMB']['comb_scale']))

        self.__flanger = FlangerFilter(
            float(config_data['FLANGER']['flanger_max_delay']), 
            float(config_data['FLANGER']['flanger_scale']), 
            float(config_data['FLANGER']['flanger_rate']))

        self.__wahwah = WahWahFilter(
            float(config_data['WAHWAH']['wahwah_damping']), 
            int(config_data['WAHWAH']['wahwah_min_cutoff']), 
            int(config_data['WAHWAH']['wahwah_max_cutoff']),
            float(config_data['WAHWAH']['wahwah_frequency']))

    def save_data_to_db(self):
        config_data = configparser.ConfigParser()
        config_data.read(self.__db)

        config_data['GENERAL']['config_welcome_message'] = self.__config.welcome_message
        config_data['GENERAL']['config_wav_original'] = self.__config.wav_original
        config_data['GENERAL']['config_wav_modified'] = self.__config.wav_modified
        config_data['COMB']['comb_delay'] = str(self.__comb.delay)
        config_data['COMB']['comb_scale'] = str(self.__comb.scale)
        config_data['FLANGER']['flanger_max_delay'] = str(self.__flanger.max_delay)
        config_data['FLANGER']['flanger_scale'] = str(self.__flanger.scale)
        config_data['FLANGER']['flanger_rate'] = str(self.__flanger.rate)
        config_data['WAHWAH']['wahwah_damping'] = str(self.__wahwah.damping)
        config_data['WAHWAH']['wahwah_min_cutoff'] = str(self.__wahwah.min_cutoff)
        config_data['WAHWAH']['wahwah_max_cutoff'] = str(self.__wahwah.max_cutoff)
        config_data['WAHWAH']['wahwah_frequency'] = str(self.__wahwah.frequency)

    
        with open(self.__db, 'w') as configfile:
            config_data.write(configfile)

    def get_all_params(self):
        params = \
            "\t- 'config.welcome_message': '%s'\n" \
            "\t- 'config.wav_original': '%s'\n" \
            "\t- 'config.wav_modified': '%s'\n" \
            "\t- 'comb.delay': %d\n" \
            "\t- 'comb.scale': %.2f\n" \
            "\t- 'flanger.max_delay': %.3f\n" \
            "\t- 'flanger.scale': %.2f\n" \
            "\t- 'flanger.rate': %.2f\n"  \
            "\t- 'wahwah.damping': %.2f\n"  \
            "\t- 'wahwah.min_cutoff': %d\n"  \
            "\t- 'wahwah.max_cutoff': %d\n"  \
            "\t- 'wahwah.frequency': %.2f\n" %\
            (self.__config.welcome_message, self.__config.wav_original,
             self.__config.wav_modified, self.__comb.delay, self.__comb.scale,
             self.__flanger.max_delay, self.__flanger.scale,
             self.__flanger.rate, self.__wahwah.damping, self.__wahwah.min_cutoff,
             self.__wahwah.max_cutoff, self.__wahwah.frequency)

        return params

    def set_param(self, option, value):
        error_flag = False

        if option == 1 and isinstance(value, str):
            self.__config.welcome_message = value
        elif option == 2 and isinstance(value, str):
            self.__config.wav_original = value
        elif option == 3 and isinstance(value, str):
            self.__config.wav_modified = value
        elif option == 4 and isinstance(value, int):
            self.__comb.delay = value
        elif option == 5 and isinstance(value, float):
            self.__comb.scale = value
        elif option == 6 and isinstance(value, float):
            self.__flanger.max_delay = value
        elif option == 7 and isinstance(value, float):
            self.__flanger.scale = value
        elif option == 8 and isinstance(value, float):
            self.__flanger.rate = value
        elif option == 9 and isinstance(value, float):
            self.__wahwah.damping = value
        elif option == 10 and isinstance(value, int):
            self.__wahwah.min_cutoff = value
        elif option == 11 and isinstance(value, int):
            self.__wahwah.max_cutoff = value
        elif option == 12 and isinstance(value, float):
            self.__wahwah.frequency = value
        else:
            error_flag = True

        return error_flag

    def get_param(self, option):
        value = None

        if isinstance(option, int) and option >= 1 and option <= 12:
            data = {
                1: self.__config.welcome_message,
                2: self.__config.wav_original,
                3: self.__config.wav_modified,
                4: self.__comb.delay,
                5: self.__comb.scale,
                6: self.__flanger.max_delay,
                7: self.__flanger.scale,
                8: self.__flanger.rate,
                9: self.__wahwah.damping,
                10: self.__wahwah.min_cutoff,
                11: self.__wahwah.max_cutoff,
                12: self.__wahwah.frequency
            }
            value = data[option]

        return value

    
    def get_comb_signal(self):
        return self.__comb.get_response_in_frecuency()

    def get_flanger_signal(self, raw_signal, fs):
        return self.__flanger.apply_filter(raw_signal, fs)

    def get_wahwah_signal(self, raw_signal, fs):
        return self.__wahwah.apply_filter(raw_signal, fs)

    def get_parent_dir(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __load_default_values(self):
        self.__config = Configuration(
            Model.DEFAULT_CONFIG_WELCOME_MESSAGE,
            Model.DEFAULT_CONFIG_WAV_ORIGINAL,
            Model.DEFAULT_CONFIG_WAV_MODIFIED)

        self.__comb = CombFilter(Model.DEFAULT_COMB_DELAY,
                                    Model.DEFAULT_COMB_SCALE)

        self.__flanger = FlangerFilter(
            Model.DEFAULT_FLANGER_MAX_DELAY, 
            Model.DEFAULT_FLANGER_SCALE, 
            Model.DEFAULT_FLANGER_RATE)

        self.__wahwah = WahWahFilter(
            Model.DEFAULT_WAHWAH_DAMPING, 
            Model.DEFAULT_WAHWAH_MIN_CUTOFF,
            Model.DEFAULT_WAHWAH_MAX_CUTOFF, 
            Model.DEFAULT_WAHWAH_FREQUENCY)

    def restore_default_values(self):
        self.__load_default_values()
        self.save_data_to_db()

    @staticmethod
    def save_raw_to_wav(raw_data, wav_file, fs):
        wavfile.write(wav_file, fs, raw_data.astype(numpy.dtype('i2')))
        

    @staticmethod
    def convert_wav_to_raw(wav_file):
        data = None
        fs, data = wavfile.read(wav_file)
        return fs, data
        
