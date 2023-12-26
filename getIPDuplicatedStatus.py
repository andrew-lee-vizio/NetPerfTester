import SSHSession as SSHSession

port = '5002'
protocol = 'TCP'

tv = SSHSession.SSHSession('10.64.138.158',port, protocol)
tv.openConnection()
tv.switchSuperuser()
tv.gotoWorkspace()
tv.send('rm logs.txt')
tv.send('journalctl -u networkmonitor > logs.txt')
tv.send('cat logs.txt')