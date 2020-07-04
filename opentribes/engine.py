"""
    Main engine definition.
"""

import os
import io
import typing
import logging
import zipfile

import panda3d.core
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.stdpy.file import *

from . import loaders, t2ml

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

    __runtime: typing.Optional[str] = None
    """
        The path to the OpenTribes runtime directory.
    """

    __cache: typing.Optional[str] = None
    """
        The path to the cache directory.
    """

    __mounted_mods: typing.Optional[typing.List[str]] = None
    """
        A list of currently mounted mod names.
    """

    def __init__(self, runtime: str, cache:str, gamedata: str, mods: typing.List[str]):
        """
            Initializes a new engine instance.

            :param runtime: The path to the OpenTribes runtime directory.
            :param cache: The path to the cache directory.
            :param gamedata: The path to the gamedata directory to use.
            :param mods: The list of mods to mount. These should just be the names of the directories
                underneath of gamedata. Mods will be mounted in the order they are specified, with any
                duplications ignored.
        """
        ShowBase.__init__(self)

        self.__cache = os.path.abspath(cache)
        self.__mods = [os.path.basename(mod) for mod in mods]
        self.__gamedata = os.path.abspath(gamedata)
        self.__runtime = os.path.abspath(runtime)

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

    def extract_vl2(self, mod: str, absolute_path: str) -> str:
        """
            Extracts the Vl2 specified at absolute_path for the mod to the cache directory.
            This is necessary because Panda will only mount VFS entries that are either multifiles
            or directories.

            :param mod: The name of the mod this is for.
            :param absolute_path: The absolute path to the VL2 in question.

            :return: The path to the resulting directory to mount in the VFS.
        """
        logger = logging.getLogger("Engine:ExtractVL2")
        logger.info("Converting VL2 at absolute path %s for mod %s.", absolute_path, mod)

        filename, _ = os.path.splitext(os.path.basename(absolute_path))

        output_directory = os.path.join(self.__cache, mod)
        output_vl2_path = os.path.join(output_directory, filename)

        logger.debug("Output VL2 path: %s", output_vl2_path)

        # Create the directory structure if necessary
        os.makedirs(output_vl2_path, exist_ok=True)

        with zipfile.ZipFile(absolute_path) as zip_handle:
            zip_handle.extractall(path=output_vl2_path)
        return output_vl2_path

    def resolve_vl2_directory(self, mod: str, absolute_path: str) -> typing.Optional[str]:
        """
            Helper function to resolve the extract directory for the specified mod
            and VL2, if it exists.

            :param mod: The name of the mod this is for.
            :param absolute_path: The absolute path to the VL2 in question.

            :return: A path to the VL2 mount directory if it exists. None otherwise.
        """
        filename, _ = os.path.splitext(os.path.basename(absolute_path))

        output_directory = os.path.join(self.__cache, mod)
        output_vl2_path = os.path.join(output_directory, filename)

        if os.path.exists(output_vl2_path) is True:
            return output_vl2_path
        return None

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

        vfs = panda3d.core.VirtualFileSystem.getGlobalPtr()

        # Load in a known order every time to avoid problems caused by the operating system returning the list in different orders
        logger.info("Scanning VL2s ...")
        for candidate in sorted(os.listdir(absolute_mod_path)):
            candidate = os.path.join(absolute_mod_path, candidate)

            if os.path.isfile(candidate):
                _, extension = os.path.splitext(candidate)
                extension = extension.lower()

                if extension == ".vl2":
                    vl2_name = os.path.basename(candidate)
                    logger.info("Mounting VL2: %s", vl2_name)
                    logger.debug("Mounting VL2 at path: %s", candidate)

                    # Resolve mount directory and if necessary, perform an extract
                    vl2_directory = self.resolve_vl2_directory(mod=mod, absolute_path=candidate)
                    if vl2_directory is None:
                        vl2_directory = self.extract_vl2(mod=mod, absolute_path=candidate)

                    # Once processed, mount the directory
                    if vl2_directory is None:
                        logger.critical("Failed to extract VL2 %s!", vl2_name)
                        continue

                    logger.debug("VL2 extracted path: %s", vl2_directory)
                    if vfs.mount(panda3d.core.Filename(vl2_directory), ".", panda3d.core.VirtualFileSystem.MFReadOnly) is False:
                        logger.critical("Failed to mount VL2 at VFS path: %s", vl2_directory)

    def start(self):
        """
            Starts the engine and takes control flow for the duration of the application.
        """
        logger = logging.getLogger("Engine:Run")
        logger.info("Initializing engine ...")
        logger.info("Runtime directory: %s", self.__runtime)
        logger.info("Gamedata directory: %s", self.__gamedata)
        logger.info("Cache Directory: %s", self.__cache)
        logger.info("Mods: %s", ", ".join(self.__mods))
        logger.debug("Loader instance: %s", self.loader)

        # opentribes.t2ml.parser.low_level_parse_file("draakan.txt")
        logger.info("Mounting runtime directory")

        vfs = panda3d.core.VirtualFileSystem.getGlobalPtr()
        vfs.mount(panda3d.core.Filename(self.__runtime), ".", panda3d.core.VirtualFileSystem.MFReadOnly)

        for mod in self.__mods:
            self.mount_mod_directory(mod=mod)

        window_properties = WindowProperties()
        window_properties.setTitle("Tribes 2")
        window_properties.setIconFilename("base/Tribes2.ico")
        self.win.requestProperties(window_properties)

        # Finally let Panda3D take over from here
        logger.info("Starting engine!")
        self.run()
