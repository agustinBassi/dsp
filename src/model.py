import logging
import os
import math
import os
import json

import numpy as np
import scipy.signal as signal
from scipy.io import wavfile


class Configuration:
    """TODO: Comment here
    """

    def __init__(self, welcome_message, wav_original, wav_modified):
        self.__welcome_message = welcome_message
        self.__wav_original = wav_original
        self.__wav_modified = wav_modified

    def __repr__(self):
        return ("{'welcome_message': '%s', 'wav_original': '%s', " \
                "'wav_modified': '%s'}" % (self.__welcome_message, 
                self.__wav_original, self.__wav_modified))

    def __str__(self):
        return ("Configuration(welcome_message = %s, wav_original " \
                "= %s, wav_modified = %s)" % (self.__welcome_message, 
                self.__wav_original, self.__wav_modified))

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

        # for i in range ((max_delay_sample + 1), len(flanger_signal-1)):
        #     current_sinus = sinus_reference(i)

        #     current_delay = max_delay_sample * current_sinus

        #     if (i - int(current_delay)) >= 0:
        #         flanger_signal[i] = int((self.__scale * flanger_signal[i]) + 
        #                                 (self.__scale * 
        #                                 flanger_signal[i - int(current_delay)]))
      
        try:
            # Iterate over the signal, calculate each delay to be applied
            # and then add it to original signal
            for i in range ((max_delay_sample + 1), len(flanger_signal)-1):
                current_sinus = sinus_reference(i)

                current_delay = max_delay_sample * current_sinus
                
                if (i - int(current_delay)) >= 0:
                    flanger_signal[i] = int((self.__scale * flanger_signal[i]) + 
                                            (self.__scale * 
                                            flanger_signal[i - int(current_delay)]))
            logging.debug("Flanger filter applied to signal")
        except IndexError:
            logging.error("Index %d out of range of %d" % 
                            (i - int(current_delay), len(flanger_signal)))

        return flanger_signal

    @property
    def fs(self):
        return self.__fs

    @fs.setter
    def fs(self, fs):
        self.__fs = fs

    @fs.getter
    def fs(self):
        return self.__fs
    
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
        self.__numerator = [1] + (self.__delay - 1) * [0] + [self.__scale]
        self.__denominator = 1.0

    def __repr__(self):
        return ("{'delay': '%d', 'scale: '%.2f'}"  %
                (self.__delay, self.__scale)) 

    def __str__(self):
        return str('CombFilter(delay = %d samples, scale = %.2f)' %
                (self.__delay, self.__scale))

    def get_response_in_frecuency (self):
        logging.debug("Calculating response in frecuency of comb filter")
        
        numerator = [1] + (self.__delay - 1) * [0] + [self.__scale]
        denominator = 1.0

        frequencies, response_in_frequency = signal.freqz(numerator, 
                                                          denominator)
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

class Error:
    """
    """
    
    __error_mesage = ""


    @staticmethod
    def set_error_message(error_message):
        Error.__error_mesage = error_message

    @staticmethod
    def get_error_message():
        return Error.__error_mesage

