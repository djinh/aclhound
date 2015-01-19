#!/usr/bin/env python2.7
# Copyright (C) 2014-2015 Job Snijders <job@instituut.net>
#
# This file is part of ACLHound
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import datetime
import json
import ipaddr
import itertools

from targets import asa
from targets import ios
from targets import junos

now = datetime.date.today()
now_stamp = int(now.strftime('%Y%M%d'))


class Render():

    def __init__(self, name=None, **kwargs):
        self.data = []
        self.name = name

    """ relevant keys for compression/deduplication:
        AST({
            u'source':
                AST({u'l4': {'ports': ['any']},
                     u'l3': AST({u'ip': [u'any'], })}),
            u'destination':
                AST({u'l4': {'ports': ['any']},
                     u'l3': AST({u'ip': [u'any'], })}),
            u'protocol': u'any',
    """

    def add(self, ast):
        # only add policy to object if it is not expired
        expire = ast[0]['keywords']['expire']
        if expire:
            if int(expire) <= now_stamp:
                return
        self.data.append(ast)

    def output(self, vendor=None, afi=None):
        if not vendor:
            print('This class needs a vendor to output data correctly')
            return False
        return getattr(self, 'output_' + vendor)(afi=afi)

    def output_ios(self, **kwargs):
        return ios.render(self, **kwargs)

    def output_asa(self, **kwargs):
        return asa.render(self, **kwargs)

    def output_junos(self, **kwargs):
        return junos.render(self, **kwargs)

#    def __str__(self):
#        return '\n'.join(self.output(vendor=self.vendor, afi=self.afi))
