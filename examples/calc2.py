#!/usr/bin/env python3
"""
This example demonstrate how decorating with `mach1`
turns your class into a command line application, which also
has it's own REPL::

   $ ./examples/calc2.py add 4 1
   1 + 4 => 5

   $ ./examples/calc2.py
   Welcome to the calc shell. Type help or ? to list commands.

   calc2 > add 4 1
   4 + 1 => 5
   calc2 > exit
   Come back soon ...
"""

import sys

from mach import mach2

class HelperClass:

    def _excluded_method(self):
        """
        This method is 'private'. It's name starts with _.
        Thus, this method does not get a public command line interface
        """
        print("This will not be shown")


@mach2(explicit=True)
class Calculator(HelperClass):

    def add(self, a: int, b: int):
        """adds two numbers and prints the result"""
        print("%s + %s => %d" % (a, b, int(a) + int(b)))

    def div(self, a: int, b: int):
        """divide one number  by the other"""
        print("%s / %s => %d" % (a, b, int(a) // int(b)))

    def exit(self):
        """exist to finish this session"""
        print("Come back soon ...")
        sys.exit(0)


if __name__ == '__main__':
    calc = Calculator()
    calc.intro = 'Welcome to the calc shell. Type help or ? to list commands.\n'
    calc.prompt = 'calc2 > '
    calc.run()
