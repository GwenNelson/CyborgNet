"""
The MIT License (MIT)

Copyright (c) 2015 Gareth Nelson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from config import *
from twisted.protocols import basic
from twisted.internet import reactor
import sys

class HubServerShell(basic.LineReceiver):
    from os import linesep as delimiter
    def __init__(self,hub_core):
        self.hub_core = hub_core
    def connectionMade(self):
        self.sendLine(PROTOCOL_GREETING)
        self.sendLine(SHELL_GREETING)
        self.transport.write(SHELL_PROMPT)

    def lineReceived(self, line):
        if line == 'help':
           self.sendLine(SHELL_HELP)
        if line == 'exit':
           reactor.stop()
        if line.startswith('pair'):
           split_line = line.split()
           if len(split_line) != 3:
              self.transport.write('ERROR - command takes 3 parameters!\n')
           else:
              self.hub_core.pair_module(split_line[1],split_line[2])
              self.transport.write('Paired module %s\n' % split_line[1])
        self.transport.write(SHELL_PROMPT)

