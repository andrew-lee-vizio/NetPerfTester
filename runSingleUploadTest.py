import SSHSession as SSHSession
import json
import time

with open('config.json') as f:
    config = json.load(f)
    # print(config)

port = config['param']['port']
protocol = config['param']['protocol']
#sender/source
src = config['tv']
#receiver/destination
dst=config['pc']

sender = SSHSession.SSHSession(src['ip'] ,port, protocol, src['hostname'], src['id'], src['password'])
sender.openConnection()
receiver = SSHSession.SSHSession(dst['ip'] ,port, protocol, dst['hostname'], dst['id'], dst['password'])
receiver.openConnection()

receiver.setReceiver()
sender.generatePacket(receiver.getIP())

ret = src['hostname'] + ' --> ' + dst['hostname'] + ': ' + receiver.getThroughtput() +' : ' + time.strftime('%Y-%m-%d %H:%M:%S')

sender.closeConnection()
receiver.stopReceiverMode()
receiver.closeConnection()

print(ret)