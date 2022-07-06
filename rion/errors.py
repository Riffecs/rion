"""
    Short Error Class
"""

import sys
from datetime import datetime

from termcolor import colored


class Errors:
    """
    Short Error Class
    """

    def __init__(self, start) -> None:
        """
        Konstruktor
        """
        self.start = start

    def error_message(self, text: str) -> None:
        """
        Resume an error
        """
        print(colored(text, "red"))
        diff = datetime.now() - self.start
        print(f"run: {diff.total_seconds()}s")
        sys.exit(0)
