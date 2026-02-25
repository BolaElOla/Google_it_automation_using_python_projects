import sys,socket

ip = sys.argv[1]
ports = sys.argv[2]

request = socket.socket(socket.Af_INET,socket.SOCK_STREAM)

for x in range(ports):
    if request.connect_ex(f"{ip}",x):
        print(f"port {x} is open")
    else:
        continue
request.close()