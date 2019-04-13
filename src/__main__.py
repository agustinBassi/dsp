#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""DSP Final Practice Project.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import argparse
import os

from model import Model
from view import View
from controller import Controller

DEFAULT_CONFIG_FILE = "/config.ini"
DEFAULT_TEST_FLAG = False


def parse_options(config_file, test_flag):
    # Create the parser and putting a title to it
    parser = argparse.ArgumentParser("Running '{}'".format('main.py'))

    # store_true makes it a flag
    parser.add_argument("-t", "--test", type=int, default=int(test_flag),
                        choices=[0, 1], help="Test on/off")

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="The path of config file, it must be ini file format")

    arguments = parser.parse_args()

    if arguments.config is not None:
        config_file = arguments.config

    if arguments.test is not None:
        test_flag = bool(arguments.test)

    return config_file, test_flag


def main():
    """Main method to run DSP Project.
    """

    config_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file += DEFAULT_CONFIG_FILE
    test_flag = DEFAULT_TEST_FLAG

    config_file, test_flag = parse_options(config_file, test_flag)

    View.show_program_arguments(config_file, test_flag)

    controller = Controller(Model(config_file), View())

    controller.start()


if __name__ == "__main__":
    main()
