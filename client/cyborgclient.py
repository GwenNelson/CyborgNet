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

class CyborgNetClient:
   def __init__(self,hub_addr=('127.0.0.1',4183),module_id=''):
       self.hub_addr = hub_addr
   def set_shared_key(self,shared_key):
       self.shared_key = shared_key
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

