#!/usr/bin/env python3
"""
This example demonstrate how decorating with `mach1`
turns your class into a command line application.


   $ ./examples/calc.py add 2 4
   4 + 2 => 6
   $ ./examples/calc.py div 2 4
   4 / 2 => 2
"""

from mach import mach1


@mach1()
class Calculator:

    def add(self, a: int, b: int):
        """adds two numbers and prints the result"""
        print("%s + %s => %d" % (a, b, int(a) + int(b)))

    def div(self, a: int, b: int):
        """divide one number by the other"""
        print("%s / %s => %d" % (a, b, int(a) // int(b)))


if __name__ == '__main__':

    calc = Calculator()
    calc.run()
