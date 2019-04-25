#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2019 Agustin Bassi.

Usage:
  python3 __main__.py (default config.ini)
  python3 __main__.py -c path_config.ini
  python3 __main__.py (-h | --help)
Options:
  -h, --help    Show help
  -c, --config  Set the path of config.ini file

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
