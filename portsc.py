import sys,socket

ip =socket.gethostbyname(sys.argv[1])
ports = sys.argv[2]

request = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

for x in range(int(ports)):

    request = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    request.settimeout(0.1)
    if not request.connect_ex((f"{ip}",x)):
        print(f"port {x} is open")
    else:
        continue
request.close()