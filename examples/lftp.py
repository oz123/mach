#!/usr/bin/env python3
# demonstrate how to enable only shell

import sys

from mach import mach2

@mach2
class FTPClient:

    def login(self, user: str, password: str):
        """login to the FTP server"""

        print(user, password)

    def connect(self, host: str, port: int=21):
        """connect to FTP host

        host - the host IP or fqdn
        port - the port listening to FTP
        """
        pass

    def ls(self):
        """list files in the current directory"""
        pass

    def exit(self):
        """exit the program"""
        sys.exit(0)

if __name__ == '__main__':
    ftpclient = FTPClient()
    ftpclient.intro = 'Welcome to the lftp client. Type help or ? to list commands.\n'
    ftpclient.prompt = 'lftp > '

    ftpclient.cmdloop()
