import paramiko
import time
import re

src_ip = '10.64.138.208'
src_id = 'networkmonitor'
src_pass = 'networkmonitor'
src_rootpw = 'Debian@vizio'
src_rootpattern = 'root'

dst_ip='10.64.139.242'
dst_id='root'
dst_pass='root'
dst_rootpattern = ''

iperf_port='5001 '
iperf_opt='-t 10'

ssh1 = paramiko.SSHClient()
ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh1.connect(src_ip, username=src_id, password=src_pass)
src = ssh1.invoke_shell()

ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect(dst_ip, username=dst_id, password=dst_pass)

src_cmd='iperf -c '+dst_ip+' -p ' + iperf_port + iperf_opt
dst_cmd='./iperf -s -p ' + iperf_port

dst = ssh2.invoke_shell()

# [dst] switch superuser and go to the vendor/data/snaps folder
dst_buff = ''
dst.send('su -\n')
while dst_buff.find('Password: ') <0 :
    resp = dst.recv(1024)
    dst_buff = resp.decode()
    # print(dst_buff)

dst.send('root\n')
# need to optimize later
while dst_buff.find(':/$') <0 :
    resp = dst.recv(1024)
    dst_buff = resp.decode()
    # print(dst_buff)
# print('DST: switched to superuser\n')

dst.send('cd /vendor/data/snaps\n')
dist_buff=''
dst.send(dst_cmd+'\n')
while dst_buff.find('Server listening on TCP port') <0 :
    resp = dst.recv(1024)
    dst_buff = resp.decode()
    # print(dst_buff)
print('DST: DST is ready to go!!! ' + iperf_port)

# [src] switch superuser and go to the vendor/data/snaps folder
src_buff=''
src.send('su -\n')
while src_buff.find('Password: ') <0 :
    resp = src.recv(1024)
    src_buff = resp.decode()

src.send(src_rootpw+'\n')
while src_buff.find(src_rootpattern) <0 :
    resp = src.recv(1024)
    src_buff = resp.decode()
    # print(src_buff)
    if src_buff.find(src_id) >0 :
        print('SRC: authenticaion failure\n')
        break
    
print('SRC: SRC is ready to go!!!')

src.send(src_cmd+'\n')
# print(src.recv(1024))
# print('\n')

while dst_buff.find(' Mbits/sec') < 0 :
    resp = dst.recv(1024)
    dst_buff += resp.decode()
    # print(dst_buff)

ret=re.search( 'Mbits/sec', dst_buff)

# print(ret)
throughput = dst_buff[ret.span()[0]-6:ret.span()[1]]
print(throughput)

ssh1.close()
ssh2.close()
