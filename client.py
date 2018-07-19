from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor, stdio
from twisted.protocols.basic import LineReceiver
from sys import stdout
import json

class CommandReader(LineReceiver):
    delimiter = '\n'

    def connectionMade(self):
        self.factory = CommandClientFactory()
        self.connector = reactor.connectTCP("localhost", 5678, self.factory)

    def lineReceived(self, line):
        # Split command and argument
        args = line.split(" ")
        # Send command to server
        self.connector.transport.write(json.dumps(dict(command=args[0],id=args[1])))

class ServerInterfaceProtocol(Protocol):
    def dataReceived(self, data):
        # Decodes result received from server and prints to stdout
        print json.loads(data).values()[0]

class CommandClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return ServerInterfaceProtocol()

stdio.StandardIO(CommandReader())
reactor.run()