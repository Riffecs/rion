"""
 Start modules for all imports
"""
import sys
from datetime import datetime

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
    errorx = Errors()

    if len(sys.argv) >= 2:
        # Deletes the path and the basic command from the array
        command_list = np.delete(np.array(sys.argv), [0, 1])

        # Create a variable that stores the main command.
        loader: str = sys.argv[1]

        # Converts the Numpy array back to a normal list
        flags: object = np.ndarray.tolist(command_list)

        # Create Object
        riox = Rion(flags, loader)

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
            riox.venv()
        else:
            # If no command was found, it aborts the program.
            errorx.error_message("no command was found")
    else:
        errorx.error_message("no input")

    # End Time Managment
    diff = datetime.now() - start
    print(f"run: {diff.total_seconds()}s")
