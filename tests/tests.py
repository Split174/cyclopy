import unittest
from cc import calc_cyclomatic
import os

class TestCalcMetric(unittest.TestCase):
    def test_icecast_recorder_14(self):
        with open(os.path.dirname(__file__) + "/testsrc/icecast_recorder.py", "r") as file:
            source = file.read()
            visitor = calc_cyclomatic(source)
            self.assertEqual(visitor.metrics, 15)


if __name__ == '__main__':
    unittest.main()