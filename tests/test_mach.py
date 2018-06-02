#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mach` module."""
import argparse
import cmd

from io import StringIO
from unittest import mock


import pytest


from examples.greet import Hello
from examples.calc import Calculator
from examples.calc2 import Calculator as Calc2
from examples.uftpd import uFTPD
from examples.lftp import FTPClient


def test_hello():

    hello = Hello()

    assert isinstance(hello.parser, argparse.ArgumentParser)


def test_calc():

    calc = Calculator()

    assert isinstance(calc.parser, argparse.ArgumentParser)


def test_calc2():

    calc = Calc2()

    assert isinstance(calc.parser, argparse.ArgumentParser)
    assert isinstance(calc, cmd.Cmd)

    # https://stackoverflow.com/q/34500249/492620
    with mock.patch('sys.stdout', new=StringIO()) as fakeOutput:
        calc.add(1, 3)
        assert '1 + 3 => 4' == fakeOutput.getvalue().strip()

    with mock.patch('sys.stdout', new=StringIO()) as fakeOutput:
        calc.do_add(1, 3)
        assert '1 + 3 => 4' == fakeOutput.getvalue().strip()

    with mock.patch('sys.stdout', new=StringIO()) as fakeOutput:
        calc.onecmd('add 1 2')
        assert '1 + 2 => 3' == fakeOutput.getvalue().strip()


def test_calc2_no_interactive():
    calc = Calc2()

    # this is ./examples/calc2.py add 2 4
    with mock.patch('sys.stdout', new=StringIO()) as fakeOutput:
        calc._run1(["add", "2", "4"])
        assert '4 + 2 => 6' == fakeOutput.getvalue().strip()


def test_uftpd():

    uftpd = uFTPD()
    try:
        uftpd.run(['server', '--version'])
    except SystemExit:
        pass

    opts = """--opts={"ftp": 21, "foo": "bar"}"""

    try:
        uftpd.run(['server', opts])
    except SystemExit:
        pass


@pytest.mark.parametrize(
    "input,output",
    [("connect foo.example.com 21", "Connected to foo.example.com:21"),
     ("connect foo.example.com", "Connected to foo.example.com:21"),
     ("connect foo.bar.com port=2121", "Connected to foo.bar.com:2121"),
     ('connect ftp.example.com 21 opts={"user": oz123, "password":s3kr35}',
      "Could not parse JSON in opts"),
     (('connect ftp.example.com 21'
       ' opts=\'{"user": "oz123", "password":"s3kr35"}\''),
      'Connected to ftp.example.com:21\nLogin success ...'),
     ("login foo s3kr35", "Login success ..."),
     ('""', '*** Unknown syntax: ""'),
     ("login foo bar bla", "*** Unknown syntax: login foo bar bla"),
     ("moo", "*** Unknown syntax: moo"),
     ("ls", "Files in /"),
     ("ls /foo/", "Files in /foo/"),
     ("help", """Documented commands (type help <topic>):
========================================
connect  exit  help  login  ls"""),
     ("connect foo=21", "Unknown option foo"),
     ("""connect foo.example.com 21 opts='{"user": "oz123", "password": "s3kr35"}""",
      """connect foo.example.com 21 opts='{"user": "oz123", "password": "s3kr35"}: No closing quotation"""),
])
def test_lftp(input, output):
    ftpc = FTPClient(stdout=StringIO())

    ftpc.onecmd(input)
    assert ftpc.stdout.getvalue().strip() == output

