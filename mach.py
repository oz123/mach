"""
This file is part of m.a.c.h.

m.a.c.h is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

m.a.c.h is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with m.a.c.h.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import inspect
import json
import pkg_resources
import shlex

from cmd import Cmd
from itertools import filterfalse, tee

try:
    __version__ = pkg_resources.get_distribution('pwman3').version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    __version__ = "0.0.1"


def partition(pred, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return list(filterfalse(pred, t1)), list(filter(pred, t2))


class DefaultSubcommandArgParse(argparse.ArgumentParser):
    # https://stackoverflow.com/a/37593636/492620
    __default_subparser = None

    def set_default_subparser(self, name):
        self.__default_subparser = name

    def _parse_known_args(self, arg_strings, *args, **kwargs):
        in_args = set(arg_strings)
        d_sp = self.__default_subparser
        if d_sp is not None and not {'-h', '--help'}.intersection(in_args):
            for x in self._subparsers._actions:
                subparser_found = (
                    isinstance(x, argparse._SubParsersAction) and
                    in_args.intersection(x._name_parser_map.keys())
                )
                if subparser_found:
                    break
            else:
                # insert default in first position, this implies no
                # global options without a sub_parsers specified
                arg_strings = [d_sp] + arg_strings
        return super(DefaultSubcommandArgParse, self)._parse_known_args(
            arg_strings, *args, **kwargs
        )


class Mach(Cmd):

    def onecmd(self, line):
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)

        try:
            arg = shlex.split(arg)
        except ValueError as e:
            self.stdout.write(line + ": %s\n" % e)
            return

        arg, args_with_val = partition(lambda x: "=" in x, arg)
        di = {}

        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            # when a method is not found
            return self.default(line)

        sig = inspect.getfullargspec(func)
        for item in args_with_val:
            name, val = item.split('=')
            if name != sig.varkw and name not in sig.args[1:]:
                self.stdout.write("Unknown option %s\n" % name)
                return
            di[name] = val

        if sig.varkw and sig.varkw in di:
            try:
                kwargs = json.loads(di.pop(sig.varkw))
                di.update(kwargs)
            except json.decoder.JSONDecodeError:
                self.stdout.write("Could not parse JSON in %s\n" % sig.varkw)
                return

        try:
            return func(*arg, **di)
        except ValueError:
            # when a method is wrongly used
            return self.default(line)

        except TypeError as e:
            if e.args[0].endswith(
                    "missing 1 required positional argument: 'arg'"):
                return func("")
            else:
                return self.default(line)


_supported_types = {'str': str, 'float': float, 'int': int}


def parse_docs(docstring):
    """
    Parse documentation string and create a help string
    """

    doc = docstring.split("\n")
    doc_dict = {'cmd': doc[0]}
    if len(doc) > 1:
        doc = {k: v for k, v in
               (item.split(' - ') for item in
                list(filter(lambda x: x, doc))[1:])}
        doc_dict.update(doc)
    return doc_dict


def add_parsers(name, function, doc, sig, subparsers):

    subp = subparsers.add_parser(
        name, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help=doc['cmd'])

    idx_args_with_defaults = len(sig.defaults) if sig.defaults else 0

    if sig.defaults:
        _defaults = list(reversed(sig.defaults))

    for idx, val in enumerate(reversed(sig.args[1:])):
        subpargs, opts = [], {}
        opts['help'] = doc.get(val, '')
        type_ = sig.annotations.get(val)
        if type_ and type_.__name__ == 'bool':
            opts['action'] = "store_true"
        elif type_ and type_.__name__ in _supported_types:
                opts['type'] = _supported_types[type_.__name__]
        if idx_args_with_defaults and idx < idx_args_with_defaults:
            opts['default'] = _defaults[idx]
            if len(val) == 1:
                subpargs.append("-" + val)
            else:
                subpargs.append("--" + val)
                subpargs.append("-" + val[0])
        else:
            subpargs.append(val)

        subp.add_argument(*subpargs, **opts)
    if sig.varkw:
        subp.add_argument("--" + sig.varkw,
                          help="Additional options loaded from JSON")

    return name, function, doc


def create_helper(doc, name):
    return lambda name: print(doc)


def not_private(x):
    """find all methods which do not have a name which starts with _"""
    try:
        return not x.__name__.startswith("_") and inspect.isfunction(x)
    except:
        return False


def _mach(kls, add_do=False, explicit=True, auto_help=True):

    if hasattr(kls, 'default'):
        parser = DefaultSubcommandArgParse(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    else:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    if explicit:
        parser.add_argument("--shell",
                            action='store_true',
                            help="run an interactive shell")

    subparsers = parser.add_subparsers(help='commands', dest="cmd")

    if add_do:
        do_kls = type(kls.__name__, (Mach, kls), {})

    for (name, function) in inspect.getmembers(kls,
                                               predicate=not_private):
        _d = inspect.getdoc(function)
        doc = parse_docs(_d)
        sig = inspect.getfullargspec(function)
        add_parsers(name, function, doc, sig, subparsers)

        if add_do:
            setattr(do_kls, "do_%s" % name, function)
            setattr(do_kls, "help_%s" % name, create_helper(_d, name))

    if hasattr(kls, 'default'):
        parser.set_default_subparser(kls.default)

    if add_do:
        kls = do_kls

    parser.auto_help = auto_help
    kls.parser = parser
    return kls


def _run1(inst, args=None):
    p = inst.parser.parse_args(args=args)

    if getattr(p, 'shell', False):
        inst.cmdloop()
        return True

    if p.cmd:
        func_args_kwargs = inspect.getfullargspec(getattr(inst, p.cmd))
        args = func_args_kwargs.args
        args.pop(args.index("self"))
        if func_args_kwargs.varkw:
            kwargs = getattr(p, func_args_kwargs.varkw)
            if kwargs:
                kwargs = json.loads(kwargs)
            else:
                kwargs = {}
            func = getattr(inst, p.cmd)
            func(*(getattr(p, arg) for arg in args), **kwargs)
        else:
            func = getattr(inst, p.cmd)
            func(*(getattr(p, arg) for arg in args))
            return True

    elif inst.parser.auto_help:
        inst.parser.print_help()


def _run2(inst):  # pragma: no coverage
    if not inst._run1() and (
            '--shell' not in inst.parser._option_string_actions):
        inst.cmdloop()


def mach1(auto_help=True):  # pragma: no coverage

    def real_decorator(callable_, *args, **kwargs):

        def wrapper(*args, **kwargs):
            kls = _mach(callable_, explicit=False, auto_help=auto_help)
            kls.run = _run1
            return kls(*args, **kwargs)

        return wrapper

    return real_decorator


def mach2(explicit=False):

    def real_decorator(callable_, *args, **kwargs):

        def wrapper(*args, **kwargs):
            kls = _mach(callable_, add_do=True, explicit=explicit)
            kls._run1 = _run1
            kls.run = _run2
            return kls(*args, **kwargs)

        return wrapper

    return real_decorator
