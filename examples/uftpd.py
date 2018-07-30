#!/usr/bin/env python3
"""
This example demonstrates how one can work with boolean values
and additonal kwargs.


./examples/uftpd.py  server --help
usage: uftpd.py server [-h] [--version] [--syslog] [--foreground]
                       [--level LEVEL] [--opts OPTS]

optional arguments:
  -h, --help     show this help message and exit
  --version      Show the program version and exit (default: False)
  --syslog       Use syslog, even if running in foreground (default: False)
  --foreground   Run in foreground, do not detach from controlling terminal
                 (default: False)
  --level LEVEL  set the verbosity level: none, err, info, notice, debug
                 (default: 2)
  --opts OPTS    Additional options loaded from JSON (default: None)

$ ./examples/uftpd.py --opts='{"ftp": 21}'
serving FTP on port 21

$ ./examples/uftpd.py --opts='{"ftp": 21, "foo": "bar"}'
Unknown option foo given
"""

import sys

from mach import mach1


@mach1()
class uFTPD:

    default = 'server'

    def server(self, level: int=2, foreground: bool=False,
               syslog: bool=False, version: bool=False, **opts):
        """No nonsense TFTP/FTP Server

        level - set the verbosity level: none, err, info, notice, debug
        foreground - Run in foreground, do not detach from controlling terminal
        syslog - Use syslog, even if running in foreground
        version - Show the program version and exit
        opts - ftp=PORT, tftp=PORT


        """
        if version:
            print("uftpd version 0.1")
            sys.exit(0)

        for key in opts:
            if key not in ['ftp', 'tftp']:
                print("Unknown option %s given" % key)
                sys.exit(1)

        print("serving FTP on port %d" % opts['ftp'])


if __name__ == '__main__':
    uFTPD().run()
