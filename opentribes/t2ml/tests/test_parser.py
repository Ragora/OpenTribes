import unittest
import pkg_resources

import opentribes

class TestParser(unittest.TestCase):
    def test_basic(self):
        payload = pkg_resources.resource_string(__name__, "draakan.txt")
        result = opentribes.t2ml.parser.low_level_parse(payload.decode("utf-8"))
