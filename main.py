# -*- coding: utf-8 -*-

import command as cmd
import topologyParser

isDebug = True;

def startControllers():
	cmd.noxCore('switch')
	cmd.noxCore('routeflowc')
	cmd.runRfServer()

def	setupControlPlane():
	cmd.lxcStart('router1')
	cmd.lxcStart('router2')
	cmd.ovsOpenflowd('dp0', '127.0.0.1', 6666, 'rfovs')
	cmd.ifconfig('dp0', 'up')
	cmd.ovsOpenflowd('br0', '127.0.0.1', 6363)
	cmd.ifconfig('br0', 'up', '192.168.1.1', '255.255.255.0')
	dp0Interface = ['router1.1', 'router1.2', 'router2.1', 'router2.2']
	for interface in dp0Interface:
		cmd.ovsDpctl('dp0', interface)

	br0Interface = ['router1.0', 'router2.0']
	for interface in br0Interface:
		cmd.ovsDpctl('br0', interface)

def setupTopology():
	topology = topologyParser.Topology('topology.xml')
	hostList = topology.getHost()
	for host in hostList:
		cmd.lxcStart(host)

	openflowSwitchList = topology.getOpenflowSwitch()
	for openflowSwitch in openflowSwitchList:
		interfaceList = topology.getOpenflowSwitchInterface(openflowSwitch)
		cmd.ovsOpenflowd(openflowSwitch, '210.25.137.243', 6633)
		for	 interface in interfaceList:
			cmd.ovsDpctl(openflowSwitch, interface)

if __name__ == '__main__':
	startControllers()
	setupControlPlane()
#	setupTopology()
