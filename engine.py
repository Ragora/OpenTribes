"""
    Main engine definition.
"""

import os
import typing
import logging

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

import loaders

class Engine(ShowBase):
    """
        Main engine class. This class will perform any initializations necessary for the Tribes 2 game to run.
    """

    __gamedata: typing.Optional[str] = None
    """
        The absolute path to the gamedata directory.
    """

    __mods: typing.Optional[typing.List[str]] = None
    """
        A list of all active mod names.
    """

    __mounted_mods: typing.Optional[typing.List[str]] = None
    """
        A list of currently mounted mod names.
    """

    def __init__(self, gamedata: str, mods: typing.List[str]):
        """
            Initializes a new engine instance.

            :param gamedata: The path to the gamedata directory to use.
            :param mods: The list of mods to mount. These should just be the names of the directories
                underneath of gamedata. Mods will be mounted in the order they are specified, with any
                duplications ignored.
        """
        ShowBase.__init__(self)

        self.__mods = [os.path.basename(mod) for mod in mods]
        self.__gamedata = os.path.abspath(gamedata)

        if os.path.exists(self.__gamedata) is False:
            raise ValueError("Gamedata path '%s' does not exist." % gamedata)

        # Base must exist in the gamedata directory
        if os.path.exists(os.path.join(self.__gamedata, "base")) is False:
            raise ValueError("base mod does not exist in gamedata path '%s'." % self.__gamedata)

        # Ensure base is the first mod
        if self.__mods[0] != "base":
            self.__mods = ["base"] + self.__mods

        # Set working dir to the gamedata directory
        os.chdir(self.__gamedata)

    def mount_mod_directory(self, mod: str):
        """
            Mounts a mod directory to the engine instance.

            :param mod: The mod name contained within gamedata to mount.
        """
        mod = os.path.basename(mod)

        logger = logging.getLogger("Engine:MountMod")
        logger.debug("Mounting mod: %s", mod)

        absolute_mod_path = os.path.join(self.__gamedata, mod)

        logger = logging.getLogger("Engine:MountMod:%s" % mod)
        logger.debug("Mod absolute path: %s", absolute_mod_path)

        if os.path.exists(absolute_mod_path) is False:
            logger.error("Path for mod %s does not exist. Ignoring.", mod)
            return

        # FIXME: Is there a known mount order of VL2s here? Alphabetical order or something?
        logger.info("Scanning VL2s ...")
        for candidate in os.listdir(absolute_mod_path):
            candidate = os.path.join(absolute_mod_path, candidate)

            if os.path.isfile(candidate):
                _, extension = os.path.splitext(candidate)
                extension = extension.lower()

                if extension == ".vl2":
                    vl2_name = os.path.basename(candidate)
                    logger.info("Mounting VL2: %s", vl2_name)
                    logger.critical("ZIP virtual file systems needs implemented for this to work!")

    def start(self):
        """
            Starts the engine and takes control flow for the duration of the application.
        """
        logger = logging.getLogger("Engine:Run")
        logger.info("Initializing engine ...")
        logger.info("Gamedata directory: %s", self.__gamedata)
        logger.info("Mods: %s", ", ".join(self.__mods))
        logger.debug("Loader instance: %s", self.loader)

        for mod in self.__mods:
            self.mount_mod_directory(mod=mod)

        window_properties = WindowProperties()
        window_properties.setTitle("Tribes 2")
        window_properties.setIconFilename("base/Tribes2.ico")
        self.win.requestProperties(window_properties)

        # Finally let Panda3D take over from here
        self.run()
