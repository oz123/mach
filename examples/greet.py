#!/usr/bin/env python3
"""
This example demonstrates how one can define a default subcommand
which is invoked if no other subcommand is given::

   $ ./examples/greet.py -h
   usage: greet.py [-h] {greet,part} ...

   positional arguments:
     {greet,part}  commands
       greet       Greets a user one or more times
       part        Politely part from a user

   optional arguments:
  -h, --help    show this help message and exit
   $ ./examples/greet.py greet --name Tom
   Hello Tom
   $ ./examples/greet.py
   Your name: Tom
   Hello Tom
   $


"""
from mach import mach1


@mach1
class Hello:

    default = 'greet'

    def greet(self, count: int=1, name: str=""):
        "Greets a user one or more times"
        if not name:
            name = input('Your name: ')

        for c in range(count):
            print("Hello %s" % name)

    def part(self):
        "Politely part from a user"
        print("It was nice to meet you!")


Hello().run()
