
from twisted.internet import protocol, reactor
import topologyParser
import time

HOST = '210.25.137.242'
PORT = 21567

class TSClntProtocol(protocol.Protocol):
    def sendCmd(self,data):
	print '...sending %s...' % data
        self.sendLine(data)
	
    def sendData(self):
        topology = topologyParser.Topology('to.xml')
        hostList = topology.getHost()
        for host in hostList:
               	 data = "lxcStart('"+host+"')"+'\n'
           	 self.sendCmd(data)
		 
		 openflowSwitchList = topology.getOpenflowSwitch()
       	for openflowSwitch in openflowSwitchList:
                 interfaceList = topology.getOpenflowSwitchInterface(openflowSwitch)
                 data = "ovsOpenflowd('"+openflowSwitch+"', '210.25.137.243', 6633)\n"
		 print '...sending %s...' % data
                 self.transport.write(data)
                 for      interface in interfaceList:
                        data="ovsDpctl('"+openflowSwitch+"','"+ interface+"')\n"
			print '...sending %s...' % data
                 	self.transport.write(data)
			time.sleep(1)



        self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        print data
#        self.sendData()

class TSClntFactory(protocol.ClientFactory):
    protocol = TSClntProtocol
    clientConnectionLost = clientConnectionFailed = \
        lambda self, connector, reason: reactor.stop()

reactor.connectTCP(HOST, PORT, TSClntFactory())
reactor.run()
