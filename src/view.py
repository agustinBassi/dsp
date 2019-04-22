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
        print("\t(  0 ) --- Exit program")
        print("\t(  1 ) --- Show current configuration parameters")
        print("\t(  2 ) --- Update configuration parameters")
        print("\t(  3 ) --- Save current values into config file")
        print("\t(  4 ) --- Plot response in frecuency of comb filter")
        print("\t(  5 ) --- Plot flanger signal over original signal")
        print("\t(  6 ) --- Plot wahwah signal over original signal")
        print("\t(  7 ) --- Play original wav audio")
        print("\t(  8 ) --- Play flanger wav audio")
        print("\t(  9 ) --- Play wahwah wav audio")
        print("\t( 10 ) --- Play flanger & wahwah concatenated wav audio")
        print("\t( 11 ) --- Restore default values")
        print("\n==================================================\n")

        while True:
            try:
                option = int(input("--- Enter option from 0 to 11 > Option: "))
                print("\n==================================================\n")
                if (option >= 0 and option <= 11):
                    break
                else:
                    print("\n==================================================\n")
                    raise ValueError
            except ValueError:
                print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")
                print("ERROR: Type a valid menu option from 0 to 11!")
                print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")

        return option

    def show_settings_menu(self):
        print("\n==================================================\n")
        print("\nSelect one of options below:\n")
        print("\t|--- (  0 ) - no modify any parameter")
        print("\t|")
        print("\t|--- (  1 ) - CONFIG  --> welcome_message")
        print("\t|--- (  2 ) - CONFIG  --> wav_original")
        print("\t|--- (  3 ) - CONFIG  --> wav_modified")
        print("\t|")
        print("\t|--- (  4 ) - COMB    --> delay")
        print("\t|--- (  5 ) - COMB    --> scale")
        print("\t|")
        print("\t|--- (  6 ) - FLANGER --> max_delay")
        print("\t|--- (  7 ) - FLANGER --> scale")
        print("\t|--- (  8 ) - FLANGER --> rate")
        print("\t|")
        print("\t|--- (  9 ) - WAHWAH  --> damping")
        print("\t|--- ( 10 ) - WAHWAH  --> min_cutoff")
        print("\t|--- ( 11 ) - WAHWAH  --> max_cutoff")
        print("\t|--- ( 12 ) - WAHWAH  --> frequency")
        print("\n==================================================\n")

        while True:
            try:
                option = int(input("--- Enter option from 0 to 12 > Option: "))
                print("\n==================================================\n")
                if (option >= 0 and option <= 12):
                    break
                else:
                    raise ValueError
            except ValueError:
                print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")
                print("ERROR: Type a valid menu option from 0 to 12!")
                print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")

        value = None

        if option == 1:
            value = (str(input("\n--- Enter welcome message > ")))
        elif option == 2:
            value = (str(input("\n--- Enter wav original > ")))
        elif option == 3:
            value = (str(input("\n--- Enter wav modified >")))
        elif option == 4:
            value = (int(input("\n--- Enter comb delay (int 1 to 100) > ")))
        elif option == 5:
            value = (float(input("\n--- Enter comb scale (float 0 to 100) > ")))
        elif option == 6:
            value = (float(input("\n--- Enter flanger delay (float 0.001 to 0.020) > ")))
        elif option == 7:
            value = (float(input("\n--- Enter flanger scale (float 0 to 1.0) > ")))
        elif option == 8:
            value = (float(input("\n--- Enter flanger rate (float 0 to 5.0) > ")))
        elif option == 9:
            value = (float(input("\n--- Enter wahwah damping (float 0.01 to 0.07) > ")))
        elif option == 10:
            value = (int(input("\n--- Enter wahwah min cutoff (int 100 to 100) > ")))
        elif option == 11:
            value = (int(input("\n--- Enter wahwah max cutoff int (2500 to 4500) > ")))
        elif option == 12:
            value = (float(input("\n--- Enter wahwah frequency (float 0.1 to 2.0) > ")))

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

    def plot_wahwah_triangle_wave(self, triangle_signal,
                        title="Triangle waveform",
                        label_x="Samples", label_y="Frecuency (Hz)",
                        ref_1="Response in frecuency", refs_location="best"):
        # plot signals to graphic
        plt.plot(triangle_signal)
        # set labels to axes
        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.legend([ref_1], loc=refs_location)
        # show figure
        plt.show()

    def plot_wahwah_signals(self, original_signal, wahwah_signal,
                                title="Wahwah signal response",
                                label_x="Time", label_y="Amplitude",
                                ref_1="Original signal", ref_2="Wahwah signal",
                                refs_location="best"):
        # plot signals to graphic
        plt.plot(original_signal)
        plt.plot(wahwah_signal)
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
        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        print("INFO: %s" % error_message)
        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++\n")

    @staticmethod
    def show_program_arguments(config_file, test_flag):
        print("\n///////////////////////////////////////////////////\n")
        print("Command line arguments:")
        print("\t- config_file: %s" % config_file)
        print("\t- test_flag:   %d" % test_flag)
        print("\n///////////////////////////////////////////////////\n")
