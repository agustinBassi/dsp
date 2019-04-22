import sys

from model import Model
from view import View


class Controller:
    """
    """

    def __init__(self, model, view):
        self.__view = view
        self.__model = model
        try:
            self.__model.load_data_from_db()
            self.__view.show_info("DB data loaded correctly")
        except:
            self.__view.show_error("Error while loading db file for model")

    def start(self):
        while True:
            option = self.__view.show_main_menu()

            if option == 0:
                self.op0_exit_program()
            elif option == 1:
                self.op1_show_current_settings()
            elif option == 2:
                self.op2_set_new_parameters()
            elif option == 3:
                self.op3_save_current_settings()
            elif option == 4:
                self.op4_plot_comb_response()
            elif option == 5:
                self.op5_plot_flanger_signal()
            elif option == 6:
                self.op6_plot_wahwah_triangle_signal()
            elif option == 7:
                self.op7_plot_wahwah_filter()
            elif option == 8:
                self.op8_play_original_signal()
            elif option == 9:
                self.op9_play_flanger_signal()
            elif option == 10:
                self.op10_play_wahwah_signal()
            elif option == 11:
                self.op11_play_flanger_wahwah_signal()
            elif option == 12:
                self.op12_restore_default_values()
            

    def op0_exit_program(self):
        self.__view.show_info("Exiting from DSP Controller...")
        sys.exit()

    def op1_show_current_settings(self):
        settings = self.__model.get_all_params()
        self.__view.show_current_settings(settings)

    def op2_set_new_parameters(self):
        option, value = self.__view.show_settings_menu()
        error = self.__model.set_param(option, value)
        if error:
            self.__view.show_error("Option '{}' or value '{}' invalid".format(option, value))
        else:
            self.__view.show_info("'{}': '{}' updated".format(option, value))

    def op3_save_current_settings(self):
        try:
            self.__model.save_data_to_db()
            self.__view.show_info("Data correctly saved into DB")
        except:
            self.__view.show_error("Error while saving current data into DB")

    def op4_plot_comb_response(self):
        comb_signal = self.__model.get_comb_signal()
        self.__view.show_info("Plotting comb signal")
        self.__view.plot_comb_filter(comb_signal)

    def op5_plot_flanger_signal(self):
        wav_original = self.__model.get_param(2)

        if wav_original != None:
            wav_original_abs_path = self.__model.get_parent_dir() + "/" + wav_original

            fs, raw_original = Model.convert_wav_to_raw(wav_original_abs_path)
            raw_modified = self.__model.get_flanger_signal(raw_original, fs)

            self.__view.show_info("Plotting flanger signals")
            self.__view.plot_flanger_signals(raw_original, raw_modified)

        else:
            self.__view.show_error("Index 2 for obtain wavs original is incorrect")

    def op6_plot_wahwah_triangle_signal(self):
        self.__view.show_info("Plot wahwah triangle signal")

    def op7_plot_wahwah_filter(self):
        self.__view.show_info("Plot wahwah filter signal")

    def op8_play_original_signal(self):
        wav_original = self.__model.get_param(2)
        if wav_original != None:
            wav_original_abs_path = self.__model.get_parent_dir() + "/" + wav_original
            try:
                self.__view.play_audio(wav_original_abs_path)
            except:
                self.__view.show_error("Impossible play: %s" % wav_original_abs_path)
        else:
            self.__view.show_error("The index 2 for obtain original wav is incorrect")

    def op9_play_flanger_signal(self):
        wav_original_abs_path = self.__model.get_parent_dir() + "/" + \
                                self.__model.get_param(2)
        wav_modified_abs_path = self.__model.get_parent_dir() + "/" + \
                                self.__model.get_param(3)
        try:
            fs, raw_original = Model.convert_wav_to_raw(wav_original_abs_path)
            raw_modified = self.__model.get_flanger_signal(raw_original, fs)
            try:
                Model.save_raw_to_wav(raw_modified, wav_modified_abs_path, fs)
                self.__view.play_audio(wav_modified_abs_path)
            except:
                self.__view.show_error("Error converting or playing flanger signal wav")
        except:
            self.__view.show_error("Error getting original signal or flanger signal")

    def op10_play_wahwah_signal(self):
        self.__view.show_info("Play wahwah wav audio")

    def op11_play_flanger_wahwah_signal(self):
        self.__view.show_info("Play flanger & wahwah concatenated wav audio")

    def op12_restore_default_values(self):
        self.__view.show_info("op12_restore_default_values")


    
