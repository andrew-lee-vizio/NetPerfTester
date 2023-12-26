import SSHSession as SSHSession

port = '5002'
protocol = 'TCP'

tv = SSHSession.SSHSession('10.64.139.242',port, protocol)
tv.openConnection()
tv.switchSuperuser()
tv.gotoWorkspace()
tv.setReceiver()

pc = SSHSession.SSHSession('10.64.138.208', port, protocol, 'NUC','networkmonitor', 'networkmonitor')
# pc.setLinuxBox('NUC','networkmonitor', 'networkmonitor')
pc.openConnection()

pc.generatePacket(tv.getIP())
print(tv.getThroughtput())

tv.stopReceiverMode()
pc.closeConnection()
tv.closeConnection()
