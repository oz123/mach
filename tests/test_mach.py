#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mach` module."""
import argparse
import cmd
import os
import sys

from unittest import mock


import pytest


from mach import mach1, mach2


import examples
from examples.greet import Hello
from examples.calc import Calculator
from examples.calc2 import Calculator as Calc2
from examples.uftpd import uFTPD


def test_hello():

    hello = Hello()

    assert isinstance(hello.parser, argparse.ArgumentParser)


def test_calc():

    calc = Calculator()

    assert isinstance(calc.parser, argparse.ArgumentParser)


def test_calc2():
    mock_stdin = mock.create_autospec(sys.stdin)
    mock_stdout = mock.create_autospec(sys.stdout)

    calc = Calc2(stdin=mock_stdin, stdout=mock_stdout)

    assert isinstance(calc.parser, argparse.ArgumentParser)
    assert isinstance(calc, cmd.Cmd)

    # https://stackoverflow.com/q/34500249/492620
    # TODO: add assertions here
    calc.add(1, 3)

    # TODO: add assertions here
    calc.do_add(1, 3)

    # TODO: add assertions here
    calc.onecmd('add 1 2')



def test_uftpd():

    uftpd = uFTPD()
    try:
        uftpd.run(['server', '--version'])
    except SystemExit:
        pass

    opts="""--opts={"ftp": 21, "foo": "bar"}"""

    try:
        uftpd.run(['server', opts])
    except SystemExit:
        pass
