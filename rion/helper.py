# pylint: disable-all
# pylint: disable = E, W, R, C

"""
The module does all the things I am too lazy to do. sorry
"""

import ctypes
import hashlib
import os
import os.path
import platform
import subprocess
import uuid
from pathlib import Path

import packaging

from rion.errors import Errors


class Helper:
    """
    Helper Class
    """

    def __init__(self, start):
        """
        Konstruktor
        """
        self.start = start
        self.error = Errors(start)

    @staticmethod
    def testsudo() -> bool:
        """
        Checks if a script was started with admin or root rights.
        """
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin

    @staticmethod
    def os_bindings(path: str) -> str:
        """
        Changes the paths from Linux to Windows.
        It's really only about the backslash.
        """
        if "Windows" in platform.platform():
            return path.replace("/", "\\")

        return path

    @staticmethod
    def uid() -> str:
        """
        Returns a unique random string
        """
        return str(uuid.uuid4()).replace("-", "")

    @staticmethod
    def dimarray(notbeautiful: str) -> list:
        """
        We turn the tuple into a more dimensional array
        """
        notbeautiful = notbeautiful.replace("(", "")[1:-1].replace("'", "")
        return notbeautiful.replace("'", "").split(",")

    @staticmethod
    def check(name: str, version: str, venv: str) -> bool:
        """
        Checks if a package is installed.
        """
        path: str = os.getcwd()
        name = f"{name}_v.{version}"
        if len(venv) == 0:
            venv = "venv"
        pathlib: list[str] = [str(Path.home()), "rion", "node", venv]
        for runner in pathlib:
            os.chdir(runner)
        bondage: bool = os.path.isfile(name)
        os.chdir(path)
        return bondage

    @staticmethod
    def ping(host):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", host]
        return subprocess.call(command) == 0

    @staticmethod
    def name(name: str, version: str) -> str:
        return f"{name}_v{version.replace('v', '')}"

    def read_config(self, modul: str) -> dict:
        """
        Read the config
        """
        # create dict
        user = {"system": "rion"}
        if modul != "installer":
            # go to config file
            path: str = os.getcwd()
            os.chdir(Path.home())
            if not os.path.isdir("rion"):
                self.error.error_message("rion not found")
            os.chdir("rion")
            # open file
            try:
                with open("rion.conf", encoding="utf8") as runner:
                    for line in runner.readlines():
                        # The config has no line breaks
                        line = line.replace(" ", "")
                        # Since the config has no descriptions, each line must have a =.
                        # The Config is not there for decoration but to store values.
                        if "=" not in line:
                            self.error.error_message("Rion ist not installed")
                        # Manipulating the Dictonary through the user configs.
                        line = line.replace("\n", "")
                        line = line.split("=")
                        user[line[0]] = line[1]
                # go back
                os.chdir(path)
            except Exception as error:
                self.error.error_message(str(error))
        return user

    @staticmethod
    def sha256(fname: str) -> None:
        """
        Generate SHA Value of a file
        """
        sha256_hash = hashlib.sha256()
        with open(fname, "rb") as docker:
            for byte_block in iter(lambda: docker.read(4096), b""):
                sha256_hash.update(byte_block)
            print(sha256_hash.hexdigest())

    def name_function(self, content: list[str]) -> dict:
        """
        Return Name
        """
        # Load Package Data
        version: str = ""
        if len(content) != 3:
            name: str = input("Name: ")
            version = input("Version: ")
            venv: str = input("Venv :")
        else:
            name: str = content[0]
            version = content[1]
            venv: str = content[2]
        # Test Package Data
        if 3 >= len(name) >= 30:
            self.error.error_message("Wrong Name Syntax")
        if "." not in version and len(version) <= 3:
            self.error.error_message("wrong Version Syntax")
        if len(venv) == 0:
            venv = "venv"
        # Create Return
        return {"name": name, "version": version, "venv": venv}

    @staticmethod
    def testversion(dummy: dict, idxf: str) -> None:
        """
        Test Version
        """
        if dummy["version"] != idxf:
            Errors.error_message("Wrong Version")

    def compare_version(self, version_one: str, version_two: str) -> int:
        """
        Test two Versions
        """
        # create container
        compare: int = -2
        # Load Version
        version_one = version_one.replace("v", "").replace(" ", "")
        version_two = version_two.replace("v", "").replace(" ", "")
        # Test Version
        if packaging.version.parse(version_one) > packaging.version.parse(version_two):
            compare = 1
        if packaging.version.parse(version_one) < packaging.version.parse(version_two):
            compare = 2
        if packaging.version.parse(version_one) == packaging.version.parse(version_two):
            compare = 0
        if compare == -2:
            self.error.error_message("Comparison is not possible")
        # Return
        return compare

    @staticmethod
    def get_package(name: str, idxf: str, venv: str) -> dict:
        """
        change Data Type
        """
        return {
            "name": name,
            "version": idxf,
            "venv": venv,
        }
