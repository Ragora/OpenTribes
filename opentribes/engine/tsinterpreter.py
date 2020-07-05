import logging

import lark
import direct.stdpy.file

from ..ts import parser

class TSInterpreter:
    """
        Class representing an instance of the Torque Script interpreter.
    """

    __engine = None

    def __init__(self, engine):
        """
            Initializes an instance of TSInterpreter.
        """
        self.__engine = engine

    def exec_file(self, path: str, vfs: bool = True) -> bool:
        """
            Requests the interpreter to execute the file at the specified path.

            :param path: The absolute path to the file to execute.
            :param vfs: If True, the path is handled using the VFS. False is used for unrestricted filesystem
                loading for files such as console_start.cs.

            :return: True if execution was successful. False otherwise.
        """
        logger = logging.getLogger("TSInterpreter:Exec")

        description = "with vfs" if vfs else "WITHOUT vfs"
        logger.debug("Attempting execute of file %s %s", path, description)

        open_function = direct.stdpy.file.open if vfs else open

        try:
            with open_function(path, "r") as handle:
                payload = handle.read()
            tree = parser.low_level_parse(payload)
        except lark.exceptions.LarkError as error:
            logger.error("Failed to exec file %s: %s", path, error)
            return False
        except FileNotFoundError:
            logger.error("Could not find file for exec: %s", path)
            return False
        return True
