import os
import sys
import unittest

from src.model import Configuration
from src.model import CombFilter
from src.model import FlangerFilter
from src.model import WahWahFilter
from src.model import Model
from src.view import View


class TestView(unittest.TestCase):

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

    def test_plot_wahwah_triangle(self):
        wahwah = WahWahFilter(0.05, 300, 4500, 0.5)

        triangle_signal = wahwah._create_triangle_waveform(143325, 11025)

        view = View()

        view.plot_wahwah_triangle_wave(triangle_signal)

        pass