class Model:

    def __init__(self, db):
        self.__db = db

    def load_data_from_db(self):
        error_flag = False
        try:
            with open(self.__db) as db_data:
                data = json.load(db_data)
            
            self.__config = Configuration(data['config_welcome_message'],
                                          data['config_wav_original'],
                                          data['config_wav_modified'])

            self.__comb = CombFilter(data['comb_delay'],
                                     data['comb_scale'])

            self.__flanger = FlangerFilter(data['flanger_fs'],
                                           data['flanger_max_delay'],
                                           data['flanger_scale'],
                                           data['flanger_rate'])

            logging.debug("Config file read correctly: %s" % 
                           self.__db)
        except:
            logging.error("Error read config file: %s" % self.__db)
            Error.set_error_message("Error read config file: %s" % self.__db)
            error_flag = True

        return error_flag

    def save_data_to_db(self):
        error_flag = False

        new_data = {
            'config_welcome_message': str(self.__config.welcome_message),
            'config_wav_original': str(self.__config.wav_original),
            'config_wav_modified': str(self.__config.wav_modified),
            'comb_delay': int(self.__comb.delay),
            'comb_scale': float(self.__comb.scale),
            'flanger_fs': int(self.__flanger.fs),
            'flanger_max_delay': float(self.__flanger.max_delay),
            'flanger_scale': float(self.__flanger.scale),
            'flanger_rate': float(self.__flanger.rate)
        }

        try:
            with open(self.__db, 'w') as db_data:  
                json.dump(new_data, db_data, indent=4)
            logging.debug("New data was saved into %s" % self.__db)
        except:
            logging.error("Impossible to save config file")
            Error.set_error_message("Impossible to save config file")
            error_flag = True
        
        return error_flag

    def get_all_params(self):
        # return ("%s\n%s\n%s" % (str(self.__config), str(self.__comb),
        #                         str(self.__flanger)))
        return {
            'config.welcome_message': self.__config.welcome_message,
            'config.wav_original': self.__config.wav_original,
            'config.wav_original': self.__config.wav_original,
            'comb.delay': self.__comb.delay,
            'comb.scale': self.__comb.scale,
            'flanger.fs': self.__flanger.fs,
            'flanger.max_delay': self.__flanger.max_delay,
            'flanger.scale': self.__flanger.scale,
            'flanger.rate': self.__flanger.rate
        }
        

    def set_param(self, option, value):
        error_flag = False

        if option == 1 and type(value) == str:
            self.__config.welcome_message = value
        elif option == 2 and type(value) == str:
            self.__config.wav_original = value
        elif option == 3 and type(value) == str:
            self.__config.wav_modified = value
        elif option == 4 and type(value) == int:
            self.__comb.delay = value
        elif option == 5 and type(value) == float:
            self.__comb.scale = value
        elif option == 6 and type(value) == int:
            self.__flanger.fs = value
        elif option == 7 and type(value) == float:
            self.__flanger.max_delay = value
        elif option == 8 and type(value) == float:
            self.__flanger.scale = value
        elif option == 9 and type(value) == float:
            self.__flanger.rate = value
        else:
            error_flag = True
            Error.set_error_message("Error set parameter - check option '{}'"
                                    "or type of '{}'".format(option, value))
        
        return error_flag

    def get_param(self, option):
        error_flag = False
        value = None

        if type(option) != int or option < 0 or option > 8:
            error_flag = True
            Error.set_error_message("Get param " \
                                    "invalid option '{}'".format(option))
        else:
            data = {
                0: self.__config.welcome_message,
                1: self.__config.wav_original,
                2: self.__config.wav_modified,
                3: self.__comb.delay,
                4: self.__comb.scale,
                5: self.__flanger.fs,
                6: self.__flanger.max_delay,
                7: self.__flanger.scale,
                8: self.__flanger.rate,
            }
            value = data[option]
        
        return error_flag, value

    def get_flanger_signal(self, raw_signal):
        error_flag = False
        flanger_signal = None

        if len(raw_signal) < 1:
            error_flag = True
            Error.set_error_message("Invalid raw singal to apply flanger")
        else:
            flanger_signal = self.__flanger.apply_filter(raw_signal)

        return error_flag, flanger_signal

    def get_comb_signal(self):
        return self.__comb.get_response_in_frecuency()

    def get_parent_dir(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def save_raw_to_wav(raw_data, wav_file):
        error_flag = False
        DEFAULT_FS = 44100
        try:
            wavfile.write(wav_file, DEFAULT_FS, raw_data)
            logging.debug("Data saved into wav file: %s" % wav_file)
        except:
            logging.error("Error saving wav file %s" % wav_file)
            error_flag = True
            Error.set_error_message("Error saving wav file %s" % wav_file)
        
        return error_flag


    @staticmethod
    def convert_wav_to_raw(wav_file):
        data = None
        error_flag = False
        try:
            fs, data = wavfile.read(wav_file)
            logging.debug("File opened: %s - FS: %dkhz- " \
                          "Elements: %d - Duration: %.2f segs" % \
                          (wav_file, fs, len(data), len(data)/fs))
        except:
            logging.error("Error openning wav: %s" % wav_file)
            error_flag = True
            Error.set_error_message("Error openning wav file %s" % wav_file)

        return error_flag, data

