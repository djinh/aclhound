#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CAVEAT UTILITOR
# This file was automatically generated by Grako.
#    https://bitbucket.org/apalala/grako/
# Any changes you make to it will be overwritten the
# next time the file is generated.
#

from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import * # noqa
from grako.exceptions import * # noqa


__version__ = '14.167.10.59.20'


class grammarParser(Parser):
    def __init__(self, whitespace=None, **kwargs):
        super(grammarParser, self).__init__(whitespace=whitespace, **kwargs)

    @rule_def
    def _start_(self):
        def block1():
            self._rule_()
        self._positive_closure(block1)

        self.ast['@'] = self.last_node
        self._check_eof()

    @rule_def
    def _rule_(self):
        self._action_expr_()
        self.ast['action'] = self.last_node
        self._cut()
        self._protocol_expr_()
        self.ast['protocol'] = self.last_node
        self._cut()
        self._source_expr_()
        self.ast['source'] = self.last_node
        self._cut()
        self._dst_expr_()
        self.ast['destination'] = self.last_node
        self._cut()
        self._state_expr_()
        self.ast['state'] = self.last_node
        self._expire_expr_()
        self.ast['expire'] = self.last_node
        self._cut()
        self._comment_expr_()
        self.ast['comment'] = self.last_node

    @rule_def
    def _state_expr_(self):
        with self._optional():
            self._token('stateful')

    @rule_def
    def _expire_expr_(self):
        with self._optional():
            self._token('expire')
            self._date_()
            self.ast['@'] = self.last_node

    @rule_def
    def _date_(self):
        self._pattern(r'[0-9]{8}')

    @rule_def
    def _action_expr_(self):
        with self._choice():
            with self._option():
                self._token('allow')
            with self._option():
                self._token('deny')
            self._error('expecting one of: deny allow')

    @rule_def
    def _protocol_expr_(self):
        with self._choice():
            with self._option():
                self._icmp_expr_()
                self.ast['icmp'] = self.last_node
                self._cut()
            with self._option():
                self._token('udp')
                self._cut()
            with self._option():
                self._token('tcp')
                self._cut()
            with self._option():
                self._token('any')
                self._cut()
            self._error('expecting one of: udp any tcp')

    @rule_def
    def _icmp_expr_(self):
        self._token('icmp')
        self._icmp_term_()

    @rule_def
    def _icmp_term_(self):
        with self._choice():
            with self._option():
                self._group_expr_()
                self.ast['include'] = self.last_node
                self._cut()
            with self._option():
                self._icmp_parameter_()
                self.ast['icmp_type'] = self.last_node
                self._icmp_parameter_()
                self.ast['icmp_code'] = self.last_node
            self._error('no available options')

    @rule_def
    def _icmp_parameter_(self):
        with self._optional():
            self._number_()

    @rule_def
    def _comment_expr_(self):
        with self._optional():
            self._token('#')
            self._pattern(r'.*[\n]?')
            self.ast['@'] = self.last_node

    @rule_def
    def _string_(self):
        self._pattern(r'[a-zA-Z0-9_-]+')

    @rule_def
    def _address_string_(self):
        self._pattern(r'[a-fA-F0-9\.:\/]+')

    @rule_def
    def _source_expr_(self):
        self._token('src')
        self._cut()
        self._endpoint_tuple_()
        self.ast['@'] = self.last_node

    @rule_def
    def _dst_expr_(self):
        self._token('dst')
        self._cut()
        self._endpoint_tuple_()
        self.ast['@'] = self.last_node

    @rule_def
    def _endpoint_tuple_(self):
        self._endpoint_expr_()
        self.ast['l3'] = self.last_node
        self._portgroup_expr_()
        self.ast['l4'] = self.last_node

    @rule_def
    def _endpoint_list_(self):
        def block1():
            self._prefix_()
        self._positive_closure(block1)

        self.ast['@'] = self.last_node
        self._check_eof()

    @rule_def
    def _endpoint_expr_(self):
        with self._choice():
            with self._option():
                self._token('any')
                self.ast.add_list('ip', self.last_node)
            with self._option():
                self._prefix_()
                self.ast.add_list('ip', self.last_node)
            with self._option():
                self._group_expr_()
                self.ast['include'] = self.last_node
            self._error('expecting one of: any')

    @rule_def
    def _group_expr_(self):
        self._token('@')
        self._cut()
        self._string_()
        self.ast['@'] = self.last_node

    @rule_def
    def _portgroup_expr_(self):
        with self._optional():
            self._token('port')
            self._port_term_()
            self.ast['@'] = self.last_node

    @rule_def
    def _port_term_(self):
        with self._choice():
            with self._option():
                self._token('any')
                self.ast.add_list('ports', self.last_node)
            with self._option():
                self._group_expr_()
                self.ast['include'] = self.last_node
            with self._option():
                def block3():
                    self._port_atoms_()
                self._closure(block3)
                self.ast['ports'] = self.last_node
            self._error('expecting one of: any')

    @rule_def
    def _port_atoms_(self):
        self._port_expr_()
        self.ast.add_list('@', self.last_node)
        def block1():
            self._token(',')
            self._port_expr_()
            self.ast.add_list('@', self.last_node)
        self._closure(block1)

    @rule_def
    def _port_expr_(self):
        with self._choice():
            with self._option():
                self._port_range_()
                self.ast['range'] = self.last_node
            with self._option():
                self._port_number_()
                self.ast['single'] = self.last_node
            self._error('no available options')

    @rule_def
    def _port_range_(self):
        self._NUMBER_()
        self.ast['@'] = self.last_node
        self._token('-')
        self._NUMBER_()
        self.ast['@'] = self.last_node
        self._cut()

    @rule_def
    def _port_number_(self):
        self._NUMBER_()
        self._cut()

    @rule_def
    def _number_(self):
        self._NUMBER_()
        self._cut()

    @rule_def
    def _prefix_(self):
        self._address_string_()
        self._cut()

    @rule_def
    def _NUMBER_(self):
        self._pattern(r'[0-9]+')


class grammarSemanticParser(CheckSemanticsMixin, grammarParser):
    pass


class grammarSemantics(object):
    def start(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def state_expr(self, ast):
        return ast

    def expire_expr(self, ast):
        return ast

    def date(self, ast):
        return ast

    def action_expr(self, ast):
        return ast

    def protocol_expr(self, ast):
        return ast

    def icmp_expr(self, ast):
        return ast

    def icmp_term(self, ast):
        return ast

    def icmp_parameter(self, ast):
        return ast

    def comment_expr(self, ast):
        return ast

    def string(self, ast):
        return ast

    def address_string(self, ast):
        return ast

    def source_expr(self, ast):
        return ast

    def dst_expr(self, ast):
        return ast

    def endpoint_tuple(self, ast):
        return ast

    def endpoint_list(self, ast):
        return ast

    def endpoint_expr(self, ast):
        return ast

    def group_expr(self, ast):
        return ast

    def portgroup_expr(self, ast):
        return ast

    def port_term(self, ast):
        return ast

    def port_atoms(self, ast):
        return ast

    def port_expr(self, ast):
        return ast

    def port_range(self, ast):
        return ast

    def port_number(self, ast):
        return ast

    def number(self, ast):
        return ast

    def prefix(self, ast):
        return ast

    def NUMBER(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = grammarParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in grammarParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for grammar.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(args.file, args.startrule, trace=args.trace, whitespace=args.whitespace)
