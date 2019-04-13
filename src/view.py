"""This module has all needed to plot filters signals with pyplot library.

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import logging
import os

import matplotlib.pyplot as plt
from scipy.io import wavfile


class View:

    def show_main_menu(self):
        print("\n==================================================\n")
        print("\nSelect one of options below:\n")
        print("\t0 - exit program")
        print("\t1 - show current configuration parameters")
        print("\t2 - set new parameters")
        print("\t3 - plot response in frecuency of comb filter")
        print("\t4 - play original wav audio")
        print("\t5 - play flanger wav audio")
        print("\t6 - plot flanger filter signal")
        print("\t7 - save current values into config file")
        print("\n==================================================\n")

        while True:
            try:
                option = int(input("Enter option from 0 to 7 > "))
                if (option >= 0 and option <= 7):
                    break
                else:
                    raise ValueError
            except ValueError:
                print("\n================================================\n")
                print("ERROR - Type a valid menu option from 1 to 7!")
                print("\n================================================\n")

        return option

    def show_settings_menu(self):
        print("\n==================================================\n")
        print("\nSelect one of options below:\n")
        print("\t0 - no modify any parameter")
        print("\t1 - set_welcome_message")
        print("\t2 - set_wav_original")
        print("\t3 - set_wav_modified")
        print("\t4 - set_comb_delay")
        print("\t5 - set_comb_scale")
        print("\t6 - set_flanger_fs")
        print("\t7 - set_flanger_max_delay")
        print("\t8 - set_flanger_scale")
        print("\t9 - set_flanger_rate")
        print("\n==================================================\n")

        while True:
            try:
                option = int(input("Enter option from 0 to 9 > "))
                if (option >= 0 and option <= 9):
                    break
                else:
                    raise ValueError
            except ValueError:
                print("\n================================================\n")
                print("ERROR - Type a valid menu option from 0 to 9!")
                print("\n================================================\n")

        value = None

        if option == 1:
            value = (str(input("\n\tEnter welcome message > ")))
        elif option == 2:
            value = (str(input("\n\tEnter wav original > ")))
        elif option == 3:
            value = (str(input("\n\tEnter wav modified >")))
        elif option == 4:
            value = (int(input("\n\tEnter comb delay > ")))
        elif option == 5:
            value = (float(input("\n\tEnter comb scale > ")))
        elif option == 6:
            value = (int(input("\n\tEnter flanger fs > ")))
        elif option == 7:
            value = (float(input("\n\tEnter flanger delay > ")))
        elif option == 8:
            value = (float(input("\n\tEnter flanger scale > ")))
        elif option == 9:
            value = (float(input("\n\tEnter flanger rate > ")))

        return option, value

    def plot_comb_filter(self, response_in_frequency,
                         title="Comb filter response in frecuency",
                         label_x="Time", label_y="Amplitude",
                         ref_1="Response in frecuency", refs_location="best"):

        logging.debug("Showing Comb filter plot - "
                      "title: %s, Label X: %s, Label Y: %s, " %
                      (title, label_x, label_y))

        # plot signals to graphic
        plt.plot(abs(response_in_frequency))
        # set labels to axes
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1], loc=refs_location)
        # show figure
        plt.show()

    def plot_flanger_signals(self, original_signal, flanger_signal,
                             title="Flanger signal response",
                             label_x="Time", label_y="Amplitude",
                             ref_1="Original signal", ref_2="Flanger signal",
                             refs_location="best"):

        logging.debug("Plot flanger signal - "
                      "title: %s, Label X: %s, Label Y: %s, " %
                      (title, label_x, label_y))

        # plot signals to graphic
        plt.plot(original_signal)
        plt.plot(flanger_signal)
        # set legends to graph
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1, ref_2], loc=refs_location)
        # show figure
        plt.show()

    def show_current_settings(self, settings):
        print("\n==================================================\n")
        print("Current settings:\n")
        print(settings)
        print("\n==================================================\n")

    def play_audio(self, audio_file):
        print("\n==================================================\n")
        os.system("aplay %s" % audio_file)
        print("\n==================================================\n")

    def show_error(self, error_message):
        print("\n**************************************************\n")
        print("ERROR: %s" % error_message)
        print("\n**************************************************\n")

    def show_info(self, error_message):
        print("\n==================================================\n")
        print("INFO: %s" % error_message)
        print("\n==================================================\n")

    @staticmethod
    def show_program_arguments(config_file, test_flag):
        print("\n==================================================\n")
        print("Command line arguments:")
        print("\t- config_file: %s" % config_file)
        print("\t- test_flag:   %d" % test_flag)
        print("\n==================================================\n")
