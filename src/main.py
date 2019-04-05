#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""DSP Final Practice Project.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging

from wav_file import test_wav_file_class
from flanger_filter import test_flanger_filter_class
from filters_view import test_filters_view_class
from comb_filter import test_comb_filter_class
from filters_controller import test_filters_controller_class

def main():
    """Main method to run DSP Project.
    """
    print("Running DSP Final Practice. Log level %d" % logging.DEBUG)

    logging.basicConfig(level = logging.DEBUG,
                        format = '%(levelname)s - %(message)s')

    #test_wav_file_class()
    #test_flanger_filter_class()
    #test_filters_view_class()
    #test_comb_filter_class()
    test_filters_controller_class()

main()