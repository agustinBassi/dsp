import os
import sys
import unittest

from src.model import Configuration
from src.model import FlangerFilter
from src.model import CombFilter
from src.model import Model
from src.model import Error

class TestConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.config = Configuration("a", "b", "c")

    def tearDown(self):
        pass

    def test_repr(self):
        expected_text = "{'welcome_message': 'a', 'wav_original': 'b', " \
                        "'wav_modified': 'c'}"
        self.assertEqual(repr(self.config), expected_text)

    def test_str(self):
        expected_text = "Configuration(welcome_message = a, wav_original " \
                        "= b, wav_modified = c)"
        self.assertEqual(str(self.config), expected_text)

    def test_welcome_message(self):
        self.config.welcome_message = "aa"
        self.assertEqual("aa", self.config.welcome_message)

    def test_wav_original(self):
        self.config.wav_original = "bb"
        self.assertEqual("bb", self.config.wav_original)

    def test_wav_modified(self):
        self.config.wav_modified = "cc"
        self.assertEqual("cc", self.config.wav_modified)

class TestFlangerFilter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.flanger = FlangerFilter(1, 2.0, 3.0, 4.0)

    def tearDown(self):
        pass

    def test_repr(self):
        expected_text = "{'fs': '1', 'max_delay: '2.0000'," \
                "'scale': '3.00', 'rate': '4.00'}"
        self.assertEqual(repr(self.flanger), expected_text)

    def test_str(self):
        expected_text = 'FlangerFilter(fs = 1 hz, max_delay = 2.0000 seg, ' \
                        'scale = 3.00, rate = 4.00)'
        self.assertEqual(str(self.flanger), expected_text)

    def test_apply_filter(self):
        pass

    def test_fs(self):
        self.flanger.fs = 11
        self.assertEqual(self.flanger.fs, 11)
    
    def test_max_delay(self):
        self.flanger.max_delay = 2.2
        self.assertEqual(self.flanger.max_delay, 2.2)

    def test_scale(self):
        self.flanger.scale = 3.3
        self.assertEqual(self.flanger.scale, 3.3)

    def test_rate(self):
        self.flanger.rate = 4.4
        self.assertEqual(self.flanger.rate, 4.4)

class TestCombFilter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.comb = CombFilter(1, 2.0)

    def tearDown(self):
        pass

    def test_repr(self):
        expected_text = "{'delay': '1', 'scale: '2.00'}"
        self.assertEqual(repr(self.comb), expected_text)

    def test_str(self):
        expected_text = "CombFilter(delay = 1 samples, scale = 2.00)"
        self.assertEqual(str(self.comb), expected_text)

    def test_delay(self):
        self.comb.delay = 11
        self.assertEqual(self.comb.delay, 11)

    def test_scale(self):
        self.comb.scale = 2.2
        self.assertEqual(self.comb.scale, 2.2)

