"""This module has all needed to work with Wav files.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging
import os

from scipy.io import wavfile


class WavFile:
    """This class works with actions related to wav files.

    All methods of this class are static methods, so, no instance 
    of object is needed.
    """

    DEFAULT_FS = 44100

    @staticmethod
    def convert_to_raw(wav_file):
        data = None
        try:
            fs, data = wavfile.read(wav_file)
            logging.debug("File opened: %s - FS: %dkhz- " \
                          "Elements: %d - Duration: %.2f segs" % \
                          (wav_file, fs, len(data), len(data)/fs))
        except:
            logging.error("Error openning wav: %s" % wav_file)
        return data
    

    @staticmethod    
    def save_raw_into_wav(raw_list, wav_file):
        try:
            logging.debug("Trying to save raw data into wav file: %s" \
                          % wav_file)
            wavfile.write(wav_file, WavFile.DEFAULT_FS, raw_list)
        except:
            logging.error("Error saving raw data into wav file %s" \
                          % wav_file)


    @staticmethod
    def play (wav_file):
        try:
            logging.debug("Trying to play wav file: %s" % wav_file)
            os.system("aplay %s" % wav_file)
        except:
            logging.error("Error playing wav file: %s" % wav_file)


def test_wav_file_class():
    
  ORIGINAL_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz.wav"
  MODIFIED_WAV = "/home/agustin/projects/dsp/wavs/tone_1khz_modified.wav"

  raw_list = WavFile.convert_to_raw(ORIGINAL_WAV)
  WavFile.save_raw_into_wav(raw_list, MODIFIED_WAV)
  WavFile.play(MODIFIED_WAV)
