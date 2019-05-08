import sys
from mach import mach1


@mach1()
class Bolt:
    """
    The main entry point for the program. This class does the CLI parsing
    and descides which action shoud be taken
    """

    def __init__(self):
        self.parser.add_argument("-v", "--verbosity")
        self.parser.add_argument("--version", action='store_true')

        self._verbosity = 1
        self.version = "0.1"

    def _set_verbosity(self, value):
        "set verbosity"
        self._verbosity = value

    def _get_version(self, *args):
        print("This is Bolt version %s" % self.version)
        sys.exit(0)

    def clone(self):
        """clone a site"""
        print("Clonning with verbosity level of %s" % self._verbosity)


if __name__ == '__main__':
    bolt = Bolt()
    bolt.run()
