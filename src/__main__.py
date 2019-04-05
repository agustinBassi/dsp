#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""DSP Final Practice Project.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging
import argparse
import os

from .model import Model
from .view import View
from .controller import Controller

DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_CONFIG_FILE = "/config.json"
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
    config_file = os.path.dirname(os.path.realpath(__file__))
    config_file += DEFAULT_CONFIG_FILE
    test_flag = DEFAULT_TEST_FLAG

    log_level, config_file, test_flag = parse_options(log_level, config_file,
                                                      test_flag)
    
    # logging.basicConfig(level = log_level,
    #                     format = '%(levelname)s - %(message)s')

    View.show_program_arguments(log_level, config_file, test_flag)

    model = Model(config_file)
    view = View()
    controller = Controller(model, view)

    controller.start()

if __name__ == "__main__":
    main()