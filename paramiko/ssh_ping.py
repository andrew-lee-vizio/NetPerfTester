import paramiko
import time
import re

bastion_ip='10.64.139.242'
bastion_pass='root'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
ssh.connect(bastion_ip, username='root', password=bastion_pass)

chan = ssh.invoke_shell()


# other cloud server 
priv_ip='ip'
passw='pass'

# test_script='/root/check_rackconnect.sh'

chan.send('su -\n')
# time.sleep(1)

buff = ''
while buff.find('Password: ') < 0 :
    resp = chan.recv(9999)
    buff = resp.decode()
    # print(resp)

chan.send('root\n')

chan.send('cd /vendor/data/snaps\n')
cmd = './iperf -c 10.64.138.194 -p 5001\n'
chan.send(cmd)

while buff.find(' Mbits/sec') < 0 :
    resp = chan.recv(9999)
    buff = resp.decode()
    # print(buff)


ret=re.search( '/sec', buff)
# print(ret)
throughput = buff[79:93]
print(throughput)

ssh.close()

# print('command was successful:' + str(ret[0].span()))

# def run_cmd(cmd):
    # buff = ''
    # while not buff.endswith(':~# '):
    #     resp = chan.recv(9999)
    #     buff += resp
    #     print(resp)

    # Ssh and wait for the password prompt.
    # buff = ''
    # while not buff.endswith('\'s password: '):
    #     resp = chan.recv(9999)
    #     buff += resp
    #     print(resp)
    
    # Send the password and wait for a prompt.
    # time.sleep(3)
    # chan.send(passw + '\n')

    # buff = ''
    # while buff.find(' Mbits/sec.') < 0 :
    #     resp = chan.recv(9999)
    #     buff += resp
    #     print(resp)
       
    # ret=re.search( '(\d) done.', buff).group(1)
    # ssh.close()

    # print('command was successful:' + str(ret=='0'))

# scp_opt=""
# cmd='scp -q ' + scp_opt + ' -o NumberOfPasswordPrompts=1 -o StrictHostKeyChecking=no %s root@%s:~/; echo $? done.' % ( test_script, priv_ip )
# cmd = 'cd /vendor/data/snaps && rm logs.txt && journalctl -u networkmonitor >logs.txt && cat logs.txt | grep isIPDuplicated'
# cmd = './iperf -c 10.64.138.194 -p 5001'
# print('\n test 2\n cmd %s\n' % cmd)
# run_cmd(cmd)