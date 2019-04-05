"""TODO comment

Copyright: Agustin Bassi, 2019.
License: BSD.
"""

class Configuration:
    """TODO: Comment here
    """

    __welcome_message = ""
    __wav_original = ""
    __wav_modified = ""
    __comb_delay = 0
    __comb_scale = 0.0
    __flanger_fs = 0
    __flanger_max_delay = 0.0
    __flanger_scale = 0.0
    __flanger_rate = 0.0


    @staticmethod
    def set_all_parameters(welcome_message, wav_original, wav_modified, 
                            comb_delay, comb_scale, flanger_fs, 
                            flanger_max_delay, flanger_scale,flanger_rate):
        Configuration.__welcome_message = welcome_message
        Configuration.__wav_original = wav_original
        Configuration.__wav_modified = wav_modified
        Configuration.__comb_delay = comb_delay
        Configuration.__comb_scale = comb_scale
        Configuration.__flanger_fs = flanger_fs
        Configuration.__flanger_max_delay = flanger_max_delay
        Configuration.__flanger_scale = flanger_scale
        Configuration.__flanger_rate = flanger_rate


    @staticmethod
    def to_repr():
        return ("{'welcome_message': '%s', 'wav_original': '%s', " \
                "'wav_modified': '%s', 'comb_delay': %d, 'comb_scale': " \
                "%.2f, 'flanger_fs': %d, 'flanger_max_delay': %.4f" \
                ", 'flanger_scale': %.2f, 'flanger_rate': %.2f}" %
                (Configuration.__welcome_message, 
                Configuration.__wav_original,
                Configuration.__wav_modified, Configuration.__comb_delay, 
                Configuration.__comb_scale,
                Configuration.__flanger_fs, Configuration.__flanger_max_delay,
                Configuration.__flanger_scale, Configuration.__flanger_rate))


    @staticmethod
    def to_str():
        return ("\nConfiguration(welcome_message = %s, wav_original " \
                "= %s, wav_modified = %s, comb_delay = %d, comb_scale " \
                "= %.2f, flanger_fs = %d hz, flanger_max_delay = %.4f segs" \
                ", flanger_scale = %.2f, flanger_rate = %.2f hz\n" %
                (Configuration.__welcome_message, 
                Configuration.__wav_original,
                Configuration.__wav_modified, Configuration.__comb_delay, 
                Configuration.__comb_scale, Configuration.__flanger_fs, 
                Configuration.__flanger_max_delay,
                Configuration.__flanger_scale, Configuration.__flanger_rate))


    @staticmethod
    def get_welcome_message():
        return Configuration.__welcome_message


    @staticmethod
    def get_wav_original():
        return Configuration.__wav_original


    @staticmethod
    def get_wav_modified():
        return Configuration.__wav_modified


    @staticmethod
    def get_comb_delay():
        return Configuration.__comb_delay


    @staticmethod
    def get_comb_scale():
        return Configuration.__comb_scale


    @staticmethod
    def get_flanger_fs():
        return Configuration.__flanger_fs


    @staticmethod
    def get_flanger_max_delay():
        return Configuration.__flanger_max_delay

  
    @staticmethod
    def get_flanger_scale():
        return Configuration.__flanger_scale

  
    @staticmethod
    def get_flanger_rate():
        return Configuration.__flanger_rate

 
    @staticmethod
    def set_welcome_message(welcome_message):
        Configuration.__welcome_message = welcome_message

 
    @staticmethod
    def set_wav_original(wav_original):
        Configuration.__wav_original = wav_original

  
    @staticmethod
    def set_wav_modified(wav_modified):
        Configuration.__wav_modified = wav_modified

 
    @staticmethod
    def set_comb_delay(comb_delay):
        Configuration.__comb_delay = comb_delay

  
    @staticmethod
    def set_comb_scale(comb_scale):
        Configuration.__comb_scale = comb_scale

  
    @staticmethod
    def set_flanger_fs(flanger_fs):
        Configuration.__flanger_fs = flanger_fs

   
    @staticmethod
    def set_flanger_max_delay(flanger_max_delay):
        Configuration.__flanger_max_delay = flanger_max_delay

   
    @staticmethod
    def set_flanger_scale(flanger_scale):
        Configuration.__flanger_scale = flanger_scale

  
    @staticmethod
    def set_flanger_rate(flanger_rate):
        Configuration.__flanger_rate = flanger_rate

