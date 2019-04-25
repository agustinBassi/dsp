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


def parse_options(config_file):
    # Create the parser and putting a title to it
    parser = argparse.ArgumentParser("Running '{}'".format('main.py'))

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="The path of config file, it must be ini file format")

    arguments = parser.parse_args()

    if arguments.config is not None:
        config_file = arguments.config

    return config_file


def main():
    """Main method to run DSP Project.
    """

    config_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file += DEFAULT_CONFIG_FILE

    config_file = parse_options(config_file)

    View.show_program_arguments(config_file)

    controller = Controller(Model(config_file), View())

    controller.start()


if __name__ == "__main__":
    main()
