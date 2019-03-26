import os
from scipy.io import wavfile
import struct

class WavFile:

    def convert_to_raw(wav_file):
        print ("\nconvert_to_raw(): {}".format(wav_file))
        data = []
        try:
            fs, data = wavfile.read(wav_file)
            print ("\t- FS: " + str(fs))
            print ("\t- Data elements: " + str(len(data)) + "\n")
        except:
            print ("\tERROR - convert_to_raw(): {}".format(wav_file))
        
        return data
        
    def save_raw_into_wav(raw_list, wav_path):
        print ("save_raw_into_wav(): {}".format(wav_path))
        
        file_wav = open(wav_path, 'w')

        for i in range(0, len(raw_list)):
            value = raw_list[i] #random.randint(-32767, 32767)
            packed_value = struct.pack('h', value)
            file_wav.write(packed_value)

        file_wav.close()

    def play (file_path):
        print ("\nplay(): {}".format(file_path))
        try:
            os.system("aplay {}".format(file_path))
        except:
            print ("\tERROR - play(): {}".format(wav_file))

    def get_duration (wav_file):
        print ("\nget_duration(): {}".format(wav_file))
        duration = 0.0
        try:
            fs, data = wavfile.read(wav_file)
            duration = len(data)/fs
            print ("\t- Duration: " + str(duration))
        except:
            print ("\tERROR - get_duration(): {}".format(wav_file))
        
        return duration

def test_WavFile():
  ORIGINAL_WAV = "/home/agustin/Desktop/dsp/wavs/tone_1khz.wav"
  MODIFIED_WAV = "/home/agustin/Desktop/dsp/wavs/tone_1khz_modified.wav"

  print ("\nTesting WavFile...\n")
  
  raw_list = WavFile.convert_to_raw(ORIGINAL_WAV)
  WavFile.save_raw_into_wav(raw_list, MODIFIED_WAV)
  WavFile.play(MODIFIED_WAV)
  #WavFile.get_duration(FILE_PATH)




"""
def utils_convert_wav_to_raw (file_to_read):
        print ("Reading file: " + file_to_read)
        input_data = read(file_to_read)
        audio = input_data[1]
        return audio

    def utils_convert_raw_to_wav (raw_signal, file_to_save):
        print ("Saving raw data to file: " + file_to_save)
        wavfile.write(file_to_save, 44100, raw_signal)

    def utils_play_wav(file):
        print("Playing WAV file: " + file)
        song = pyglet.media.load(file)
        song.play()
        pyglet.app.run()

"""