#!/usr/bin/env python3

import os
import sys
import argparse
from collections import OrderedDict

argp = argparse.ArgumentParser()
argp.add_argument('-c', '--chdir', help='Change to directory before preprocessing')
argp.add_argument('-d', '--define', help='Define a macro', action='append')
argp.add_argument('FILE', help='File to preprocess')
opts = argp.parse_args()

class PreProcessor:
    def __init__(self):
        self.defines = OrderedDict()
        self.condition_stack = []

    def order_defines_by_length(self):
        self.defines = OrderedDict(sorted(self.defines.items(), key=lambda i: len(i[0]), reverse=True))

    def define(self, macro, value):
        self.defines[macro] = value
        self.order_defines_by_length()

    def include_files(self, file):
        with open(file, 'r', encoding='UTF-8') as fh:
            lines = fh.readlines()

            i = 0
            while i < len(lines):
                line = lines[i]

                # Handle #include
                if line.startswith("#include"):
                    file_to_include = line.replace('#include', '').strip()
                    self.include_files(file_to_include)
                    i += 1
                    continue

                # Handle #define
                elif line.startswith("#define"):
                    line = line.replace('#define', '').strip()
                    if ' ' in line:
                        macro, value = line.split(' ', maxsplit=1)
                    else:
                        macro, value = line, ''
                    self.defines[macro] = value.strip()
                    self.order_defines_by_length()
                    i += 1
                    continue

                # Handle #ifndef
                elif line.startswith("#ifndef"):
                    macro = line[len("#ifndef"):].strip()
                    self.condition_stack.append(macro not in self.defines)
                    i += 1
                    continue

                # Handle #ifeq MACRO VALUE
                elif line.startswith("#ifeq"):
                    parts = line.strip().split()
                    if len(parts) != 3:
                        raise SyntaxError(f"Invalid #ifeq syntax: {line}")
                    _, macro, value = parts
                    current = self.defines.get(macro)
                    self.condition_stack.append(current == value)
                    i += 1
                    continue

                # Handle #else
                elif line.startswith("#else"):
                    if not self.condition_stack:
                        raise SyntaxError("#else without #ifndef or #ifeq")
                    self.condition_stack[-1] = not self.condition_stack[-1]
                    i += 1
                    continue

                # Handle #endif
                elif line.startswith("#endif"):
                    if not self.condition_stack:
                        raise SyntaxError("#endif without #ifndef or #ifeq")
                    self.condition_stack.pop()
                    i += 1
                    continue

                # Handle shebang
                elif line.startswith("#!"):
                    print(line, end='')
                    i += 1
                    continue

                # Skip other lines starting with #
                elif line.lstrip().startswith("#"):
                    i += 1
                    continue

                # Skip lines in false condition blocks
                if False in self.condition_stack:
                    i += 1
                    continue

                # Replace defined macros
                for macro, value in self.defines.items():
                    line = line.replace(macro, value)

                print(line, end='')
                i += 1

if opts.chdir:
    os.chdir(opts.chdir)

pp = PreProcessor()

for define in opts.define:
    if '=' not in define:
        pp.define(define, "1")
    else:
        macro, value = define.split('=', maxsplit=1)
        pp.define(macro, value)

pp.include_files(opts.FILE)
