# import paramiko
from netmiko import ConnectHandler, NetmikoTimeoutException
import re

class SSHSession:
    tcpOpt = ' -w 128k -t 10'
    udpOpt = ' -u -b 50M -t 10'

    channel:str

    def __init__(self, _ip, _port, _isTCP, _host='tv', _id='root', _password='root'):
        self.ip=_ip
        self.iperfPort=_port
        self.isTCP=_isTCP.upper()
        self.host=_host
        self.username = _id
        self.password = _password

    def openConnection(self):
        self.device = ConnectHandler(device_type='linux', 
            ip=self.ip, username=self.username, password=self.password)
        # self.printLog("SSH connection is opended: " + self.ip)
        if self.password == 'root':
           count=0
           while self.switchSuperuser() == False:
               count+=1
               if(count==3):
                   self.printLog("ERROR, it's not able to switch the super user!")
                   return False
            
           return self.gotoWorkspace()

    def closeConnection(self):
        self.device.disconnect()
        # self.printLog("SSH connection is closed: " + self.ip)

    def switchSuperuser(self, rootPw='root'):
        output = self.device.send_command_timing('su -\n',2)
        if 'Password: ' not in output:
            print("ERROR")
            return False
            
        self.device.send_command_timing(rootPw)
        output = self.device.send_command_timing('whoami\n', 0.1)
        # self.printLog("current user: " + output)

        if (output != 'root'): 
            self.printLog("ERROR! Fail to swithch to root user on TV!")
            return False
        return True

    def gotoWorkspace(self):
        output = self.device.send_command_timing('cd /vendor/data/snaps', cmd_verify=True)
        # self.printLog(output)
        output = self.device.send_command_timing('ll | grep iperf', cmd_verify=True)
        # self.printLog(output)
        if ('iperf' not in output):
            self.device.send_command_timing('cp /apps/acr/basic/iperf .', cmd_verify=True)
            self.device.send_command_timing('cp /apps/castshell/board/bin/iperf .',cmd_verify=True)
            output = self.device.send_command_timing('ll | grep iperf', cmd_verify=True)
            # self.printLog(output)
            if ('iperf' not in output):
                self.printLog("ERROR. No iperf file in the workspace!")
                return False
        else:
            return True
    
    def setReceiver(self):
        if self.password == 'root':
            cmd = './iperf -s -p ' + self.iperfPort
        else:
            cmd = 'iperf -s -p ' + self.iperfPort

        if (self.isTCP == 'UDP'): 
            cmd += ' -u'
        # self.channel = '\n'
        self.channel = self.device.send_command_timing(cmd, cmd_verify=True)
        # self.printLog(self.channel)        

    def getThroughtput(self):
        # while self.channel.find('/sec') < 0:
        #     try:
        #         buff = self.device.read_channel()
        #         self.printLog(buff)
        #         self.channel += buff
        #     except NetmikoTimeoutException:
        #         break
        try:
            buff=self.device.read_until_pattern(pattern='/sec', read_timeout= 30)
            self.channel=buff
            # self.printLog(buff)
        except NetmikoTimeoutException:
            self.printLog(self.channel)

        pos=re.search( '/sec', self.channel)
        if pos:
            self.throuthput=self.channel[pos.span()[0]-11:pos.span()[1]]
        else:
            self.throughtput='ERROR'
            
        # self.printLog(self.throuthput)
        self.channel=''
        return self.throuthput

    def stopReceiverMode(self):
        output = self.device.send_command_timing('\x03')
        # self.printLog(output)
        self.device.clear_buffer()

    def printLog(self, str):
        print("[" + self.host + "\t]: " + str)

    def generatePacket(self, targetIp):
        if self.password == 'root':
            cmd = './iperf -c ' + targetIp + ' -p ' + self.iperfPort
        else:
            cmd = 'iperf -c ' + targetIp + ' -p ' + self.iperfPort
        if (self.isTCP == 'UDP'):
            cmd+=self.udpOpt
        else:
             cmd+=self.tcpOpt
        # self.printLog(cmd)
        output=self.device.send_command_timing(cmd, cmd_verify=True)
        # output=self.device.send_command_timing(cmd, last_read=1,cmd_verify=True)
        # self.printLog(output)        

    def send(self, cmd):
        output = self.device.send_command_timing(cmd, cmd_verify=True)
        # self.printLog(output)        
    
    def getIP(self):
        return self.ip
    
    def getHost(self):
        return self.host
    





