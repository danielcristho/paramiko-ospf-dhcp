import paramiko, yaml, time
from pprint import pprint
from datetime import datetime

sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def readYaml(yamlFile):
    with open(yamlFile) as f:
        inventory = f.read()

    inventoryDict = yaml.load(inventory)
    return inventoryDict

def deviceCredentials(routerCred):
    device = {
            "ip": routerCred,
            "username": "admin",
            "password": "admin",
    }
    conn = sshClient.invoke_shell()

    if device['enable']:
        conn.send("enable\n")
        conn.send("cisco\n") #send secret
        time.sleep(2)

#config ip address
def configAddress(conn, ipConfig):
    interface = ipConfig['interface']
    ipAddr = ipConfig['ipAddress']
    configList = ['interface {}'.format(interface),
                    'ip address {}'.format(ipAddr),
                    'no shutdown']

    print (conn.send(configList))                

#config DHCP
def configDhcp(conn, dchpConfig):
    pool = dchpConfig['pool']
    network = dchpConfig['network']
    gateway = dchpConfig['gateway']
    configList = ['ip dhcp pool {}'.format(pool),
                    'network {}'.format(network),
                    'default-router {}'.format(gateway)]
    print(conn.send(configList))

#config OSPF
def configOspf(conn, ospfConfig):
    area = ospfConfig['area']
    networkList  = ospfConfig['network']
    confifList = ['router ospf 1']
    for network in networkList:
        confifList.append('network {} area {}'.format(network, area))
    print(conn.send(confifList))

def main():
    yamlFile = 'inventory.yaml'
    inventoryDict = readYaml(yamlFile)
    pprint(inventoryDict)

    for router in inventoryDict['DEVICE']:

        routerCred = router['host']
        print("=============================")
        print("Configuring {}".format(routerCred))
        print("=============================")
        
        conn = deviceCredentials(routerCred)

        ipConfig = router['intConfig']
        for conf in ipConfig:
            configAddress(conn, conf)

        dhcpConfig = router['dhcpConfig']
        for config in dhcpConfig:
            configDhcp(conn, config)

        ospfConfig = router['ospfConfig']
        for config in ospfConfig:
            configOspf(conn, config)

        sshClient.close()    
main()    

