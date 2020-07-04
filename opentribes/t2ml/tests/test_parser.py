import os
import unittest
import pkg_resources

import panda3d.core

# Activate Panda3D's overrides for the Python commands to allow VFS integration when necessary
from direct.stdpy.file import *

import opentribes

class TestParser(unittest.TestCase):
    def setUp(self):
        """
            Setup function called by unittest to bootstrap all tests. This is necessary here to configure
            Panda3D's VFS to work in the test environment.
        """

        # Find the module location and mount the opentribes subdirectory to .
        module_path = pkg_resources.require("opentribes")[0].module_path
        vfs = panda3d.core.VirtualFileSystem.getGlobalPtr()
        vfs.mount(panda3d.core.Filename(os.path.join(module_path, "opentribes")), ".", panda3d.core.VirtualFileSystem.MFReadOnly)

    def test_basic(self):
        with open("t2ml/tests/draakan.txt", "r") as handle:
            payload = handle.read()
        result = opentribes.t2ml.parser.low_level_parse(payload)
