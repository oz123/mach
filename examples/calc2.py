#!/usr/bin/env python3
import sys

from mach import mach2


@mach2
class Calculator:

    def add(self, a: int, b: int):
        """adds two numbers and prints the result"""
        print(int(a) + int(b))

    def div(self, a: int, b: int):
        """divide one number  by the other"""
        print(int(a) / int(b))

    def exit(self, args):
        """exist to finish this session"""
        print("Come back soon ...")
        sys.exit(0)


calc = Calculator()
calc.intro = 'Welcome to the calc shell. Type help or ? to list commands.\n'
calc.prompt = 'calc2 > '

calc.run()
