"""
 Start modules for all imports
"""
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np

from rion.errors import Errors
from rion.rion import Rion


def handler() -> None:
    """
    Manages the CL arguments and distributes them to appropriate commands.
    """
    # time Handler
    start = datetime.now()

    # Load Error Object
    errorx = Errors(start)

    if len(sys.argv) >= 2:
        # Deletes the path and the basic command from the array
        command_list = np.delete(np.array(sys.argv), [0, 1])

        # Create a variable that stores the main command.
        loader: str = sys.argv[1]

        # Converts the Numpy array back to a normal list
        flags: object = np.ndarray.tolist(command_list)

        # Create Object
        riox = Rion(flags, loader, start)

        # Set Version
        print("Version: " + str(riox.__version__))

        # Test Version
        invalid_version = False
        if loader == "uninstall":
            riox.uninstall()
        try:
            os.chdir(Path.home())
            os.chdir("rion")
            version_old = ""
            with open("rion.conf", encoding="utf8") as docker:
                for line in docker.readlines():
                    if "version" in line:
                        version_old = line.replace(" ", "").split("=")[1]
                        print(
                            f"Version old:{version_old}\n"
                            f" Version New: {riox.__version__.replace(' ', '')}"
                        )
            if version_old != riox.__version__.replace(" ", ""):
                invalid_version = True
        except OSError:
            time.sleep(1)
        finally:
            if invalid_version:
                errorx.error_message("Invalid Version\nPlease install Rion again")
            # Transfer the NumPy array with all configs to the relevant functions.
            if loader == "install":
                riox.install()
            elif loader == "update":
                riox.update()
            elif loader == "upgrade":
                riox.upgrade()
            elif loader == "version":
                riox.version()
            elif loader == "remove":
                riox.remove()
            elif loader == "search":
                riox.search()
            elif loader == "freeze":
                riox.freeze()
            elif loader == "check":
                riox.check()
            elif loader == "installer":
                riox.installer()
            elif loader == "uninstall":
                riox.uninstall()
            elif loader == "login":
                riox.login()
            elif loader == "server":
                riox.server()
            elif loader == "venv":
                riox.manage_venv()
            elif loader == "info":
                riox.info()
            else:
                # If no command was found, it aborts the program.
                errorx.error_message("no command was found")
    else:
        errorx.error_message("No Input")

    # End Time Managment
    diff = datetime.now() - start
    print(f"run: {diff.total_seconds()}s")
