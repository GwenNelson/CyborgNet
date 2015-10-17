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

PROTOCOL_VERSION_MAJOR = 0
PROTOCOL_VERSION_MINOR = 1
PROTOCOL_HOSTINFO      = 'Python alpha'

PROTOCOL_GREETING      = 'CyborgNet %s protocol %s.%s' % (PROTOCOL_HOSTINFO,PROTOCOL_VERSION_MAJOR,PROTOCOL_VERSION_MINOR)

TCP_PORT               = 4183

TCP_ENDPOINT           = 'tcp:%d' % TCP_PORT

SHELL_GREETING = """

Welcome to the CyborgNet hub server, type help for a list of commands

"""

SHELL_PROMPT = '> '

SHELL_HELP = """
 help - display this help message
 exit - shutdown the server
 pair - pair a module
        takes 2 parameters: <module ID>
                            <shared secret>
"""
