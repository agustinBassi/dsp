import os

class WavFile:

    def convert_to_raw(wav_file):
        print ("convert_to_raw(): {}".format(wav_file))

    def convert_to_wav(raw_file):
        print ("convert_to_wav(): {}".format(raw_file))

    def play (file_path):
        print ("play(): {}".format(file_path))
        playsound(file_path)

    def get_duration (wav_file):
        print ("get_duration(): {}".format(wav_file))

def test_WavFile():
  FILE_PATH = "/home/agustin/Desktop/dsp/wavs/tone_1khz.wav"

  print ("Testing WavFile...")
  
  WavFile.convert_to_raw(FILE_PATH)
  WavFile.convert_to_wav(FILE_PATH)
  WavFile.play(FILE_PATH)
  WavFile.get_duration(FILE_PATH)




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