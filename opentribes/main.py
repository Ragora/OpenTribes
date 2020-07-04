"""
    Main application entry point.
"""

import os
import sys
import logging
import argparse

import engine

class Application:
    def main(self):
        logger = logging.getLogger("Main")

        parser = argparse.ArgumentParser(description="Run Tribes 2.")
        parser.add_argument("--gamedata", required=False, default=os.path.abspath(sys.argv[0]), type=str, help="The path to the GameData directory.")
        parser.add_argument("--mod", nargs="+", required=False, type=str, default=["base"], help="The mod to run.")
        parser.add_argument("--logLevel", required=False, type=str, default="INFO", choices=["INFO", "DEBUG", "ERROR", "WARNING", "CRITICAL"], help="The log level to use.")
        parser.add_argument("--logFile", required=False, type=str, default=None, help="The log file to write to.")

        arguments = parser.parse_args()

        # Initialize logging before doing anything else
        logging.basicConfig(format="%(asctime)s %(name)s [%(levelname)s]: %(message)s", filemode="w", filename=arguments.logFile, level=getattr(logging, arguments.logLevel))
        logger.info("Log Level: %s", arguments.logLevel)

        if arguments.logFile is not None:
            logger.info("Log File: %s", arguments.logFile)

        # Pass control flow to the engine object
        game = engine.Engine(gamedata=arguments.gamedata, mods=arguments.mod)
        game.start()

if __name__ == "__main__":
    Application().main()
