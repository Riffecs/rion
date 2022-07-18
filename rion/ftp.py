# pylint: disable-all
# pylint: skip-file
"""
simple FTP Handler
"""
from ftplib import FTP_TLS
import ssl


class FTPHandler:
    """
    simple FTP Handler
    """

    def __init__(
        self,
        server: str = "None",
        port: str = "None",
        user: str = "None",
        pwd: str = "None",
    ):
        """
        Konstruktor
        """
        self.server = server
        self.port = port
        self.user = user
        self.pwd = pwd

    def download(self, file: str) -> None:
        """
        Download an File from a FTP Server
        @param file:
        @return:
        """
        ftp = FTP_TLS()
        ftp.ssl_version = ssl.PROTOCOL_SSLv23
        ftp.debugging = 2
        ftp.connect(self.server, int(self.port))
        ftp.login(self.user, self.pwd)
        ftp.retrbinary("RETR " + file, open(file, "wb").write)
