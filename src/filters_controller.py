"""TODO comment

Copyright: Agustin Bassi, 2019.
License: BSD.
"""
import json
import logging
import os
import sys

import numpy as np

from configuration import Configuration as config
from filters_view import FiltersView as view
from comb_filter import CombFilter
from flanger_filter import FlangerFilter
from wav_file import WavFile


class FlitersController:
    """TODO: Comment here
    """

    #TODO estaria bueno que desde aca se pueda mapear a una funcion
    __OPTIONS = {
        0: "exit program",
        1: "show current configuration parameters",
        2: "set new parameters",
        3: "plot response in frecuency of comb filter",
        4: "apply flanger filter and save new wav modified",
        5: "same as 4 option but plotting the response",
        6: "save current values into config file"
    }

    def __init__(self, config_file):
        self.__config_file = config_file
        self.read_configs()

    def __repr__(self):
        return ("{'config_file': '%s'}" % self.__config_file)

    def __str__(self):
        return ("FlitersController(config_file = %s)" % self.__config_file)

    def read_configs(self):
        try:
            with open(self.__config_file) as json_data_file:
                configs = json.load(json_data_file)
            
            config.set_welcome_message(configs['welcome_message'])
            config.set_wav_original(configs['wav_original'])
            config.set_wav_modified(configs['wav_modified'])
            config.set_comb_delay(configs['comb_delay'])
            config.set_comb_scale(configs['comb_scale'])
            config.set_flanger_fs(configs['flanger_fs'])
            config.set_flanger_max_delay(configs['flanger_max_delay'])
            config.set_flanger_scale(configs['flanger_scale'])
            config.set_flanger_rate(configs['flanger_rate'])

            logging.debug("Config file read correctly: %s" % 
                           self.__config_file)
        except:
            logging.error("Impossible to read config file: %s" % 
                           self.__config_file)

    def show_menu(self):
        print("\nSelect one of options below:\n")
        # Add to menu string the options availables
        for i in range(0, len(FlitersController.__OPTIONS)):
            print("\t%d - %s" % (i, FlitersController.__OPTIONS[i]))
        
        while True:
            try:
                self.__option_selected = int(input("\n> "))
                if (self.__option_selected < 0 or 
                    self.__option_selected > 
                    len(FlitersController.__OPTIONS)):
                    raise ValueError
                else:
                    break
            except ValueError:
                print("ERROR - Type a valid option from 1 to %d!" % 
                      len(FlitersController.__OPTIONS))

        if self.__option_selected == 0:
            self.__do_option_0()
        elif self.__option_selected == 1:
            self.__do_option_1()
        elif self.__option_selected == 2:
            self.__do_option_2()
        elif self.__option_selected == 3:
            self.__do_option_3()
        elif self.__option_selected == 4:
            self.__do_option_4()
        elif self.__option_selected == 5:
            self.__do_option_5()
        elif self.__option_selected == 6:
            self.__do_option_6()

    def __do_option_0(self):
        sys.exit()

    def __do_option_1(self):
        config.to_str()

    def __do_option_2(self):
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

        while True:
            try:
                option = int(input("\n> "))
                if (option >= 0 and option <= 9):
                    break
                else: 
                    raise ValueError
            except ValueError:
                print("ERROR - Invalid option!")

        if option == 1:
            config.set_welcome_message(str(input("Enter welcome message > ")))
        elif option == 2:
            config.set_wav_original(str(input("Enter wav original > ")))
        elif option == 3:
            config.set_wav_modified(str(input("Enter wav modified >" )))
        elif option == 4:
            config.set_comb_delay(int(input("Enter comb delay > ")))
        elif option == 5:
            config.set_comb_delay(float(input("Enter comb scale > ")))
        elif option == 6:
            config.set_flanger_fs(int(input("Enter flanger fs > ")))
        elif option == 7:
            config.set_flanger_max_delay(float(input("Enter flanger delay > ")))
        elif option == 8:
            config.set_flanger_scale(float(input("Enter flanger scale > ")))
        elif option == 9:
            config.set_flanger_rate(float(input("Enter flanger rate > ")))

    def __do_option_3(self):
        comb_filter = CombFilter(config.get_comb_delay(), 
                                 config.get_comb_scale())
        
        freqs, response_in_freq = comb_filter.get_response_in_frecuency()

        view.plot_comb_filter(freqs, response_in_freq)

    def __do_option_4(self):
        flanger_filter = FlangerFilter(config.get_flanger_fs(), 
                                       config.get_flanger_max_delay(), 
                                       config.get_flanger_scale(), 
                                       config.get_flanger_rate())

        original_signal = WavFile.convert_to_raw(config.get_wav_original())

        flanger_signal = flanger_filter.apply_filter(original_signal)

        WavFile.save_raw_into_wav(flanger_signal, config.get_wav_modified())

        WavFile.play(config.get_wav_modified())

        return original_signal, flanger_signal

    def __do_option_5(self):
        original_signal, flanger_signal = self.__do_option_4()
        view.plot_flanger_signals(original_signal, flanger_signal)
    
    def __do_option_6(self):
        config.to_str()
        new_data = {
            'welcome_message': config.get_welcome_message(),
            'wav_original': config.get_wav_original(),
            'wav_modified': config.get_wav_modified(),
            'comb_delay': config.get_comb_delay(),
            'comb_scale': config.get_comb_scale(),
            'flanger_fs': config.get_flanger_fs(),
            'flanger_max_delay': config.get_flanger_max_delay(),
            'flanger_scale': config.get_flanger_scale(),
            'flanger_rate': config.get_flanger_rate()
        }

        try:
            with open(self.__config_file, 'w') as outfile:  
                json.dump(new_data, outfile, indent=4)
            logging.error("New data was saved into %s" % self.__config_file)
        except:
            logging.error("Impossible to save config file")

def test_filters_controller_class():
    CONFIG_FILE = "/home/agustin/projects/dsp/config.json"
    
    controller = FlitersController(CONFIG_FILE)

    #controller.read_configs()

    #print(str(controller))
    #print(repr(controller))

    while True:
        controller.show_menu()


