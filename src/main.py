#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""DSP Final Practice Project.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging
import argparse
import os

from wav_file import test_wav_file_class
from flanger_filter import test_flanger_filter_class
from filters_view import test_filters_view_class
from comb_filter import test_comb_filter_class
from filters_controller import test_filters_controller_class

DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_CONFIG_FILE = "../config.json"
DEFAULT_TEST_FLAG = False

def parse_options(log_level, config_file, test_flag):
    # Create the parser and putting a title to it
    parser = argparse.ArgumentParser("Running '{}'".format('main.py'))

    parser.add_argument("-v", "--verbosity", type=str, 
                        choices=["ERROR", "WARN", "INFO", "DEBUG"],
                        help="Verbosity level")
    # store_true makes it a flag
    parser.add_argument("-t", "--test", type=int, default=int(test_flag),
                        choices=[0, 1], help="Test on/off")

    parser.add_argument("-c", "--config", type=str,
                        help="The path of config file, it must be JSON extension")

    arguments = parser.parse_args()

    log_level_map = {
        "ERROR": logging.ERROR,
        "WARN" : logging.WARN,
        "INFO" : logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    if arguments.verbosity != None:
        log_level = log_level_map[arguments.verbosity]

    if arguments.config != None:
        config_file = arguments.config

    if arguments.test != None:
        test_flag = bool(arguments.test)

    return log_level, config_file, test_flag

def main():
    """Main method to run DSP Project.
    """
    
    log_level = DEFAULT_LOG_LEVEL
    config_file = DEFAULT_CONFIG_FILE
    test_flag = DEFAULT_TEST_FLAG

    log_level, config_file, test_flag = parse_options(log_level, config_file,
                                                      test_flag)
    
    logging.basicConfig(level = log_level,
                        format = '%(levelname)s - %(message)s')

    print("The level of vervosity is {}".format(log_level))
    print("The config file is {}".format(config_file))
    print("The test flag is {}".format(test_flag))
    
    #test_wav_file_class()
    #test_flanger_filter_class()
    #test_filters_view_class()
    #test_comb_filter_class()
    test_filters_controller_class()

    

main()