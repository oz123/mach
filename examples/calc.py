#!/usr/bin/env python3

from mach import mach1


@mach1
class Calculator:

    def add(self, a: int, b: int):
        """adds two numbers and prints the result"""
        print(int(a) + int(b))

    def div(self, a: int, b: int):
        """divide one number by the other"""
        print(int(a) / int(b))


calc = Calculator()

calc.run()
