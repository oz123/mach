========
M.A.C.H
========
.. image:: https://readthedocs.org/projects/mach/badge/?version=latest
   :target: http://mach.readthedocs.io/en/latest/?badge=latest
.. image:: https://travis-ci.org/oz123/mach.svg?branch=master
   :target: https://travis-ci.org/oz123/mach
.. image:: https://coveralls.io/repos/github/oz123/mach/badge.svg?branch=master
   :target: https://coveralls.io/github/oz123/mach?branch=master

Magical Argparse Command Helper

.. image:: https://raw.githubusercontent.com/oz123/mach/master/imgs/mach-logo.jpg


Features
--------

 * Get your CLI interfaces quickly
 * Turn a simple class to a CLI application or an interactive interpreter.


Given:

.. code:: python

  class Calculator:

      def add(self, a, b):
          """adds two numbers and prints the result"""
          return a + b

      def div(self, a, b):
          """divide one number by the other"""
          return a / b

You can make command line application using the decorator ``mach1``:

.. code:: python

   from mach import mach1

   @mach1()
   class Calculator:

       def add(self, int: a, int: b):
           """adds two numbers and prints the result"""
          print(a + b)

       def div(self, int: a, int: b):
           """divide one number by the other"""
          print(a / b)


   calc = Calculator()

   calc.run()

Now if you run the module, you will get a program that you can invoke with
the flag ``-h`` or ``--help``:

.. code:: shell

   $ python calc.py -h
   usage: calc.py [-h] {add,div} ...

   positional arguments:
   {add,div}   commands

      add       adds two numbers and prints the result
      div       divide one number by the other

   optional arguments:
     -h, --help  show this help message and exit


each method is a subcommand, with type checking and it's own very help.
Hench, this won't work:

.. code:: shell

   $ python calc.py add foo bar
   usage: calc.py add [-h] b a
   calc.py add: error: argument b: invalid int value: 'foo'

And this will:

.. code:: shell

   $ python calc.py add 4 9
   13

To see the help of the subcommand use ``-h``:

.. code:: shell

   $ python calc.py add -h
   usage: calc.py add [-h] b a

   positional arguments:
    b
    a

   optional arguments:
     -h, --help  show this help message and exit

With the help of the decorator ``mach2`` you can turn your class to CLI
application and have also an iteractive shell which invoke when no
parameters are given:

.. code:: shell

   $ ./examples/calc2.py
   Welcome to the calc shell. Type help or ? to list commands.

   calc2 > ?

   Documented commands (type help <topic>):
   ========================================
   add  div  exit  help

   calc2 > help add
   adds two numbers and prints the result
   calc2 > add 2 4
   6
   calc2 > div 6 2
   3.0
   calc2 > exit
   Come back soon ...
   $

Installation
------------

You can get mach from PyPI using pip::

   $ pip install mach.py
