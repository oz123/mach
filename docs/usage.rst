=====
Usage
=====

``m.a.c.h`` is a single Python module which has two decorators for usages.
The first decorator ``mach1`` turns a normal Python class to a command line
application with subcommand a-la ``git`` or ``docker``. If the application
has no need for subcommands you can simply define a ``default`` subcommand
which will be invoked automatically.

Example ``mach1``
-----------------

.. code:: python

   from mach import mach1


   @mach1()
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

   ./examples/greet.py greet -h
   usage: greet.py greet [-h] [--name NAME] [--count COUNT]

   optional arguments:
     -h, --help            show this help message and exit
     --name NAME, -n NAME  the name of the user to greet (default: )
     --count COUNT, -c COUNT
                           the number of times to greet the user (default: 1)

Also note, that the automatically added options support both long and short
variants. Hence, these invocataions are possible::

   ./examples/greet.py -c 3 -n Tom
   ./examples/greet.py --count 3 -n Tom
   ./examples/greet.py --count 3 --name Tom
   ./examples/greet.py -c 3 --name --Tom

Advanced ``mach1`` with default values and JSON parsing
-------------------------------------------------------

You can write methods with default values or with a certain number
of open options as in ``**kwargs`` passed to a Python method:

See ``examples/uftpd.py`` for an implementation of a hypothetical
FTP server example.

You can invoke this ftp server with::

   $ ./examples/uftpd.py --foreground --level 3

This will run the server in the foreground with a verbosity level 3.

   $ ./examples/uftpd.py --opts='{"ftp": 21}'
   serving FTP on port 21

``opts`` is automatically parsed as JSON. The server will run in
the background and a verbosity level of 2.

Using ``mach2``
---------------

The decorator ``mach2`` adds on top of ``mach1`` all the existing
capabilities, the ability to turn a class to an interactive interpreter.
The most simple interactive interpreter is a command line calculator:

.. code:: python

   import sys

   from mach import mach2

   @mach2()
   class Calculator:

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

You can invoke this application via the command line by giving a
sub-command::

   $ ./examples/calc2.py add 5 6
   6 + 5 => 11

Or start an interactive session by not giving any sub-command::

   $ ./examples/calc2.py
   Welcome to the calc shell. Type help or ? to list commands.

   calc2 >

You can now type a command in the interactive interpreter::

   calc2 > add 7 3
   7 + 3 => 10
   calc2 > div 16 8
   16 / 8 => 2

As with ``mach1`` doc-strings are used to documented your application
functionality::

   calc2 > help div
   divide one number  by the other
   calc2 > help add
   adds two numbers and prints the result


Advanced ``mach1`` with default values and JSON parsing
-------------------------------------------------------

A simple calculator does not all the features ``mach2`` offers.
A better example is a hypothetical ``FTP`` client.

See ``examples/lftp.py``.

Once started it waits for user input at the ``lftp`` prompt::

   $ ./examples/lftp.py
   Welcome to the lftp client. Type help or ? to list commands.

   lftp > help

   Documented commands (type help <topic>):
   ========================================
   connect  exit  help  login  ls

   lftp > help connect
   connect to FTP host

   host - the host IP or fqdn
   port - the port listening to FTP

Typing the ``help`` command will list the available commands.
Typing ``help connect`` lists the arguments that the command
``connect`` gets, by parsing the method's docstring.

Since this command can now be invoked in any of the following ways::

   lftp > connect 10.10.192.192
   Connected to 10.10.192.192:21

   lftp > connect host=foo.example.com port=21
   Connected to foo.example.com:21

   lftp > connect foo.example.com 2121
   Connected to foo.example.com:2121

   lftp > connect foo.example.com 21 opts='{"user": "oz123", "password": "s3kr35"}'
   Connected to foo.example.com:21
   Login success ...

The last invocation also shows that you can pass extra arguments as JSON.

The interpreter is checking how you invoke the commands. Hence this all don't work::

   lftp > connect foo 2121 bar
   *** Unknown syntax: connect foo 2121 bar
   lftp > help login
   login to the FTP server
   lftp > login oz123 s3kr35
   Login success ...
   lftp > login foobar secret error
   *** Unknown syntax: login foobar secret error


Explicit shell or implicit shell using `mach2`
----------------------------------------------

The example `calc2.py` and `lftp` have an implicit shell option.
That is, if the program called with out arguments it will start an interactive
shell session, like the Python interpreter itself.

However, you might not desire this behaviour. Instead you prefer an explicit argument
for a shell invocation. If so, you can simply decorate your class with:

.. code:: python

   @mach2(explicit=True)
   class Calculator:

       def add(self, a: int, b: int):
           """adds two numbers and prints the result"""
           print("%s + %s => %d" % (a, b, int(a) + int(b)))

       ...


Now, and interactive shell option is added::

   $ ./examples/calc2.py -h
   usage: calc2.py [-h] [--shell] {add,div,exit} ...

   positional arguments:
     {add,div,exit}  commands
       add           adds two numbers and prints the result
       div           divide one number by the other
       exit          exist to finish this session

   optional arguments:
     -h, --help      show this help message and exit
     --shell         run an interactive shell (default: False)
   $ ./examples/calc2.py --shell
   Welcome to the calc shell. Type help or ? to list commands.

   calc2 >

Inheritence and 'private' methods
---------------------------------

The examples shown above always create a command line interface from
all methods defined in a class. So if we have a class which inherits
methods from another class, all methods will have a 'public' command
line interface:

.. code:: python

   class Foo:
        def foo(self):
            pass
        def bar(self):
            pass

   @mach1()
   class Baz(Foo)
       def do(self):
           pass


This a will create a command line interface for `do` but also
for `foo` and `bar`. This can be avoided by naming the class method
with a leading underscore `_`:

.. code:: python

   class Foo:
        def _foo(self):
            pass
        def _bar(self):
            pass

   @mach1()
   class Baz(Foo)
       def do(self):
           self._foo()

This creats a command line interface only for `do`, and the 'private'
methods are hidden.

Extra long help for subcommands
-------------------------------

You can use an extended help format for subcommands. Just add `---`
after describing the options of each subcommand. Below these `---`
you can add a longer text which will be shown next to each subcommand.
This is demonstated by the example `uftpd2.py`:

.. code:: shell

   ./examples/uftpd2.py -h
   usage: uftpd2.py [-h] {server} ...

   positional arguments:
     {server}    commands
       server    No nonsense TFTP/FTP Server. add some long test below these
                 three dashes

   optional arguments:
     -h, --help  show this help message and exit

