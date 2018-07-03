#!/usr/bin/env python3

from mach import mach1


@mach1
class Bolt:
    def __init__(self):
        self.foo = "baz"

    def log(self, conf=None):
        """do something with logs"""
        pass


def main():
    k = Bolt()
    k.run()


if __name__ == '__main__':
    main()
