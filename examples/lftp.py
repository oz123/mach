#!/usr/bin/env python3
# demonstrate how to enable only shell

import sys

from mach import mach2

@mach2()
class FTPClient:

    def login(self, user: str, password: str):
        """login to the FTP server"""

        self.stdout.write("Login success ...\n")

    def connect(self, host: str, port: int=21, **opts):
        """connect to FTP host

        host - the host IP or fqdn
        port - the port listening to FTP
        """
        self.stdout.write("Connected to %s:%s\n" % (host, port))

        if opts:
            self.login(**opts)

    def ls(self, dir: str="/"):
        """list files in dir"""
        self.stdout.write("Files in %s\n" % dir)

    def exit(self):
        """exit the program"""
        sys.exit(0)

if __name__ == '__main__':
    ftpclient = FTPClient()
    ftpclient.intro = 'Welcome to the lftp client. Type help or ? to list commands.\n'
    ftpclient.prompt = 'lftp > '

    ftpclient.run()