class TestError(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_error_message(self):
        Error.set_error_message("Error 1")
        self.assertEqual(Error.get_error_message(), "Error 1")

        Error.set_error_message("Error 2")
        self.assertNotEqual(Error.get_error_message(), "Error 1")

class TestModel(unittest.TestCase):

    ERROR_FIXTURE_PATH = "error_fixture_path"
    CORRECT_FIXTURE_PATH = "/tests/fixtures/fixture_config.ini"

    @classmethod
    def setUpClass(cls):
        TestModel.config_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        TestModel.config_file += TestModel.CORRECT_FIXTURE_PATH

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_data_from_db(self):
        # passing an invalid path and check if return error = true
        model = Model(TestModel.ERROR_FIXTURE_PATH)
        error_flag = model.load_data_from_db()
        self.assertEqual(error_flag, True)
        del(model)

        # passing an valid path and check if return error = false
        model = Model(TestModel.config_file)
        error_flag = model.load_data_from_db()
        self.assertEqual(error_flag, False)
        del(model)

    def test_save_data_to_db(self):
        # passing an invalid path and check if return error = true
        model = Model(TestModel.ERROR_FIXTURE_PATH)
        model.load_data_from_db()
        error_flag = model.save_data_to_db()
        self.assertEqual(error_flag, True)
        del(model)

        # passing an valid path and check if return error = false
        model = Model(TestModel.config_file)
        model.load_data_from_db()
        error_flag = model.save_data_to_db()
        self.assertEqual(error_flag, False)
        del(model)

    def test_get_all_params(self):
        success_text = \
            "\t- 'config.welcome_message': 'DSP Controller!'\n" \
            "\t- 'config.wav_original': 'wavs/tone_1khz.wav'\n" \
            "\t- 'config.wav_modified': 'wavs/tone_1khz_modified.wav'\n" \
            "\t- 'comb.delay': 8\n" \
            "\t- 'comb.scale': 1.00\n" \
            "\t- 'flanger.fs': 44101\n" \
            "\t- 'flanger.max_delay': 0.007\n" \
            "\t- 'flanger.scale': 0.54\n" \
            "\t- 'flanger.rate': 2.51\n"
        error_text = \
            "\t- 'config.welcome_message': 'DSP Controller!'\n" \
            "\t- 'config.wav_original': 'wavs/tone_1khz.wav'\n" \
            "\t- 'config.wav_modified': 'wavs/tone_1khz_modified.wav'\n" \
            "\t- 'comb.delay': 8\n" \
            "\t- 'comb.scale': 1.00\n" \
            "\t- 'flanger.fs': 44100\n" \
            "\t- 'flanger.max_delay': 0.003\n" \
            "\t- 'flanger.scale': 0.50\n" \
            "\t- 'flanger.rate': 1.00\n"

        model = Model(TestModel.config_file)
        error_flag = model.load_data_from_db()
        if error_flag:
            self.assertEqual(model.get_all_params(), error_text)
        else:
            self.assertEqual(model.get_all_params(), success_text)
        del(model)

        model = Model(TestModel.ERROR_FIXTURE_PATH)
        error_flag = model.load_data_from_db()
        if error_flag:
            self.assertEqual(model.get_all_params(), error_text)
        else:
            self.assertEqual(model.get_all_params(), success_text)
        del(model)

    def test_get_param_incorrects(self):
        values_to_test = ["a", 2.1, ["a", "b"], ("a", "b"), {"a": "b"},
                          {"a", "b"}, -1, 100]  

        model = Model(TestModel.config_file)

        # test option from every value_to_test
        for i in range (len(values_to_test)):
            # get_param start from 1 to get values
            error_flag, _ = model.get_param(values_to_test[i])
            self.assertEqual(error_flag, True)

    def test_get_param_corrects(self):
        values_to_test = ("DSP Controller!", 
                          "wavs/tone_1khz.wav", 
                          "wavs/tone_1khz_modified.wav", 
                          8, 1.0, 
                          44100, 0.003, 0.5, 1.0)

        model = Model(TestModel.ERROR_FIXTURE_PATH)

        # test option from every value_to_test
        for i in range (len(values_to_test)):
            # get_param start from 1 to get values
            error_flag, value = model.get_param(i + 1)
            self.assertEqual(error_flag, False)
            self.assertEqual(value, values_to_test[i])
        
    def test_set_param_incorrects(self):
        values_to_test = (2, 2, 2, "2", 2, "2", 2, 2, 2)

        model = Model(TestModel.config_file)

        # test option from every value_to_test
        for i in range (len(values_to_test)):
            # get_param start from 1 to get values
            error_flag = model.set_param(i + 1, values_to_test[i])
            self.assertEqual(error_flag, True)    

    def test_set_param_corrects(self):
        values_to_test = ("a", "a", "a", 123, 1.1, 123, 1.1, 1.1, 1.1)

        model = Model(TestModel.ERROR_FIXTURE_PATH)

        # test option from every value_to_test
        for i in range (len(values_to_test)):
            # get_param start from 1 to get values
            error_flag = model.set_param(i + 1, values_to_test[i])
            self.assertEqual(error_flag, False)
            error_flag, value = model.get_param(i + 1)
            self.assertEqual(error_flag, False)
            self.assertEqual(value, values_to_test[i])

    def test_comb_signal(self):
        comb_filter = CombFilter(8, 1)
        comb_signal = comb_filter.get_response_in_frecuency()

        model = Model(TestModel.ERROR_FIXTURE_PATH)
        comb_signal_model = model.get_comb_signal()

        self.assertEqual(comb_signal_model.all(), comb_signal.all())



### TODO SECTION

# TODO testear flanger
# TODO testear los metodos que faltan en model
