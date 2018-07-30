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

This example also shows how you can use a special format for the method
docstring to expand the help of subcommands options::

   $ ./examples/greet.py greet -h
usage: greet.py greet [-h] [--name NAME] [--count COUNT]

optional arguments:
  -h, --help     show this help message and exit
  --name NAME    the name of the user to greet (default: )
  --count COUNT  the number of times to greet the user (default: 1)
"""

from mach import mach1


@mach1()
class Hello:

    default = 'greet'

    def greet(self, count: int=1, name: str=""):
        """Greets a user one or more times

        count - the number of times to greet the user
        name - the name of the user to greet
        """

        if not name:
            name = input('Your name: ')

        for c in range(count):
            print("Hello %s" % name)

    def part(self):
        """Politely part from a user"""
        print("It was nice to meet you!")


if __name__ == '__main__':
    Hello().run()
