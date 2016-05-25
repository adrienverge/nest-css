#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Adrien Vergé
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import io
import sys

import tinycss


def remove_macros(source):
    return '\n'.join([l for l in source.split('\n') if not l.startswith('#')])


def nest_css(input_file, nest_selector, output=sys.stdout):
    with open(input_file) as f:
        source = f.read()

    source = remove_macros(source)
    lines = source.split('\n')
    pos = [0, 0]
    b = io.BytesIO(source.encode('utf-8'))

    parser = tinycss.make_parser('page3')
    stylesheet = parser.parse_stylesheet_file(b)

    for r in stylesheet.rules:
        if isinstance(r, tinycss.css21.PageRule):
            continue

        # Print the original document until just before the selector
        while pos[0] < r.selector.line - 1:
            output.write(lines[pos[0]][pos[1]:] + '\n')
            pos[0] += 1
            pos[1] = 0
        output.write(lines[pos[0]][pos[1]:r.selector.column - 1])
        pos[1] = r.selector.column - 1

        original_selector = r.selector.as_css()
        selector_lines = original_selector.split('\n')
        if len(selector_lines) == 1:
            pos[1] += len(selector_lines[0])
        else:
            pos[0] += len(selector_lines) - 1
            pos[1] = len(selector_lines[-1])

        tokens = list(r.selector)
        if len(tokens) > 0:
            new_selector = nest_selector + ' '
            for token in tokens:
                new_selector += token.as_css()
                if token.type == 'DELIM' and token.value == ',':
                    new_selector += ' ' + nest_selector + ' '
            output.write(new_selector)

    # Print the original document until the end
    while pos[0] < len(lines):
        output.write(lines[pos[0]][pos[1]:])
        pos[0] += 1
        pos[1] = 0
        if pos[0] < len(lines):
            output.write('\n')


if __name__ == '__main__':
    def usage():
        sys.stderr.write('usage: %s INPUT_FILE SELECTOR\n' % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) != 3:
        usage()

    input_file = sys.argv[1]
    selector = sys.argv[2]

    nest_css(input_file, selector)
