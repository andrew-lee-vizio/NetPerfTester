#python_paramiko.py

import paramiko

ssh =  paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.64.139.242', port='22', username='root', password='root')

# stdin, stdout, stderr = ssh.exec_command('df -h')
# print(''.join(stdout.readlines()))

stdin, stdout, stderr = ssh.exec_command('cd /vendor/data/snaps')
# print(''.join(stdout.readlines()))
stdin, stdout, stderr = ssh.exec_command('ll')
# print(''.join(stdout.readlines()))
stdin, stdout, stderr = ssh.exec_command('rm logs.txt')
stdin, stdout, stderr = ssh.exec_command('journalctl -u networkmonitor | grep isIPDuplicated')
stdin, stdout, stderr = ssh.exec_command('cat logs.txt')



# stdin, stdout, stderr = ssh.exec_command('cd /vendor/data/snaps && rm logs.txt && journalctl -u networkmonitor >logs.txt && cat logs.txt | grep isIPDuplicated')

print(''.join(stdout.readlines()))

ssh.close()
