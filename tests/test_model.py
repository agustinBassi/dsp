import os
import sys
import unittest

from src.model import Configuration
from src.model import CombFilter
from src.model import FlangerFilter
from src.model import WahWahFilter
from src.model import Model


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


class TestFlangerFilter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.flanger = FlangerFilter(2.0, 3.0, 4.0)

    def tearDown(self):
        pass

    def test_repr(self):
        expected_text = "{'max_delay: '2.0000'," \
            "'scale': '3.00', 'rate': '4.00'}"
        self.assertEqual(repr(self.flanger), expected_text)

    def test_str(self):
        expected_text = 'FlangerFilter(max_delay = 2.0000 seg, ' \
                        'scale = 3.00, rate = 4.00)'
        self.assertEqual(str(self.flanger), expected_text)

    def test_apply_filter(self):
        pass

    def test_max_delay(self):
        self.flanger.max_delay = 2.2
        self.assertEqual(self.flanger.max_delay, 2.2)

    def test_scale(self):
        self.flanger.scale = 3.3
        self.assertEqual(self.flanger.scale, 3.3)

    def test_rate(self):
        self.flanger.rate = 4.4
        self.assertEqual(self.flanger.rate, 4.4)


class TestModel(unittest.TestCase):

    ERROR_FIXTURE_PATH = "error_fixture_path"
    CORRECT_FIXTURE_PATH = "/tests/fixtures/fixture_config.ini"

    @classmethod
    def setUpClass(cls):
        TestModel.config_file = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
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
        error_flag = False
        try:
            model = Model(TestModel.ERROR_FIXTURE_PATH)
            model.load_data_from_db()
        except:
            error_flag = True
        finally:
            self.assertEqual(error_flag, True)
            del(model)

        # passing an valid path and check if return error = false
        error_flag = False
        try:
            model = Model(TestModel.config_file)
            model.load_data_from_db()
        except:
            error_flag = True
        finally:
            self.assertEqual(error_flag, False)
            del(model)

    def test_save_data_to_db(self):
        # passing an invalid path and check if return error = true
        error_flag = False
        try:
            model = Model(TestModel.ERROR_FIXTURE_PATH)
            model.save_data_to_db()
        except:
            error_flag = True
        finally:
            self.assertEqual(error_flag, True)
            del(model)

        # passing an valid path and check if return error = false
        error_flag = False
        try:
            model = Model(TestModel.config_file)
            # model.save_data_to_db()
        except:
            error_flag = True
        finally:
            self.assertEqual(error_flag, False)
            del(model)

    def test_get_all_params(self):
        default_params_text = \
            "\t- 'config.welcome_message': 'DSP Controller!'\n" \
            "\t- 'config.wav_original': 'wavs/guitars.wav'\n" \
            "\t- 'config.wav_modified': 'wavs/audio_modified.wav'\n" \
            "\t- 'comb.delay': 8\n" \
            "\t- 'comb.scale': 1.00\n" \
            "\t- 'flanger.max_delay': 0.003\n" \
            "\t- 'flanger.scale': 1.00\n" \
            "\t- 'flanger.rate': 0.50\n" \
            "\t- 'wahwah.damping': 0.05\n" \
            "\t- 'wahwah.min_cutoff': 300\n" \
            "\t- 'wahwah.max_cutoff': 3000\n" \
            "\t- 'wahwah.frequency': 0.40\n"

        # set this value to check grater values than default
        self.maxDiff = None
        # passing an invalid path and check if return error = true
        try:
            model = Model(TestModel.ERROR_FIXTURE_PATH)
            model.load_data_from_db()
        except:
            pass
        finally:
            self.assertEqual(model.get_all_params(), default_params_text)
            del(model)

    def test_get_param_incorrects(self):
        values_to_test = ["a", 2.1, ["a", "b"], ("a", "b"), {"a": "b"},
                          {"a", "b"}, -1, 100]

        model = Model(TestModel.config_file)

        # test option from every value_to_test
        for i in range(len(values_to_test)):
            # get_param start from 1 to get values
            value = model.get_param(values_to_test[i])
            self.assertEqual(value, None)

    def test_get_param_corrects(self):
        values_to_test = ("DSP Controller!", "wavs/guitars.wav", "wavs/guitars_filtered.wav",
                          8, 1.0,
                          0.005, 0.5, 1.0,
                          0.05, 500, 3000, 0.5)

        model = Model(TestModel.config_file)
        model.load_data_from_db()

        # test option from every value_to_test
        for i in range(len(values_to_test)):
            # get_param start from 1 to get values
            value = model.get_param(i + 1)
            self.assertEqual(value, values_to_test[i])

    def test_set_param_incorrects(self):
        values_to_test = (2, 2, 2, 
                          "2", 2, 
                          "2", 2, 2,
                          2, "2", "2", 2)

        model = Model(TestModel.config_file)
        model.load_data_from_db()

        # test option from every value_to_test
        for i in range(len(values_to_test)):
            # get_param start from 1 to get values
            error_flag = model.set_param(i + 1, values_to_test[i])
            self.assertEqual(error_flag, True)

    def test_set_param_corrects(self):
        values_to_test = ("a", "a", "a", 
                          50, 50.1, 
                          0.01, 0.5, 2.5,
                          0.05, 500, 3500, 0.5)

        model = Model(TestModel.config_file)

        # test option from every value_to_test
        for i in range(len(values_to_test)):
            # get_param start from 1 to get values
            error_flag = model.set_param(i + 1, values_to_test[i])
            self.assertEqual(error_flag, False)
            value = model.get_param(i + 1)
            self.assertEqual(value, values_to_test[i])

    def test_comb_signal(self):
        comb_filter = CombFilter(8, 1.0)
        comb_signal = comb_filter.get_response_in_frecuency()

        model = Model(TestModel.config_file)
        comb_signal_model = model.get_comb_signal()

        self.assertEqual(comb_signal_model.all(), comb_signal.all())

    def test_flanger_signal(self):
        model = Model(TestModel.config_file)
        original_wav_path = model.get_parent_dir() + "/wavs/guitars.wav"
        fs, original_signal = Model.convert_wav_to_raw(original_wav_path)

        flanger_filter = FlangerFilter(0.005, 0.5, 1.0)
        flanger_signal = flanger_filter.apply_filter(original_signal, fs)

        model_flanger_signal = model.get_flanger_signal(original_signal, fs)

        self.assertEqual(model_flanger_signal.all(), flanger_signal.all())

    def test_wahwah_signal(self):
        model = Model(TestModel.config_file)
        original_wav_path = model.get_parent_dir() + "/wavs/guitars.wav"
        fs, original_signal = Model.convert_wav_to_raw(original_wav_path)

        wahwah_filter = WahWahFilter(0.05, 300, 3000, 0.4)
        wahwah_signal = wahwah_filter.apply_filter(original_signal, fs)

        model_wahwah_signal = model.get_flanger_signal(original_signal, fs)

        # self.assertEqual(model_wahwah_signal.all(), wahwah_signal.all())

    def test_get_parent_dir(self):
        model = Model(TestModel.config_file)
        test_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_parent_dir = model.get_parent_dir()

        self.assertEqual(test_parent_dir, model_parent_dir)
