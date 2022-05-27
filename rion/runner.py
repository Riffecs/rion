"""
    This is where the real magic happens
"""
import os
from pathlib import Path


from riontest import crypt
from riontest import db
from riontest import errors
from riontest import helper


def install(content: list) -> None:
    """
    install a package
    """
    for runner in content:
        print(runner)


def update(content: list) -> None:
    """
    updates the package list
    """
    # No control argument is used for updating the list

    if content:
        # That's actually terrible semantics. But I can't change that right now.
        errors.neednoargs()
    else:
        print("do update")


def upgrade(content: list) -> None:
    """
    updates the package list
    """
    for runner in content:
        print(runner)


def search(content: list) -> None:
    """
    Rion is now looking for packages
    """
    for runner in content:
        print(runner)


def remove(content: list) -> None:
    """
    Rion remove packages
    """
    for runner in content:
        print(runner)


def dlist(content: list) -> None:
    """
    Rion list packages
    """
    for runner in content:
        print(runner)


def freeze(content: list) -> None:
    """
    Rion freeze packages
    """
    for runner in content:
        print(runner)


def check(content: list) -> None:
    """
    Rion check packages
    """
    # TODO: Check config file
    print(content)


def config(content: list) -> None:
    """
    Rion config packages
    """
    for runner in content:
        print(runner)


def init() -> None:
    """
    Load install skript
    """

    # OS Path Modul
    path: str = helper.os_bindings(f"{os.path.expanduser('.')}/rion")
    Path(path).mkdir(parents=True, exist_ok=True)

    # Change base
    os.chdir(path)

    # Install config
    with open("config.txt", "w", encoding="utf8") as docker:
        docker.write("rion_conf\n")

    # Install Database
    db.create_database("Packages")
    db.create_table("Packages", "Package", "name text, version text")

    # Load Cipher
    key = crypt.gen_key()

    # Safe Key
    key = crypt.gen_key_as_string(key)

    # write key in conf
    with open("config.txt", "a", encoding="utf8") as docker:
        docker.write(f"key={key}\n")

    # Install Venv Manager
    with open("venv.txt", "w", encoding="utf8") as docker:
        docker.write("Venv Manager\n")

    # setup root venv
    path += helper.os_bindings("/venv/node")
    Path(path).mkdir(parents=True, exist_ok=True)

    # write rion as root venv
    with open("venv.txt", "a", encoding="utf8") as docker:
        docker.write("/node/pdk\n")
