from twisted.internet.protocol import Protocol, ClientFactory
from sys import stdout
from twisted.internet import reactor, stdio
from twisted.protocols.basic import LineReceiver
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
        print json.loads(data).values()[0]

class CommandClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return ServerInterfaceProtocol()

stdio.StandardIO(CommandReader())
reactor.run()