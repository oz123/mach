=====
Usage
=====

``m.a.c.h`` is a single Python module which has two decorators for usages.
The first decorator ``mach1`` turns a normal Python class to a command line
application with subcommand a-la ``git`` or ``docker``. If the application
has no need for subcommand you can simply define a ``default`` subcommand
which will be invoked automatically.

Example ``mach1`` 
-----------------

.. code:: python

   from mach import mach1
   
   
   @mach1
   class Hello:
   
       default = 'greet'
       
       # A doc string should always have a title

       # an empty space
       # name of the option followed by a hyphen
       # short description

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

The ``greet.py`` has two sub-commands ``greet`` and ``part``. You don't
neet to give the ``greet`` sub-command as an argument::

   $ ./examples/greet.py
   Your name: Tom
   Hello Tom
   $

The greet sub-command has two optional arguments which you can also
give in the command line::

   $ ./examples/greet.py greet --name tom --count 3
   Hello tom
   Hello tom
   Hello tom
                                 

The application is automatically documented. The first line of a method docstring is documenting the subcommand::
   
   $ ./examples/greet.py -h
   usage: greet.py [-h] {greet,part} ...

   positional arguments:
     {greet,part}  commands
       greet       Greets a user one or more times
       part        Politely part from a user

   optional arguments:
   -h, --help    show this help message and exit

Using a carefully formatted docstring you can automatically document
the options of your sub-commands. This documentation will be printed
when a sub-command help option is invoked::

   $ ./examples/greet.py greet -h
   usage: greet.py greet [-h] [--name NAME] [--count COUNT]
   
   optional arguments:
     -h, --help     show this help message and exit
     --name NAME    the name of the user to greet (default: )
     --count COUNT  the number of times to greet the user (default: 1)
   
      optional arguments:
     -h, --help     show this help message and exit
     --name NAME    the name of the user to greet (default: )
     --count COUNT  the number of times to greet the user (default: 1)

