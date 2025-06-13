#!/usr/bin/env python3

import os
import sys
import argparse
from collections import OrderedDict

argp = argparse.ArgumentParser()
argp.add_argument('-c', '--chdir', help='Change to directory before preprocessing')
argp.add_argument('FILE', help='File to preprocess')
opts = argp.parse_args()

class PreProcessor:
    def __init__(self):
        self.defines = OrderedDict()

    def order_defines_by_length(self):
        self.defines = OrderedDict(sorted(self.defines.items(), key=lambda i: len(i[0]), reverse=True))

    def include_files(self, file):
        with open(file, 'r', encoding='UTF-8') as fh:
            lines = fh.readlines()

            for line in lines:

                if line.startswith("#include"):
                    file = line.replace('#include', '').strip()
                    self.include_files(file)
                    continue

                if line.startswith("#define"):
                    line = line.replace('#define', '').strip()
                    macro, value = line.split(' ', maxsplit=1)
                    self.defines[macro] = value.strip()
                    self.order_defines_by_length()
                    continue

                if line.lstrip().startswith('#'):
                    continue

                for macro, value in self.defines.items():
                    line = line.replace(macro, value)

                print(line, end='')

if opts.chdir:
    os.chdir(opts.chdir)

pp = PreProcessor()
pp.include_files(opts.FILE)
