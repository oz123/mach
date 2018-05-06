import argparse
import inspect
import json
import shlex

from cmd import Cmd
from itertools import filterfalse, tee


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

        arg = shlex.split(arg)
        arg, args_with_val = partition(lambda x: "=" in x, arg)
        di = {}
        for item in args_with_val:
            name, val = item.split('=')
            di[name] = val

        try:
            func = getattr(self, 'do_' + cmd)
        except AttributeError:
            return self.default(line)

        sig = inspect.getfullargspec(func)

        if sig.varkw:
            try:
                kwargs = json.loads(di.pop(sig.varkw))
                di.update(kwargs)
            except json.decoder.JSONDecodeError:
                pass
        try:
            return func(*arg, **di)
        except ValueError:
            return self.default(line)

        except TypeError:
            pass

        # Cmd methods except one arg
        try:
            return func("")
        except TypeError:
            return self.default(line)


_supported_types = {'str': str, 'float': float, 'int': int}


def add_parsers(name, function, doc, sig, subparsers):

    subp = subparsers.add_parser(
        name, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help=doc)

    idx_args_with_defaults = len(sig.defaults) if sig.defaults else 0

    if sig.defaults:
        _defaults = list(reversed(sig.defaults))

    for idx, val in enumerate(reversed(sig.args[1:])):
        subpargs, opts = [], {}
        type_ = sig.annotations.get(val)
        if type_ and type_.__name__ == 'bool':
            opts['action'] = "store_true"
        elif type_ and type_.__name__ in _supported_types:
                opts['type'] = _supported_types[type_.__name__]
        if idx_args_with_defaults and idx < idx_args_with_defaults:
            opts['default'] = _defaults[idx]
            # opts['help'] = "default: %s" % opts['default'] if opts['default'] else ""
            subpargs.append("--" + val)
        else:
            subpargs.append(val)

        subp.add_argument(*subpargs, **opts)
    if sig.varkw:
        subp.add_argument("--" + sig.varkw,
                          help="Additional options loaded from JSON")

    return name, function, doc


def _mach(kls, add_do=False):

    if hasattr(kls, 'default'):
        parser = DefaultSubcommandArgParse(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    else:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(help='commands', dest="cmd")

    if add_do:
        do_kls = type(kls.__name__, (Mach, kls), {})

    for (name, function) in inspect.getmembers(kls,
                                               predicate=inspect.isfunction):
        doc = inspect.getdoc(function)
        sig = inspect.getfullargspec(function)
        add_parsers(name, function, doc, sig, subparsers)

        if add_do:
            setattr(do_kls, "do_%s" % name, function)

    if hasattr(kls, 'default'):
        parser.set_default_subparser(kls.default)

    if add_do:
        kls = do_kls

    kls.parser = parser
    return kls


def _run1(inst):
    p = inst.parser.parse_args()

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


def _run2(inst):
    if not inst._run1():
        inst.cmdloop()


def mach1(kls):
    kls = _mach(kls)
    kls.run = _run1
    return kls


def mach2(kls):
    kls = _mach(kls, add_do=True)
    kls._run1 = _run1
    kls.run = _run2
    return kls
