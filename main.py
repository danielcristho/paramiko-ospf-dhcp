from netmiko import ConnectHandler

rtr1 = {
        "device_type": "cisco_ios",
        "host": "10.10.10.1",
        "username": "cisco",
        "password": "cisco"
}

conn = ConnectHandler(**rtr1)
output = conn.send_command("show ip interface brief | exclude unassigned")
print(f"Interface on {rtr1['host']}")
print(output)
