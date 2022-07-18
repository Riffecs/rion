"""
Rion Class
"""
import glob
import os
import os.path
from pydoc import doc
import shutil
import string
import subprocess
import tarfile
from getpass import getpass
from os.path import exists
from pathlib import Path

from rion.database import Database
from rion.ftp import FTPHandler
from rion.helper import Helper
from contextlib import contextmanager
import sys, os


class Rion:
    """Rion Class"""

    def __init__(self, content="None", start="None") -> None:
        self.rion = Database("rion")
        self.content = content
        self.path_user = str(Path.home())
        self.helper = Helper(start)
        self.path_config = f"{self.path_user}/rion.conf"
        self.path_db = f"{self.path_user}/rion.db"
        self.node = f"{self.path_user}/node"
        self.path = os.getcwd()
        self.table = "INSTALL"
        self.helper = Helper(start)
        self.__version__ = "v0.2.1 - Test".replace(" ", "")

    @contextmanager
    def suppress_stdout():
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:
                yield
            finally:
                sys.stdout = old_stdout

    def dlist(self) -> None:
        """
        Prints all installed packages
        """
        # outputty contains an array of all records from corresponding table
        outputty: list = self.rion.list_table(self.table, "name")
        # Checks if the output is empty
        if len(outputty) == 0:
            self.helper.error.error_message("The database is empty")
        # Set Path
        path_now: str = os.getcwd()
        # Switch to Rion
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # check old lists
        if exists("rion_list.txt"):
            os.remove("rion_list.txt")
        # write new file
        with open("rion_list.txt", encoding="utf8") as docker:
            for runner in outputty:
                docker.write(
                    (
                        str(runner)
                        .replace("(", "")
                        .replace(")", "")
                        .replace("'", "")
                        .replace(" ", "")
                    )
                )
        # Return folder
        os.chdir(path_now)

    def freeze(self) -> None:
        """
        Prints all installed packages
        """
        # outputty contains an array of all records from corresponding table
        outputty: list = self.rion.list_table(self.table, self.table)
        # Checks if the output is empty
        if len(outputty) == 0:
            self.helper.error.error_message("The database is empty")
        else:
            # If it is not empty, then spend it all
            for runner in outputty:
                print(str(runner).replace("(", "").replace(")", "").replace("'", ""))

    def install(self) -> None:
        """
        install packages
        """
        # content = [name, version, venv]
        # User Config
        user: dict = Helper.read_config()
        path: str = os.getcwd()
        content: list = self.content
        self.ftpmodule = "Hallo"
        if len(self.content) == 3:
            venv = self.content = 2
        else:
            venv = "venv"
        try:
            self.ftpmodule = FTPHandler(
                user["server"],
                user["port"],
                user["username"],
                user["password"],
            )
        except Exception:
            self.helper.error.error_message(
                "Missing login credentials. Please enter them in the config file"
            )
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        os.chdir("node")
        if len(content) == 0:
            self.helper.error.error_message(
                "Please provide the name of the package that shall be installed."
            )
        if len(content) == 2:
            venv = "venv"
        else:
            venv = content[2].replace(" ", "")
        os.chdir(venv)
        name = content[0].replace(" ", "")
        version = content[1].replace(" ", "")
        name: str = f"{self.helper.name(name, version,venv)}.tar.gz"
        print(f"\n\n{name}\n\n")
        print("name:", name)
        self.ftpmodule.download(name)
        with tarfile.open(name, "r:gz") as tar:
            tar.extractall()
        os.remove(name)
        os.rename(content[0], self.helper.name(content[0], version))
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # Test
        dummy = f"{content[0]}-v{version}"
        print(f"\nID: {content[0]}-v{version} ")
        print(f"Name: {content[0]}")
        print(f"Version: {version}")
        print(f"Venv: {venv}")
        print(f"Table: {self.table}")
        self.rion.input_value(
            self.table,
            f"('{str(dummy)}', '{str(content[0])}', '{str(version)}','{str(venv)}')",
        )
        # self.rion.input_value(
        #     self.identify,
        #     f"{content[0]}-v{version}, {content[0]}, {str(version)}, {venv}")
        os.chdir(path)

    def installer(self) -> None:
        """
        Rion installer
        """
        # Test Sudo
        # if self.helper.testsudo():
        #    self.helper.error.error_message("Please don't use sudo")
        # To install Rion we go to the user directory.
        os.chdir(self.path_user)
        # We need to check if rion is already installed.
        if os.path.exists("rion"):
            # Since Rion is already installed it cannot be installed again.
            # Therefore, this is canceled.
            self.helper.error.error_message("Rion is already installed.")
        else:
            # We overload the path management
            # with platform specific instances to prevent errors
            os.mkdir(self.helper.os_bindings("rion"))
            os.chdir(self.helper.os_bindings("rion"))
            # Database Management
            self.rion.create_database()
            # Name, Version, Venv
            self.rion.create_table(
                self.table, "id text, name text, version text, venv text"
            )
            # Config Managment
            with open("rion.conf", "w", encoding="utf8") as docker:
                docker.write("conf=rion\n")
                docker.write(f"version={self.__version__}\n")
            # Venv Management
            os.mkdir(self.helper.os_bindings("node"))
            os.chdir("node")
            os.mkdir(self.helper.os_bindings("venv"))
            # Go back to the folder
            os.chdir(self.path)
            # create user
            self.user = {"system": "rion"}

    def login(self) -> None:
        """
        Creates a user in the User Config
        """
        # create Correct list
        correct: str = (
            string.ascii_letters + string.digits + "!#$%&'()*+,-./:;<=>?@[]^_`{|}~"
        )

        # Overload
        if len(self.content) == 2:
            username = self.content[0]
            password = self.content[1]
        else:
            # Reads the username
            username: str = input("Username:")
            # Reads the password
            password = getpass()
            # Checks if the username is long enough
        if len(username) >= 4:
            # Checks if there are any illegal characters in the string
            for runner in username:
                if runner not in correct:
                    self.helper.error.error_message("Wrong Syntax")
        else:
            self.helper.error.error_message("User exist")
        # Checks if the password is long enough
        if len(password) >= 8:
            # Checks if there are any illegal characters in the string
            for runner in password:
                if runner not in correct:
                    self.helper.error.error_message("Wrong Syntax")
        else:
            self.helper.error.error_message("User exist")
        # Load the rion System
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # Change the mode for opening the file
        with open("rion.conf", "a", encoding="utf8") as config:
            # Creates a user in the User Config
            config.write(f"username={username}\n".replace(" ", ""))
            config.write(f"password={password}\n".replace(" ", ""))
        # Goes back to the initial directory
        os.chdir(self.path)

    def remove(self) -> None:
        """
        Remove Package from venv
        """
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # Delete from DB
        name: str = self.content[0]
        version: str = self.content[1]
        self.rion.delete_package(f"{self.table}", f"{name}-v{version}", "id")
        if len(self.content) != 2:
            self.helper.error.error_message("No Userinput")
        print(f"\n\n{name}-v{version}\n\n")
        os.chdir(self.helper.os_bindings("node"))
        os.chdir(self.helper.os_bindings("venv"))
        shutil.rmtree(f"{name}-v{version}")

    def search(self) -> None:
        """
        Search Package in Database
        """
        # Modify Path
        print("\n")
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        for i in self.rion.list_table(self.table, "id"):
            if self.content[0] in i:
                print(i)

    def uninstall(self) -> None:
        """
        Uninstall Rion
        """
        # go to user folder
        os.chdir(self.path_user)
        # checking whether folder exists or not
        try:
            shutil.rmtree("rion")
        except OSError as error_log:
            self.helper.error.error_message(
                f"Rion is not installed\nError: {error_log}"
            )

    def update(self) -> None:
        """
        Load Update File from rion
        """
        user: dict = Helper.read_config()
        path: str = os.getcwd()
        content: list = self.content
        self.ftpmodule = "Hallo"
        try:
            self.ftpmodule = FTPHandler(
                user["server"],
                user["port"],
                user["username"],
                user["password"],
            )
        except Exception:
            self.helper.error.error_message(
                "Missing login credentials. Please enter them in the config file"
            )
        path: str = os.getcwd()
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        if os.path.exists("inor.db"):
            os.remove("inor.db")
        self.ftpmodule.download("inor.db")
        os.chdir(path)

    def upgrade(self) -> None:
        """
        Upgrade Rion packages
        """
        # Change dir
        path: str = os.getcwd()
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # Do Update
        self.update()
        # Load Database
        rion = self.rion
        inor = Database("inor")
        # Load content
        rion_content = rion.list_table(self.table, "name")
        inor_content = inor.list_table(self.table, "name")
        # Loader
        level1 = []
        level2 = []
        for runner in rion_content:
            level1.append(runner)
            level2.append(runner)
        for runner in inor_content:
            level1.append(runner)
            level2.append(runner)
        # Reset Path
        os.chdir(path)

    def server(self) -> None:
        """
        Writes the connection parameters for the server into the Config
        """
        if len(self.content) == 2:
            ipaddresx = self.content[0]
            port = self.content[1]
        else:
            # Reads the server
            ipaddresx: str = input("IP Adresse: ")
            # Read the Port
            port: str = input("Port: ")
        # check IP Adress (Syntax)
        for runner in ipaddresx:
            if runner not in string.digits + ".":
                self.helper.error.error_message("Wrong Syntax")
        # check Port
        if port.replace(" ", "") not in ["22", "21", "2121"]:
            self.helper.error.error_message("Wrong Port")
        # check if server or port exist
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # load conf
        with open("rion.conf", "r", encoding="utf8") as runner:
            for line in runner.readlines():
                if "server" in line:
                    self.helper.error.error_message("Server Exist")
                if "port" in line:
                    self.helper.error.error_message("Port Exist")
        with open("rion.conf", "a", encoding="utf8") as runner:
            runner.write(str(f"server={ipaddresx}\n"))
            runner.write(str(f"port={port}\n"))

    def version(self) -> None:
        """
        Upgrade Rion Version
        """
        if not Helper.testsudo():
            subprocess.run("pip install -U rion", check=True)
        else:
            self.helper.error.error_message(
                "Please execute the command with admin rights."
            )

    def manage_venv(self) -> None:
        """
        create a new venv
        """
        # Modify Path
        path = os.getcwd()
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # Test Command
        # content = [ command , name ]
        if len(self.content) != 2:
            command = input("Command: ")
            if command == "list":
                os.chdir("node")
                for runner in os.listdir("."):
                    print(runner)
                sys.exit(0)
            venv = input("Venv: ")
        else:
            os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
            command = self.content[0]
            if command == "list":
                for runner in os.listdir("."):
                    print(runner)
            venv = self.content[1]
        # Test content
        for runner in venv:
            if runner not in string.ascii_letters:
                self.helper.error.error_message("Wrong Venv Syntax")
        if command not in ["create", "list", "remove"]:
            self.helper.error.error_message("Commands:  create, list, remove")
        os.chdir(self.helper.os_bindings("node"))
        # Execute Command
        if command == "create":
            try:
                os.mkdir(self.helper.os_bindings(venv))
            except OSError as error:
                self.helper.error.error_message(
                    f"The Venv already exists\nError: {error}"
                )
        elif command == "remove":
            try:
                shutil.rmtree(venv)
            except OSError as error:
                self.helper.error.error_message(
                    f"The Venv cannot delete.\nError:{error}"
                )
        os.chdir(path)

    def info(self) -> None:
        """
        Load Infos from Metadata
        """
        # Modify Path
        path = os.getcwd()
        os.chdir(self.helper.os_bindings(f"{self.path_user}/rion"))
        # Create Package
        package: dict = self.helper.name_function(self.content)
        # go in venv
        os.chdir(self.helper.os_bindings("node"))
        os.chdir(self.helper.os_bindings(package["venv"]))
        try:
            os.chdir(
                self.helper.os_bindings(
                    self.helper.name(package["name"], package["version"])
                )
            )
        except OSError as error:
            self.helper.error.error_message(
                f"Package ist not installed.\nError: {error}"
            )
        # Serch File in package
        path_to_meta: list[str] = [].append(glob.glob("rev_info.txt"))
        # Check if no file find
        if len(path_to_meta) == 0:
            self.helper.error.error_message("No Info File found")
        # Read Info file (Overload)
        meta: str = path_to_meta[0]
        with open(meta, "r", encoding="utf-8") as docker:
            lines = [_.rstrip("\n") for _ in docker.readlines()]
        for docker in lines:
            print(docker)
        os.chdir(path)
