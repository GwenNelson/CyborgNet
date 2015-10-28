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

""" This file contains a reference implementation of the protocol over TCP that can be used for building software modules
"""

import hmac
import hashlib
import Queue
import time
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from enum import Enum

class ConnectionState(Enum):
   VERSION_NEGOTIATION = 1
   VERSION_SENT        = 2
   PRIV_REQUESTED      = 3
   PUB_REQUESTED       = 4
   SENT_MODULE_ID      = 5
   SENT_CHALLENGE_HMAC = 6

class ClientAction(Enum):
   PUB_FEED       = 1
   PUB_INPUT_FEED = 2
   SUB_FEED       = 3
   QUERY_SERVICE  = 4

class CyborgNetProtocol(basic.lineReceiver):
   def __init__(self,factory):
       self.factory = factory
       self.state                       = None
       self.challenge                   = ""
       self.module_id                   = ""
       self.is_paired                   = False
       self.shared_key                  = ''
       self.action                      = None
       self.protocol_version            = '0.1'
       self.connection_protocol_version = ''
       self.server_hostinfo             = ''
       self.server_protocol_version     = ''
   def connectionMade(self):
       self.state = ConnectionState.VERSION_NEGOTIATION
   def lineReceived(self, line):
       if self.state == ConnectionState.VERSION_NEGOTIATION:
          if not line.startswith('CyborgNet'):
             self.transport.loseConnection()
             self.server_hostinfo,self.server_protocol_version = map(lambda x: x.strip(), line.replace('CyborgNet','').split('protocol'))
             self.sendLine(self.protocol_version)
             self.state = ConnectionState.VERSION_SENT
       elif self.state == ConnectionState.VERSION_SENT:
          if line.startswith('OK'):
             self.connection_protocol_version = (line.split('protocol')[1]).strip()
          if line == 'pub/priv?':
             if self.is_paired:
                self.sendLine('priv')
                self.state = ConnectionState.PRIV_REQUESTED
             else:
                self.sendLine('pub')
                self.state = ConnectionState.PUB_REQUESTED
       elif self.state == ConnectionState.PRIV_REQUESTED:
          if line == 'ID?':
             self.sendLine(self.module_id)
             self.state = ConnectionState.SENT_MODULE_ID
       elif self.state == ConnectionState.SENT_MODULE_ID:
          if line == 'HMAC?':
             correct_resp = hmac.new(self.shared_key,self.challenge,hashlib.sha256).hexdigest()
             self.sendLine(correct_resp)
             self.state = ConnectionState.SENT_CHALLENGE_HMAC
          else:
             self.challenge = line
       elif self.state == ConnectionState.SENT_CHALLENGE_HMAC:
          if line.startswith('OK'):
             self.state = ConnectionState.CMD_MODE

class CyborgNetClient:
   def __init__(self,hub_addr=('127.0.0.1',4183),module_id='',shared_key='',is_paired=False):
       self.hub_addr         = hub_addr
       self.protocol_version = '0.1'
       self.is_paired        = is_paired
       self.shared_key       = shared_key
       self.module_id        = module_id
   def pair(self,shared_key):
       self.shared_key = shared_key
       self.is_paired  = True
   def connect(self):
       """ Connects a socket and prepares it
           Returns None on error
       """
       conn = telnetlib.Telnet(self.hub_addr[0],self.hub_addr[1])
       fd   = conn.get_socket().makefile()
       conn.read_until('protocol')
       server_ver = fd.readline().strip('\n')
       fd.write(self.protocol_version + '\n')
       conn.read_until('pub/priv?')
       if self.is_paired:
          pass
       else:
          fd.write('pub\n')
       conn.read_until('OK public access')
       return conn.get_socket()
   def register_event_feed(self,feed_id='',public=False):
       """ Connects, registers an event feed, disconnects - not very efficient but easy to use to get started
       """
       pass
   def publish_event(self,feed_id,event_data):
       """ Connects, publishes an event to an existing event feed, disconnects
       """
       pass
   def register_binary_feed(self,feed_id='',public=False):
       """ Connects, registers binary feed, disconnects
       """
       pass
   def publish_binary_data(self,feed_id=''):
       """ Connects, writes binary data to feed, disconnects
       """
       pass
   def get_binary_publish_socket(self,feed_id=''):
       """ Connects, handshakes, sends PUB command, returns socket object
           for application to write data to efficiently
       """
       pass
   def get_binary_subscribe_socket(self,feed_id=''):
       """ Connects, handshakes, sends SUB command, returns socket object
           for application to read data from efficiently
       """
       pass
   def subscribe_event_feed_thread(self,feed_id='',callback=None,threaded_callback=False):
       """ Run this in a thread, provide a callback function
           Connects, subscribes to feed, calls callback function whenever an event comes in
           if threaded_callback is True, runs the callback in a new thread
       """
       pass
   def subscribe_input_feed_thread(self,feed_id='',callback=None,threaded_callback=False,public=False):
       """ Same as subscribe_event_feed_thread, but for an input feed
       """
       pass

