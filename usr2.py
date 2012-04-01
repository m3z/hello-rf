# -*- coding: utf-8 -*-

import command as cmd
import topologyParser

isDebug = True;

#ovsList = {}

def setSlices():
        cmd.createSlice('rfSlice','tcp:210.25.137.242:6666','rf@visor.com')
        

def setupTopology():
	topology = topologyParser.Topology('topology.xml')
	hostList = topology.getHost()
#	for host in hostList:
#		cmd.lxcStart(host)

	openflowSwitchList = topology.getOpenflowSwitch()
        ipList = topology.getInterfaceIp()
        
	dpidlist = cmd.getDpidList()
	
#	for openflowSwitch in openflowSwitchList:
#		interfaceList = topology.getOpenflowSwitchInterface(openflowSwitch)
		
#		for	 interface in interfaceList:
#			cmd.ovsDpctl(openflowSwitch, interface)
        i=0
        for openflowSwitch in openflowSwitchList:
                interfaceList = topology.getOpenflowSwitchInterface(openflowSwitch)
		inportList = cmd.getPort(dpidlist[i])
		for	 interface in interfaceList:
                        for ip in ipList:
                                cmd.addFlowSpace(dpidlist[i],'20','in_port='+ inportList[interface]+',nw_src='+ip,'Slice:rfSlice=4')
                i=i+1     
                
if __name__ == '__main__':
        setSlices()
        setupTopology()
