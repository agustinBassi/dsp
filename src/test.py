import logging

from wav_file import test_wav_file_class

def main():
    print("Running DSP Final Practice. Log level %d" % logging.DEBUG)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')

    test_wav_file_class()


main()