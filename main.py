
from twisted.internet import protocol, reactor
from time import ctime
import command as cmd
import topologyParser

import os

isDebug = True;

PORT = 9900
recvBuffer = ''

def writefile(filename,data):
    print 'write file size:::::::::',len(data)
    fp = open(filename,'a+b')
    fp.write(data)
    fp.close()

def setupTopology():
	topology = topologyParser.Topology('topology.xml')
	hostList = topology.getHost()
	for host in hostList:
		cmd.lxcStart(host)

	openflowSwitchList = topology.getOpenflowSwitch()
        ipList = topology.getInterfaceIp()
        ipList = list(set(ipList))
        
	dpidlist = cmd.getDpidList()

	openflowSwitchList = topology.getOpenflowSwitch()
	for openflowSwitch in openflowSwitchList:
		interfaceList = topology.getOpenflowSwitchInterface(openflowSwitch)
		cmd.ovsOpenflowd(openflowSwitch, '210.25.137.243', 6633)
		for	 interface in interfaceList:
			cmd.ovsDpctl(openflowSwitch, interface)

	i=0
        for openflowSwitch in openflowSwitchList:
                interfaceList = topology.getOpenflowSwitchInterface(openflowSwitch)
		inportList = cmd.getPort(dpidlist[i])
		for	 interface in interfaceList:
                        for ip in ipList:
                                cmd.addFlowSpace(dpidlist[i],'20','in_port='+ inportList[interface]+',nw_src='+ip,'Slice:rfSlice=4')
                i=i+1   

class TSServProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print '...connected from:', clnt
    def dataReceived(self, data):
	global recvBuffer
	global filename
	recvBuffer = recvBuffer + data
	self.processRecvBuffer()

    def processRecvBuffer(self):
	global recvBuffer
	global filename
	while len(recvBuffer) > 0 :
            index1 = recvBuffer.find('CMB_BEGIN')
            index2 = recvBuffer.find('CMB_END')
 
            if index1 >= 0 and index2 >= 0:
                data = recvBuffer[index1+9:index2]
                recvBuffer = recvBuffer[index2+7:]
		writefile("./to.xml",data)
		setupTopology()
		os.system("python cli.py")
	    else:
		break

factory = protocol.Factory()
factory.protocol = TSServProtocol
print 'waiting for connection...'
reactor.listenTCP(PORT, factory)
reactor.run()
