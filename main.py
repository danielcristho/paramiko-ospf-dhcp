import paramiko
import json, getpass, time

with open('inventory.json', 'r') as f:
    devices = json.load(f)

with open('command.txt', 'r') as f:
    commands = f.readlines()

username = input('username: ')
password = getpass.getpass('password: ')

max_buffer = 65535

def clearBuff(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)

for device in devices.keys():
    outputFileName = device + '_output.txt'
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(devices[device]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
    newConnection = connection.invoke_shell()
    output = clearBuff(newConnection)
    time.sleep(3)
    newConnection.send("terminal length 0\n")
    output = clearBuff(newConnection)
    with open(outputFileName, 'wb') as f:
        for command in commands:
            newConnection.send(command)
            time.sleep(2)
            output = newConnection.recv(max_buffer)
            print(output)
            f.write(output)
    newConnection.close()       
