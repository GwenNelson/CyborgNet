import hmac
import hashlib
import Queue
import time
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from enum import Enum

from config import *

class ConnectionState(Enum):
   VERSION_NEGOTIATION = 1
   PUBLIC_PRIV_SELECT  = 2
   PRIV_ID_REQUESTED   = 3
   PRIV_CHALLENGE_SENT = 4
   AWAITING_COMMAND    = 5
   EVENT_FEED_PUBLISH  = 6
   BINARY_PUBLISH      = 7
   FEED_SUBSCRIBE      = 8

def gen_ver_greeting():
    return 'CyborgNet %s protocol %s' % (protocol_hostinfo,protocol_ver)

def gen_challenge_str():
    return hashlib.md5(time.ctime()).hexdigest()

def get_secret(module_id):
    return ''

def verify_hmac(remote_hmac, secret, challenge):
    return True

class CyborgNetProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory        = factory
        self.state          = None
        self.challenge      = ""
        self.secret         = ""
        self.module_id      = ""
        self.private_access = False

    def connectionMade(self):
        self.sendLine(gen_ver_greeting())
        self.state = ConnectionState.VERSION_NEGOTIATION

    def connectionLost(self, reason):
        self.state = None

    def lineReceived(self, line):
        if self.state is ConnectionState.VERSION_NEGOTIATION:
           if line != protocol_ver:
              self.sendLine("ERROR: Protocol mismatch")
              self.transport.loseConnection()
              self.state = None
           else:
              self.sendLine("OK protocol version %s" % protocol_ver)
              self.sendLine("pub/priv?")
              self.state = ConnectionState.PUBLIC_PRIV_SELECT

        elif self.state is ConnectionState.PUBLIC_PRIV_SELECT:
           if line=='pub':
              self.sendLine("OK public access")
              self.state = ConnectionState.AWAITING_COMMAND
           elif line=='priv':
              self.sendLine("ID?")
              self.state = ConnectionState.PRIV_ID_REQUESTED
           else:
              self.sendLine("ERROR: invalid input")
              self.transport.loseConnection()
              self.state = None
        
        elif self.state is ConnectionState.PRIV_ID_REQUESTED:
           self.module_id = line
           self.secret    = get_secret(self.module_id)
           self.challenge = gen_challenge_str()
           self.sendLine(self.challenge)
           self.sendLine("HMAC?")
           self.state = ConnectionState.PRIV_CHALLENGE_SENT

        elif self.state is ConnectionState.PRIV_CHALLENGE_SENT:
           if verify_hmac(line, self.secret, self.challenge):
              self.sendLine("OK private access")
              self.private_access = True
              self.state = ConnectionState.AWAITING_COMMAND
           else:
              self.sendLine("ERROR: Authentication error")
              self.transport.loseConnection()
              self.state = None

        elif self.state is ConnectionState.AWAITING_COMMAND:
           pass

class CyborgNetProtocolFactory(protocol.Factory):
    def __init__(self,hub_core):
        self.hub_core = hub_core

    def buildProtocol(self, addr):
        return CyborgNetProtocol(self)




