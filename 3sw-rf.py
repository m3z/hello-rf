# -*- coding: utf-8 -*-

import command as cmd
import topologyParser

isDebug = True;

def startControllers():
	cmd.noxCore('switch')
	cmd.noxCore('routeflowc')
	cmd.runRfServer()

def	setupControlPlane():
	cmd.lxcStart('router3')
	cmd.lxcStart('router4')
	cmd.lxcStart('router5')
	cmd.ovsOpenflowd('dp0', '127.0.0.1', 6666, 'rfovs')
	cmd.ifconfig('dp0', 'up')
	cmd.ovsOpenflowd('br0', '127.0.0.1', 6363)
	cmd.ifconfig('br0', 'up', '192.168.1.1', '255.255.255.0')
	dp0Interface = ['router3.1', 'router3.2', 'router4.1', 'router4.2','router5.1','router5.2']
	for interface in dp0Interface:
		cmd.ovsDpctl('dp0', interface)

	br0Interface = ['router3.0', 'router4.0','router5.0']
	for interface in br0Interface:
		cmd.ovsDpctl('br0', interface)



if __name__ == '__main__':
	startControllers()
	setupControlPlane()

