import SSHSession as SSHSession
import json
import time

class NetPerfTest:
    def __init__(self, sender, receiver, port='-1', protocol = '-1'):

        with open('config.json') as f:
            config = json.load(f)

        if port=='-1':
            self.port = config['param']['port'].upper()
        else:
            self.port=port
        self.port=self.port.upper()

        if protocol=='-1':
            self.protocol = config['param']['protocol']
        else:
            self.protocol = protocol
        self.protocol=self.protocol.upper()

        #sender/source
        self.src = config[sender]
        #receiver/destination
        self.dst=config[receiver]

    def openConnections(self):
        self.sender = SSHSession.SSHSession(self.src['ip'] , self.port, self.protocol, 
                                            self.src['hostname'], self.src['id'], self.src['password'])
        self.receiver = SSHSession.SSHSession(self.dst['ip'] , self.port, self.protocol, 
                                              self.dst['hostname'], self.dst['id'], self.dst['password'])
        print('[{}({})/{}({})\t]: SSH connections are established.'.format(self.sender.getHost(),self.sender.getIP(),self.receiver.getHost(),self.receiver.getIP()))
        self.sender.openConnection()
        self.receiver.openConnection()

        self.receiver.setReceiver()
        

    def runTest(self):
        self.sender.generatePacket(self.receiver.getIP())
        # self.result = '['+self.sender.getHost() + '>' + self.receiver.getHost() + '\t]' + self.protocol +' '+ self.receiver.getThroughtput() +' : ' + time.strftime('%Y-%m-%d %H:%M:%S')
        # print(self.result)
        # self.receiver.stopReceiverMode()

    def closeConnections(self):      
        self.sender.closeConnection()
        self.receiver.stopReceiverMode()
        self.receiver.closeConnection()
        print('[{}({})/{}({})\t]: SSH connections are closed.'.format(self.sender.getHost(),self.sender.getIP(),self.receiver.getHost(),self.receiver.getIP()))

    def getResult(self,cnt=-1):
        if (cnt == -1):
            self.result = '['+self.sender.getHost() + '->' + self.receiver.getHost() + '\t]: ' + self.protocol +' '+ self.receiver.getThroughtput() +', ' + time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.result = str(cnt) + '['+self.sender.getHost() + '->' + self.receiver.getHost() + '\t]: ' + self.protocol +' '+ self.receiver.getThroughtput() +', ' + time.strftime('%Y-%m-%d %H:%M:%S')
        return self.result
    
    def getProtocol(self):
        return self.protocol
    
    def setProtocol(self, protocol):
        if self.protocol == protocol:
            return 
        self.protocol = protocol
        self.protocol=self.protocol.upper()
        self.closeConnections()
        self.openConnections()

    def changeConnection(self):
        self.closeConnections()
        temp=self.src
        self.src=self.dst
        self.dst=temp
        self.openConnections()


