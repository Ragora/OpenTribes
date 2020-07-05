import lark

# Activate Panda3D's overrides for the Python commands to allow VFS integration when necessary
from direct.stdpy.file import *

def low_level_parse(payload):
    with open("t2ml/t2ml.lark", "r") as handle:
        grammar = handle.read()
    parser = lark.Lark(grammar)
    return parser.parse(payload)

def low_level_parse_file(path):
    with open(path, "r") as handle:
        return low_level_parse(payload=handle.read())
