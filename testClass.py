import SSHSession as SSHSession
from netmiko import ConnectHandler

# ssh = SSHSession.SSHSession('10.64.138.194','5001')
# ssh = SSHSession.SSHSession('10.64.138.194','root','root','root',':/$')

# chan = ssh.openConnection()
# ssh.switchSuperuser()
# ssh.send('ll')
# ssh.closeConnection()
# ssh.printTerminal()


# from netmiko import ConnectHandler

rootPattern = ':/$'

device = ConnectHandler(device_type='linux', ip='10.64.138.194',username='root', password='root')

output = device.send_command_timing('su -\n',0.1)
if 'Password: ' not in output:
    print("ERROR")
    exit

output = device.send_command_timing('root',0.1)
# print(output)
# print()

output += device.send_command_timing('cd vendor/data/snaps',0.1)
output += device.send_command_timing('ll',0.1)

print(output)

# output = device.send_command('exit')
# print(output)



device.disconnect()

