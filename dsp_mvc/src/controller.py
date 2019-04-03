import sys

from model import Model
from model import Error
from view import View

class Controller:
    """
    """

    def __init__(self, model, view):
        self.__view = view
        self.__model = model

    def start(self):
        while True:
            option = self.__view.show_main_menu()

            if option == 0:
                self.exit_program()
            elif option == 1:
                self.show_current_settings()
            elif option == 2:
                self.set_new_parameters()
            elif option == 3:
                self.show_comb_response()
            elif option == 4:
                self.play_flanger_signal()
            elif option == 5:
                self.show_flanger_signal()
            elif option == 6:
                self.save_current_settings()

    def exit_program(self):
        sys.exit()

    def show_current_settings(self):
        settings = self.__model.get_all_params()
        self.__view.show_current_settings(settings)

    def set_new_parameters(self):
        option, value = self.__view.show_settings_menu()
        error = self.__model.set_param(option, value)
        if error == True:
            self.__view.show_error(Error.get_error_message())
        else:    
            self.__view.show_info("'{}': '{}' updated".format(option, value))

    def show_comb_response(self):
        comb_signal = self.__model.get_comb_signal()
        self.__view.plot_comb_filter(comb_signal)

    def play_flanger_signal(self):
        wav_file = self.__model.get_param(1)[1]
        error, raw_signal = Model.convert_wav_to_raw(wav_file)
        if not error:
            error, flanger_signal = self.__model.get_flanger_signal(raw_signal)
            if not error:
                flanger_wav_file = self.__model.get_param(2)[1]
                Model.save_raw_to_wav(flanger_signal, flanger_wav_file)
                self.__view.play_audio(flanger_wav_file)
            else:
                self.__view.show_error("Error converting flanger wav")
        else:
            self.__view.show_error("Error converting original wav")

    def show_flanger_signal(self):
        pass

    def save_current_settings(self):
        self.__model.save_data_to_db()
    