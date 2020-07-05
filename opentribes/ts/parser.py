import lark

# Activate Panda3D's overrides for the Python commands to allow VFS integration when necessary
from direct.stdpy.file import *

def low_level_parse(payload):
    with open("ts/torque.lark", "r") as handle:
        grammar = handle.read()
    parser = lark.Lark(grammar)
    return parser.parse(payload)

def low_level_parse_file(path: str) -> lark.Tree:
    """
        Performs a Torque Script parse on the file at the specified path, returning the resulting
        parse tree unmodified.

        :param path: The path to the file to execute.

        :raises lark.exceptions.LarkError: Raised when an error has occurred during parse.
    """
    with open(path, "r") as handle:
        return low_level_parse(payload=handle.read())
