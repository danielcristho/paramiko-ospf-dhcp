import paramiko
import yaml
from pprint import pprint
import time

inputFile = input("Enter YAML File: ") or 'inventory.yml'
yamlFile = open(inputFile, 'r')
yamlData = yaml.safe_load(yamlFile)

for router in yamlData
    ip = router['host']
    username = router['username']
    password = router['password']